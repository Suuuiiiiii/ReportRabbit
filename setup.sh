#!/bin/bash
set -e

echo "🔧 Installing system dependencies..."
sudo apt update
sudo apt install -y python3-venv python3-pip

echo "🐍 Creating virtual environment..."
python3 -m venv venv

echo "🔄 Activating venv and installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install

echo "✅ Setup complete! Run like this:"
echo "   source venv/bin/activate"
echo "   python main.py --target <username> --cycles <number>"
