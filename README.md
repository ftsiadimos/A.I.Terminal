# 🤖 AI Terminal

A Flask-based web UI that combines a terminal interface with Ollama AI and SSH capabilities, allowing you to run commands on remote servers with AI-assisted command generation.

## Features

- **Web-based Terminal UI**: Modern, dark-themed terminal interface
- **Ollama Integration**: Generate commands and get assistance using local Ollama AI models
- **SSH Support**: Connect to and execute commands on remote servers
- **Real-time Communication**: WebSocket-based real-time updates
- **AI Command Generation**: Describe what you want to do, and the AI generates the command
- **Multi-tab Interface**: Switch between terminal and AI chat modes

## Prerequisites

- Python 3.7+
- Ollama running locally (http://localhost:11434)
- SSH access to target servers (optional)

## Installation

1. Clone the repository:
```bash
cd /home/fotis/gitea-repo/aiterminal
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example environment file:
```bash
cp .env.example .env
```

5. Edit `.env` with your settings:
```bash
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
SECRET_KEY=your-secure-secret-key
```

## Usage

### Starting the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Connecting to SSH Servers

1. Fill in the SSH connection form in the sidebar:
   - Host: The server address
   - Port: SSH port (default 22)
   - Username: SSH username
   - Password: SSH password (or leave empty if using key)
   - Key File: Path to SSH private key (optional)

2. Click "Connect SSH"

### Running Commands

**Direct Commands**: Type a command directly in the terminal tab and press Enter

**AI-Generated Commands**: Use any of these formats:
- `help: list all files recursively` - AI generates the command
- `generate: count lines in all Python files` - AI generates the command
- Any text ending with `?` - AI will interpret as a request

### AI Chat

Switch to the "AI Chat" tab to have a conversation with the AI about any topic or get command help.

## Architecture

### Backend (Flask)

- **app.py**: Main Flask application with SocketIO for real-time communication
- **OllamaClient**: Interface to local Ollama instance
- **SSHClient**: Wrapper around Paramiko for SSH connections
- WebSocket endpoints for command execution and AI responses

### Frontend

- **HTML/CSS/JS**: Terminal-like UI with tab support
- **Socket.IO Client**: Real-time bidirectional communication
- **Dark Theme**: GitHub-inspired dark mode

## Configuration

### Environment Variables

- `OLLAMA_HOST`: URL to Ollama API (default: http://localhost:11434)
- `OLLAMA_MODEL`: Default Ollama model (default: llama2)
- `SECRET_KEY`: Flask secret key for sessions
- `FLASK_ENV`: Environment (development/production)
- `FLASK_DEBUG`: Enable debug mode

### Available Ollama Models

The app supports any Ollama model. Popular options:
- `llama2` - General purpose
- `mistral` - Fast and efficient
- `neural-chat` - Optimized for chat
- `orca-mini` - Smaller model
- `dolphin-mixtral` - High quality

## API Endpoints

### HTTP Endpoints

- `GET /` - Main UI
- `GET /api/ollama/models` - List available Ollama models
- `POST /api/ollama/generate` - Generate response from Ollama

### WebSocket Events

**Client → Server:**
- `ssh_connect`: Connect to SSH server
- `ssh_command`: Execute command on SSH server
- `ollama_prompt`: Send prompt to Ollama
- `ollama_command_generation`: Generate command from description

**Server → Client:**
- `connection_response`: Connection established
- `ssh_status`: SSH connection status
- `command_output`: Output from executed command
- `ai_response`: Response from Ollama prompt
- `generated_command`: Generated command from AI

## Security Notes

⚠️ **Important for Production:**

1. Change the `SECRET_KEY` in `.env`
2. Use SSH keys instead of passwords
3. Run behind a reverse proxy (nginx, Apache)
4. Enable HTTPS/WSS
5. Implement authentication/authorization
6. Restrict CORS origins
7. Validate all user inputs
8. Run with limited filesystem permissions
9. Use firewall rules to restrict access
10. Monitor and log all executed commands

## Troubleshooting

### Ollama Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Pull a model if needed
ollama pull llama2
```

### SSH Connection Fails

- Verify SSH server is running: `ssh -v user@host`
- Check credentials and port
- Ensure key file has correct permissions: `chmod 600 ~/.ssh/id_rsa`
- Check if key authentication is enabled on server

### WebSocket Connection Issues

- Check browser console for errors
- Verify Flask is running with SocketIO support
- Check firewall rules
- Ensure eventlet is installed: `pip install eventlet`

## Development

### Running in Development Mode

```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

### Testing SSH Connection Locally

```bash
# Create a test user
sudo useradd -m testuser
sudo passwd testuser

# Use localhost in the SSH form
```

## License

MIT

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Future Enhancements

- [ ] Command history
- [ ] Syntax highlighting for code
- [ ] Multiple SSH sessions
- [ ] File transfer via SFTP
- [ ] Session recording
- [ ] User authentication
- [ ] Command scheduling
- [ ] Output filtering/search
- [ ] Custom prompt engineering
- [ ] Integration with other LLMs

## Support

For issues and questions, please use the GitHub issues page.
