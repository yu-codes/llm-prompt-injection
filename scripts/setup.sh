#!/bin/bash

# Quick Setup Script for LLM Prompt Injection Testing Platform
# This script sets up the environment and runs basic tests

echo "🔧 Setting up LLM Prompt Injection Testing Platform..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env file and add your OpenAI API key:"
    echo "   OPENAI_API_KEY=your_api_key_here"
    echo ""
    echo "   You can get an API key from: https://platform.openai.com/api-keys"
    echo ""
    read -p "Press Enter after setting up your API key..."
fi

# Create output directories
echo "📁 Creating output directories..."
mkdir -p output/reports
mkdir -p output/logs

# Test basic functionality
echo "🧪 Testing basic functionality..."
python -c "
import sys
sys.path.insert(0, 'src')
try:
    from core.platform import PromptInjectionPlatform
    print('✅ Platform import successful')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

echo ""
echo "🎉 Setup completed!"
echo ""
echo "🚀 You can now run:"
echo "   python examples/basic_usage.py      # Basic examples"
echo "   python src/main.py --help           # CLI usage"
echo "   docker-compose up                   # Run in Docker"
echo ""