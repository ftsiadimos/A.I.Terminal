"""
SSH Client for AI Terminal Desktop
"""

import paramiko


class SSHClient:
    def __init__(self, host, username, password=None, key_file=None, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.key_file = key_file
        self.port = port
        self.client = None
        self.connected = False
        self.current_directory = None  # Track current working directory
        
    def connect(self):
        """Connect to SSH server"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if self.key_file:
                self.client.connect(
                    self.host, 
                    port=self.port, 
                    username=self.username, 
                    key_filename=self.key_file, 
                    timeout=10
                )
            else:
                self.client.connect(
                    self.host, 
                    port=self.port, 
                    username=self.username, 
                    password=self.password, 
                    timeout=10
                )
            
            self.connected = True
            
            # Get initial working directory
            try:
                stdin, stdout, stderr = self.client.exec_command('pwd')
                self.current_directory = stdout.read().decode('utf-8').strip()
            except:
                self.current_directory = None
            
            return True, "Connected successfully"
        except Exception as e:
            return False, str(e)
    
    def execute_command(self, command):
        """Execute a command on the SSH server, robustly tracking directory changes."""
        try:
            if not self.connected or not self.client:
                return False, "Not connected"

            import shlex, re
            base_dir = self.current_directory
            def split_commands(cmd):
                parts = re.split(r'(;|&&)', cmd)
                result = []
                buf = ''
                for part in parts:
                    if part in (';', '&&'):
                        if buf.strip():
                            result.append(buf.strip())
                        result.append(part)
                        buf = ''
                    else:
                        buf += part
                if buf.strip():
                    result.append(buf.strip())
                return result

            # Track directory changes for all cd commands in the chain
            last_dir = base_dir
            cmds = split_commands(command)
            only_cd = True
            import os
            for part in cmds:
                if part in (';', '&&'):
                    continue
                if part.startswith('cd '):
                    try:
                        cd_parts = shlex.split(part)
                        if len(cd_parts) >= 2:
                            cd_target = cd_parts[1]
                            if last_dir:
                                # Use shell to resolve, but also update Python-side for .. and .
                                exec_cmd = f'cd {shlex.quote(last_dir)} && cd {shlex.quote(cd_target)} && pwd'
                                stdin, stdout, stderr = self.client.exec_command(exec_cmd)
                                output = stdout.read().decode('utf-8')
                                error = stderr.read().decode('utf-8')
                                if output and not error:
                                    # Use the shell's resolved path
                                    last_dir = output.strip().splitlines()[-1]
                                else:
                                    # Fallback to Python-side path resolution
                                    last_dir = os.path.normpath(os.path.join(last_dir, cd_target))
                                    break
                            else:
                                exec_cmd = f'cd {shlex.quote(cd_target)} && pwd'
                                stdin, stdout, stderr = self.client.exec_command(exec_cmd)
                                output = stdout.read().decode('utf-8')
                                error = stderr.read().decode('utf-8')
                                if output and not error:
                                    last_dir = output.strip().splitlines()[-1]
                                else:
                                    last_dir = os.path.normpath(cd_target)
                                    break
                    except Exception:
                        pass
                else:
                    only_cd = False
            # Update tracked directory
            if last_dir:
                self.current_directory = last_dir
            # If the command is only a single cd, don't run anything else, just return the new dir
            if only_cd and len(cmds) == 1 and cmds[0].startswith('cd '):
                return True, last_dir
            # Otherwise, run the command in the latest directory
            if self.current_directory:
                full_command = f'cd {shlex.quote(self.current_directory)} && {command}'
            else:
                full_command = command
            stdin, stdout, stderr = self.client.exec_command(full_command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            result = output if output else error
            return True, result
        except Exception as e:
            return False, str(e)
    
    def get_completions(self, partial_text):
        """Get bash tab completions for partial text"""
        try:
            if not self.connected or not self.client:
                return []
            
            # Escape special characters
            escaped_text = partial_text.replace("'", "'\\''")
            
            # Use bash's compgen for completion
            if self.current_directory:
                completion_cmd = f"cd {self.current_directory} && bash -c \"compgen -f -c -- '{escaped_text}' 2>/dev/null\""
            else:
                completion_cmd = f"bash -c \"compgen -f -c -- '{escaped_text}' 2>/dev/null\""
            
            stdin, stdout, stderr = self.client.exec_command(completion_cmd)
            output = stdout.read().decode('utf-8')
            
            if output:
                completions = [line.strip() for line in output.split('\n') if line.strip()]
                return completions
            return []
        except Exception as e:
            return []
    
    def disconnect(self):
        """Disconnect from SSH server"""
        if self.client:
            self.client.close()
            self.connected = False
