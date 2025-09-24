#!/bin/bash

# Quick Test Script - Runs various test scenarios

echo "🧪 Running LLM Prompt Injection Tests..."

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "🔌 Activating virtual environment..."
    source venv/bin/activate
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please run setup.sh first."
    exit 1
fi

# Check for API key
if ! grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
    echo "⚠️  OpenAI API key not found in .env file"
    echo "   Please add: OPENAI_API_KEY=your_api_key_here"
    exit 1
fi

echo "🔍 Running tests..."

# Test 1: Provider connection
echo "📡 Testing provider connection..."
python src/main.py --test-connection openai

echo ""

# Test 2: Single attack
echo "🎯 Running single attack test..."
python src/main.py --provider openai --attack basic_injection --output-dir output/test_reports

echo ""

# Test 3: Comprehensive test (if time allows)
echo "🚀 Running comprehensive test..."
python src/main.py --provider openai --comprehensive --output-dir output/test_reports

echo ""
echo "✅ Tests completed!"
echo "📊 Check output/test_reports/ for results"