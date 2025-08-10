#!/bin/bash
# EMF Chaos Engine - Quick Setup Script
# Just a simple weekend project setup :)

echo "🌪️ EMF Ambient Chaos Engine - Quick Setup ⚡"
echo "Setting up virtual environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "emf_chaos_venv" ]; then
    python3 -m venv emf_chaos_venv
    echo "✅ Virtual environment created"
fi

# Activate and install dependencies
source emf_chaos_venv/bin/activate
pip3 install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To run the chaos engine:"
echo "  source emf_chaos_venv/bin/activate"
echo "  python3 emf_chaos_engine_standalone.py"
echo ""
echo "🌪️ Enjoy exploring EMF chaos patterns! ⚡"
