#!/bin/bash
# EMF Chaos Engine - Quick DALL-E Image Generation
# Usage: ./quick_generate.sh [API_KEY] [slide_number|all]

echo "🎨 EMF Chaos Engine - DALL-E Slide Generator"
echo "=========================================="

# Check if API key provided
if [ $# -eq 0 ]; then
    echo "❌ Usage: $0 API_KEY [slide_number|all]"
    echo "Examples:"
    echo "  $0 sk-proj-your-key-here 3        # Generate slide 3"
    echo "  $0 sk-proj-your-key-here all      # Generate all slides"
    exit 1
fi

API_KEY="$1"
TARGET="${2:-all}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv_dalle" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv_dalle
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv_dalle/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip3 install -r requirements.txt

# Test API key first
echo "🔑 Testing API key..."
python3 emf_slide_image_generator.py --api-key "$API_KEY" --test

if [ $? -ne 0 ]; then
    echo "❌ API key test failed. Please check your key."
    exit 1
fi

# Generate images
if [ "$TARGET" = "all" ]; then
    echo "🚀 Generating all slide images..."
    python3 emf_slide_image_generator.py --api-key "$API_KEY" --all --output "EMF_Investor_Deck_Images"
else
    echo "🎯 Generating slide $TARGET..."
    python3 emf_slide_image_generator.py --api-key "$API_KEY" --slide "$TARGET" --output "EMF_Investor_Deck_Images"
fi

echo "✅ Generation complete! Check EMF_Investor_Deck_Images/ folder"
echo "📊 See generation_report.md for details"
