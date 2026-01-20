#!/bin/bash
# Simple script to set up your Anthropic API key

echo "============================================"
echo "Craig Setup - Add Your Anthropic API Key"
echo "============================================"
echo ""
echo "This script will help you configure Craig."
echo "Your API key will be stored securely in .env (not in git)."
echo ""
read -p "Enter your Anthropic API key (starts with sk-ant-): " api_key

if [[ -z "$api_key" ]]; then
    echo "❌ No key entered. Please run this script again."
    exit 1
fi

# Update the .env file
cd /home/user/craigthecompliancemanager
sed -i "s|ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=$api_key|g" .env

echo ""
echo "✅ API key configured!"
echo ""
echo "Next steps:"
echo "  1. Install dependencies: pip install -r requirements.txt"
echo "  2. Test Craig: python test_craig.py"
echo ""
