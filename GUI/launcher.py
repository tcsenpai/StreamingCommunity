#!/usr/bin/env python3
"""
StreamingCommunity GUI Launcher
Handles venv creation, dependency installation, and server startup.
"""

import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
GUI_DIR = PROJECT_ROOT / "GUI"
VENV_DIR = PROJECT_ROOT / ".venv"
REQUIREMENTS_ROOT = PROJECT_ROOT / "requirements.txt"
REQUIREMENTS_GUI = GUI_DIR / "requirements.txt"

# ANSI colors
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
NC = "\033[0m"


def print_header():
    print(f"{BLUE}{'='*40}{NC}")
    print(f"{BLUE}  StreamingCommunity GUI Launcher{NC}")
    print(f"{BLUE}{'='*40}{NC}")
    print()


def check_uv():
    """Check if uv is installed."""
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def create_venv(use_uv):
    """Create virtual environment if it doesn't exist."""
    if VENV_DIR.exists():
        print(f"{GREEN}✓ Virtual environment exists{NC}")
        return True
    
    print(f"{BLUE}Creating virtual environment...{NC}")
    try:
        if use_uv:
            subprocess.run(["uv", "venv", str(VENV_DIR)], check=True)
        else:
            subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
        print(f"{GREEN}✓ Virtual environment created{NC}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{RED}✗ Failed to create virtual environment: {e}{NC}")
        return False


def get_python_executable():
    """Get the Python executable from venv."""
    if sys.platform == "darwin":
        return VENV_DIR / "bin" / "python"
    return VENV_DIR / "Scripts" / "python.exe"


def install_requirements(use_uv):
    """Install requirements from both root and GUI."""
    python_exe = get_python_executable()
    
    for req_file, name in [(REQUIREMENTS_ROOT, "root"), (REQUIREMENTS_GUI, "GUI")]:
        if not req_file.exists():
            print(f"{YELLOW}⚠ {name}/requirements.txt not found, skipping{NC}")
            continue
            
        print(f"{BLUE}Installing requirements from {name}...{NC}")
        try:
            if use_uv:
                subprocess.run(["uv", "pip", "install", "-r", str(req_file)], 
                              cwd=PROJECT_ROOT, check=True)
            else:
                subprocess.run([str(python_exe), "-m", "pip", "install", "-r", str(req_file)], 
                              check=True)
            print(f"{GREEN}✓ {name} requirements installed{NC}")
        except subprocess.CalledProcessError as e:
            print(f"{RED}✗ Failed to install {name} requirements: {e}{NC}")
            return False
    return True


def start_server():
    """Start the Django server."""
    print()
    print(f"{BLUE}{'='*40}{NC}")
    print(f"{GREEN}  Starting Django server...{NC}")
    print(f"{BLUE}{'='*40}{NC}")
    print()
    print("  🌐 Opening browser at http://127.0.0.1:8462")
    print("  ⏹  Press Ctrl+C to stop the server")
    print()
    
    # Start server
    python_exe = get_python_executable()
    env = os.environ.copy()
    env["PATH"] = str(VENV_DIR / "bin") + ":" + env.get("PATH", "")
    
    server_process = subprocess.Popen(
        [str(python_exe), "manage.py", "runserver", "127.0.0.1:8462"],
        cwd=GUI_DIR,
        env=env
    )
    
    # Wait a moment then open browser
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:8462")
    
    # Wait for server
    try:
        server_process.wait()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        server_process.terminate()
        server_process.wait()


def main():
    print_header()
    
    # Check for uv
    use_uv = check_uv()
    if use_uv:
        print(f"{GREEN}✓ uv found - using for fast package management{NC}")
    else:
        print(f"{YELLOW}⚠ uv not found - using standard pip/venv{NC}")
        print(f"  (Install uv: {BLUE}https://github.com/astral-sh/uv{NC})")
    print()
    
    # Setup
    if not create_venv(use_uv):
        sys.exit(1)
    
    if not install_requirements(use_uv):
        sys.exit(1)
    
    # Start server
    start_server()


if __name__ == "__main__":
    main()
