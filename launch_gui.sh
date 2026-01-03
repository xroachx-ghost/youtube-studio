#!/bin/bash
# Launch GUI Application

echo "🎬 Starting YouTube Video Generator GUI..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.6+"
    exit 1
fi

# Check PyQt5
python3 -c "import PyQt5" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing PyQt5..."
    pip3 install PyQt5
fi

# Launch
cd "$(dirname "$0")"
python3 video_generator_gui.py
