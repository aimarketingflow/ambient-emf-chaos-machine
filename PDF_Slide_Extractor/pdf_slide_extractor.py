#!/usr/bin/env python3
"""
PDF Slide Extractor Tool
Converts PDF pitch decks into individual slide images for rapid presentation generation.

Usage:
    python3 pdf_slide_extractor.py input.pdf [output_dir] [--dpi 300] [--format png]

Features:
- Extract each PDF page as high-resolution image
- Configurable DPI and format (PNG, JPG, WEBP)
- Auto-naming with slide numbers
- Batch processing support
- Image optimization for presentations
"""

import os
import sys
import argparse
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_extractor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PDFSlideExtractor:
    def __init__(self, dpi=300, format='png', quality=95):
        self.dpi = dpi
        self.format = format.lower()
        self.quality = quality
        
    def extract_slides(self, pdf_path, output_dir=None):
        """Extract all slides from PDF as individual images"""
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
            
        # Create output directory
        if output_dir is None:
            output_dir = pdf_path.parent / f"{pdf_path.stem}_slides"
        else:
            output_dir = Path(output_dir)
            
        output_dir.mkdir(exist_ok=True)
        logger.info(f"Extracting slides to: {output_dir}")
        
        # Open PDF
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        logger.info(f"Processing {total_pages} slides from {pdf_path.name}")
        
        extracted_files = []
        
        for page_num in range(total_pages):
            try:
                # Get page
                page = doc.load_page(page_num)
                
                # Create transformation matrix for DPI
                mat = fitz.Matrix(self.dpi/72, self.dpi/72)
                
                # Render page to pixmap
                pix = page.get_pixmap(matrix=mat)
                
                # Convert to PIL Image
                img_data = pix.tobytes("ppm")
                img = Image.open(io.BytesIO(img_data))
                
                # Generate filename
                slide_num = str(page_num + 1).zfill(2)
                filename = f"slide_{slide_num}.{self.format}"
                output_path = output_dir / filename
                
                # Save image
                if self.format == 'jpg' or self.format == 'jpeg':
                    img.save(output_path, 'JPEG', quality=self.quality, optimize=True)
                elif self.format == 'png':
                    img.save(output_path, 'PNG', optimize=True)
                elif self.format == 'webp':
                    img.save(output_path, 'WEBP', quality=self.quality, optimize=True)
                else:
                    img.save(output_path)
                
                extracted_files.append(output_path)
                logger.info(f"✅ Slide {page_num + 1}/{total_pages}: {filename} ({img.size[0]}x{img.size[1]})")
                
            except Exception as e:
                logger.error(f"❌ Failed to extract slide {page_num + 1}: {e}")
                continue
        
        doc.close()
        
        logger.info(f"🎯 Extraction complete! {len(extracted_files)}/{total_pages} slides extracted")
        return extracted_files
    
    def batch_extract(self, pdf_directory, output_base_dir=None):
        """Extract slides from all PDFs in a directory"""
        pdf_dir = Path(pdf_directory)
        pdf_files = list(pdf_dir.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {pdf_dir}")
            return
            
        logger.info(f"Found {len(pdf_files)} PDF files for batch processing")
        
        for pdf_file in pdf_files:
            try:
                if output_base_dir:
                    output_dir = Path(output_base_dir) / f"{pdf_file.stem}_slides"
                else:
                    output_dir = None
                    
                logger.info(f"Processing: {pdf_file.name}")
                self.extract_slides(pdf_file, output_dir)
                
            except Exception as e:
                logger.error(f"Failed to process {pdf_file.name}: {e}")
                continue

def main():
    parser = argparse.ArgumentParser(description='Extract slides from PDF pitch decks as images')
    parser.add_argument('input', help='Input PDF file or directory')
    parser.add_argument('output', nargs='?', help='Output directory (optional)')
    parser.add_argument('--dpi', type=int, default=300, help='Image resolution DPI (default: 300)')
    parser.add_argument('--format', choices=['png', 'jpg', 'jpeg', 'webp'], 
                       default='png', help='Output image format (default: png)')
    parser.add_argument('--quality', type=int, default=95, 
                       help='JPEG/WEBP quality 1-100 (default: 95)')
    parser.add_argument('--batch', action='store_true', 
                       help='Process all PDFs in input directory')
    
    args = parser.parse_args()
    
    # Create extractor
    extractor = PDFSlideExtractor(
        dpi=args.dpi,
        format=args.format,
        quality=args.quality
    )
    
    try:
        if args.batch:
            extractor.batch_extract(args.input, args.output)
        else:
            extractor.extract_slides(args.input, args.output)
            
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Add missing import
    import io
    main()
