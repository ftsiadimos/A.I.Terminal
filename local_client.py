"""
Local Terminal Client for AI Terminal Desktop
Executes commands locally without SSH
"""

import subprocess
import os
import shlex


class LocalClient:
    def __init__(self):
        self.connected = True  # Always connected for local mode
        self.current_directory = os.getcwd()
        
    def connect(self):
        """Connect (always succeeds for local mode)"""
        self.current_directory = os.getcwd()
        return True, "Connected to local terminal"
    
    def execute_command(self, command):
        """Execute a command locally"""
        try:
            # Check if this is a cd command
            command_stripped = command.strip()
            if command_stripped.lower().startswith('cd '):
                # Handle cd command specially
                path = command_stripped[3:].strip()
                if not path:
                    path = os.path.expanduser('~')
                else:
                    path = os.path.expanduser(path)
                
                # Make path absolute if relative
                if not os.path.isabs(path):
                    path = os.path.join(self.current_directory, path)
                
                try:
                    os.chdir(path)
                    self.current_directory = os.getcwd()
                    return True, ""
                except FileNotFoundError:
                    return True, f"cd: {path}: No such file or directory"
                except PermissionError:
                    return True, f"cd: {path}: Permission denied"
                except Exception as e:
                    return True, f"cd: {str(e)}"
            
            # Execute other commands
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.current_directory,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Combine stdout and stderr
            output = result.stdout
            if result.stderr:
                output += result.stderr
            
            return True, output or ""
        except subprocess.TimeoutExpired:
            return False, "Command timed out (30 seconds)"
        except Exception as e:
            return False, str(e)
    
    def get_completions(self, partial_text):
        """Get bash tab completions for partial text"""
        try:
            # Escape special characters
            escaped_text = partial_text.replace("'", "'\\''")
            
            # Use bash's compgen for completion
            completion_cmd = f"bash -c \"compgen -f -c -- '{escaped_text}' 2>/dev/null\""
            
            result = subprocess.run(
                completion_cmd,
                shell=True,
                cwd=self.current_directory,
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.stdout:
                completions = [line.strip() for line in result.stdout.split('\n') if line.strip()]
                return completions
            return []
        except Exception as e:
            return []
    
    def disconnect(self):
        """Disconnect (no-op for local mode)"""
        pass
