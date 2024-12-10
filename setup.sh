#!/bin/bash

# This script will automatically set up the necessary environment and run the REV Parametrlari Dasturi program.

# Function to check for Python 3 installation
check_python() {
    if ! command -v python3 &> /dev/null
    then
        echo "Python 3 is not installed. Please install Python 3 first."
        exit 1
    else
        echo "Python 3 is installed."
    fi
}

# Function to install necessary dependencies
install_dependencies() {
    echo "Installing dependencies..."
    
    # Update package lists and install dependencies
    if [ -f "/etc/debian_version" ]; then
        # Debian/Ubuntu
        sudo apt update
        sudo apt install -y python3-pyqt5 python3-pandas sqlite3 git
    elif [ -f "/etc/arch-release" ]; then
        # Arch Linux
        sudo pacman -Syu --noconfirm
        sudo pacman -S --noconfirm python-pyqt5 python-pandas sqlite3 git
    else
        echo "Unsupported Linux distribution. Please manually install dependencies."
        exit 1
    fi
    
    echo "Dependencies installed."
}

# Function to create a virtual environment and install Python packages
setup_virtualenv() {
    if ! command -v pip &> /dev/null
    then
        echo "pip is not installed. Installing pip..."
        sudo apt install -y python3-pip
    fi
    
    echo "Setting up the virtual environment..."
    
    # Create a virtual environment (optional, can skip if not needed)
    python3 -m venv revenv
    source revenv/bin/activate
    
    # Install Python dependencies
    pip install -r requirements.txt
}

# Function to clone the repository
clone_repo() {
    echo "Cloning the repository..."
    
    # Clone the GitHub repository
    git clone https://github.com/XizmatHubRec/Frequency-recorder.git
    cd Frequency-recorder
    
    # Optionally, create a requirements.txt if not present
    if [ ! -f "requirements.txt" ]; then
        echo "pyqt5\npandas\nsqlite3" > requirements.txt
    fi
}

# Function to run the application
run_application() {
    echo "Running the application..."
    python3 main.py
}

# Main execution
check_python
install_dependencies
clone_repo
setup_virtualenv
run_application
