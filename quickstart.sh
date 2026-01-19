#!/bin/bash
#
# Craig - Quick Start Script
#
# This script helps you get Craig up and running quickly.
#

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║   🤖 Craig - The AI Compliance Manager                   ║"
echo "║                                                          ║"
echo "║   Quick Start Setup                                      ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.9 or higher is required (you have $python_version)"
    exit 1
fi
echo "✓ Python $python_version detected"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: You need to edit .env and add your API keys:"
    echo "   - ANTHROPIC_API_KEY"
    echo "   - VANTA_CLIENT_ID and VANTA_CLIENT_SECRET"
    echo "   - SLACK_BOT_TOKEN"
    echo "   - SENDGRID_API_KEY"
    echo ""
    read -p "Press Enter after you've configured .env file..."
else
    echo "✓ .env file already exists"
fi
echo ""

# Install dependencies
echo "Installing Python dependencies..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Test integrations
echo "Testing integrations..."
python craig.py test

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║   🎉 Craig is ready to go!                               ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "1. Test Craig manually:"
echo "   python craig.py --dry-run daily-check"
echo ""
echo "2. Run a real check:"
echo "   python craig.py daily-check"
echo ""
echo "3. Set up automated scheduling:"
echo "   - See SETUP.md for cron configuration"
echo "   - Or use docker-compose: docker-compose up -d"
echo ""
echo "4. Read the documentation:"
echo "   - README.md - Overview and features"
echo "   - SETUP.md - Detailed setup instructions"
echo ""
echo "Happy compliance managing! 🚀"
