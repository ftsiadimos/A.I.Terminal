#!/bin/bash

# Installation script for AI Terminal Desktop on Fedora

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VERSION=$(cat "$SCRIPT_DIR/../VERSION" 2>/dev/null || echo "1.0.0")

echo "===================================="
echo "AI Terminal Desktop Installation"
echo "===================================="
echo ""

# Check if running on Fedora
if [ ! -f /etc/fedora-release ]; then
    echo "Warning: This script is designed for Fedora. Continuing anyway..."
fi

# Install runtime system dependencies (keeps installer minimal)
echo "Installing runtime system dependencies..."
sudo dnf install -y \
    gtk4 \
    libadwaita \
    python3-gobject \
    python3-paramiko \
    python3-requests \
    python3-dotenv

if [ $? -ne 0 ]; then
    echo "Error: Failed to install runtime system dependencies"
    exit 1
fi

# Optional development and build-time packages
# These are only necessary if you plan to build extensions, compile bindings, or develop locally.
read -p "Install development packages (python3-devel, gtk4-devel, gobject-introspection-devel, cairo-devel, cairo-gobject-devel, python3-cairo)? (y/N) " install_dev
if [[ "$install_dev" =~ ^[Yy]$ ]]; then
    echo "Installing development packages..."
    sudo dnf install -y \
        python3-devel \
        gtk4-devel \
        gobject-introspection-devel \
        cairo-devel \
        cairo-gobject-devel \
        python3-cairo
    if [ $? -ne 0 ]; then
        echo "Warning: Failed to install some development packages, continuing..."
    else
        echo "Development packages installed."
    fi
else
    echo "Skipping development packages. If you plan to develop or build bindings, install them later." 
fi

# Optionally install pip (if missing) and Python packages
read -p "Install pip and Python packages (paramiko, requests, python-dotenv) for user? (y/N) " install_python_pkgs
if [[ "$install_python_pkgs" =~ ^[Yy]$ ]]; then
    if ! command -v pip3 &> /dev/null; then
        echo "pip3 not found, installing pip3..."
        sudo dnf install -y python3-pip || true
    fi
    echo "Installing Python packages (user-level)..."
    pip3 install --user paramiko requests python-dotenv
    if [ $? -ne 0 ]; then
        echo "Warning: Failed to install some Python dependencies with pip, but continuing..."
    fi
else
    echo "Skipping pip/python package installation. You can install them later with: pip3 install --user paramiko requests python-dotenv"
fi

# Install additional Python packages user-level (not in venv)
echo ""
echo "Installing additional Python dependencies..."
pip3 install --user paramiko requests python-dotenv

if [ $? -ne 0 ]; then
    echo "Warning: Failed to install some Python dependencies, but continuing..."
fi

# Check if Ollama is installed
echo ""
echo "Checking for Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found. Would you like to install it? (y/n)"
    read -r install_ollama
    if [ "$install_ollama" = "y" ] || [ "$install_ollama" = "Y" ]; then
        echo "Installing Ollama..."
        curl -fsSL https://ollama.com/install.sh | sh
        
        echo "Pulling llama2 model..."
        ollama pull llama2
    fi
else
    echo "Ollama is already installed"
fi

# Make main.py executable
chmod +x main.py

# Create desktop entry
echo ""
echo "Would you like to create a desktop entry? (y/n)"
read -r create_desktop

if [ "$create_desktop" = "y" ] || [ "$create_desktop" = "Y" ]; then
    DESKTOP_FILE="$HOME/.local/share/applications/aiterminal-desktop.desktop"
    CURRENT_DIR="$(pwd)"
    
    mkdir -p "$HOME/.local/share/applications"
    
    # Install the application icon for the desktop entry
    ICON_SRC="$SCRIPT_DIR/logoaitermin.png"
    if [ -f "$ICON_SRC" ]; then
        echo "Installing application icon..."
        mkdir -p "$HOME/.local/share/icons/hicolor/scalable/apps"
        cp "$ICON_SRC" "$HOME/.local/share/icons/hicolor/scalable/apps/aiterminal-desktop.png"
        echo "Icon installed to: $HOME/.local/share/icons/hicolor/scalable/apps/aiterminal-desktop.png"
        # If xdg-icon-resource is available, register the icon (user-level)
        if command -v xdg-icon-resource &> /dev/null; then
            xdg-icon-resource install --context apps --size scalable "$ICON_SRC" aiterminal-desktop || true
            echo "Registered icon with xdg-icon-resource"
        fi
    else
        echo "Icon source not found: $ICON_SRC (skipping icon install)"
    fi

    cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=$VERSION
Type=Application
Name=AI Terminal Desktop
Comment=AI-powered terminal with SSH and Ollama
Exec=python3 $CURRENT_DIR/main.py
Icon=aiterminal-desktop
Terminal=false
Categories=System;Utility;
EOF

    chmod +x "$DESKTOP_FILE"
    echo "Desktop entry created at $DESKTOP_FILE"
fi

echo ""
echo "===================================="
echo "Installation complete!"
echo "===================================="
echo ""
echo "To run the application:"
echo "  python3 main.py"
echo ""
echo "Or if you created a desktop entry, search for 'AI Terminal Desktop' in your applications menu"
echo ""
