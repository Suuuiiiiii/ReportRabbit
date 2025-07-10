#!/bin/bash

echo "🔧 Setting up ReportRabbit..."

# Install Python deps
echo "📦 Installing Python requirements..."
pip install -r requirements.txt

# Playwright setup
echo "🎭 Installing Playwright browsers..."
playwright install

# Windscribe check
if ! command -v windscribe &> /dev/null; then
    echo "⚠️  Windscribe CLI not found. Install it manually from https://windscribe.com/guides/linux"
else
    echo "✅ Windscribe found."
fi

echo "✅ Setup complete. You can now run the tool with:"
echo "   python3 main.py"
