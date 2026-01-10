"""
Configuration file for AI Terminal
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Application version (single source of truth)
try:
    _version_file = os.path.join(os.path.dirname(__file__), "VERSION")
    with open(_version_file, "r") as _f:
        _file_version = _f.read().strip()
except Exception:
    _file_version = os.environ.get("APP_VERSION", "1.0.0")

APP_VERSION = os.environ.get('APP_VERSION', _file_version)

# Flask Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True'
HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
PORT = int(os.environ.get('FLASK_PORT', 1010))

# Ollama Configuration
OLLAMA_HOST = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'llama2')
OLLAMA_TIMEOUT = int(os.environ.get('OLLAMA_TIMEOUT', 300))

# SSH Configuration
SSH_TIMEOUT = int(os.environ.get('SSH_TIMEOUT', 10))
SSH_PORT = int(os.environ.get('SSH_PORT', 22))

# SocketIO Configuration
SOCKETIO_CORS = os.environ.get('SOCKETIO_CORS', '*')

# Logging
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
