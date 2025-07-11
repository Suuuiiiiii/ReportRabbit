
echo "🔧 Setting up ReportRabbit..."

echo "📦 Installing Python requirements..."
pip install -r requirements.txt

echo "🎭 Installing Playwright browsers..."
playwright install

if ! command -v windscribe &> /dev/null; then
    echo "⚠️  Windscribe CLI not found. Install it manually from https://windscribe.com/guides/linux"
else
    echo "✅ Windscribe found."
fi

echo "✅ Setup complete. You can now run the tool with:"
echo "   python3 main.py"
