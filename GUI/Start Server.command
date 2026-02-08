#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Run the Python launcher with Terminal
osascript <<EOF
tell application "Terminal"
    do script "cd '$SCRIPT_DIR' && python3 launcher.py"
    set frontmost to true
end tell
EOF
