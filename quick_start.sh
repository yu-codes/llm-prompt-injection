#!/bin/bash

# Make scripts executable
chmod +x scripts/setup.sh
chmod +x scripts/run_tests.sh

echo "🔧 Making scripts executable..."
echo "✅ Scripts are now executable"
echo ""
echo "📋 Quick Start Guide:"
echo ""
echo "1. Setup environment:"
echo "   ./scripts/setup.sh"
echo ""
echo "2. Edit .env file with your OpenAI API key:"
echo "   OPENAI_API_KEY=your_api_key_here"
echo ""
echo "3. Run tests:"
echo "   ./scripts/run_tests.sh"
echo ""
echo "4. Or use Docker:"
echo "   docker-compose up"
echo ""
echo "5. Or run examples:"
echo "   python examples/basic_usage.py"
echo ""
echo "📖 For more options:"
echo "   python src/main.py --help"
echo ""