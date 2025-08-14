#!/bin/bash
# PDF Slide Extractor - Quick Setup and Run
# Usage: ./setup_and_run.sh input.pdf [output_dir]

echo "🚀 PDF Slide Extractor - Quick Setup"
echo "=================================="

# Create virtual environment
if [ ! -d "venv_pdf_extractor" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv_pdf_extractor
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv_pdf_extractor/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip3 install -r requirements.txt

# Check if input file provided
if [ $# -eq 0 ]; then
    echo "❌ Usage: $0 input.pdf [output_dir]"
    echo "Example: $0 example-slides.pdf extracted_slides/"
    exit 1
fi

INPUT_PDF="$1"
OUTPUT_DIR="${2:-${INPUT_PDF%.*}_slides}"

echo "🎯 Processing: $INPUT_PDF"
echo "📁 Output: $OUTPUT_DIR"

# Run extractor
python3 pdf_slide_extractor.py "$INPUT_PDF" "$OUTPUT_DIR" --dpi 300 --format png

echo "✅ Extraction complete! Check $OUTPUT_DIR for slide images"
echo "💡 Use these images for rapid AI generation or presentation building"
