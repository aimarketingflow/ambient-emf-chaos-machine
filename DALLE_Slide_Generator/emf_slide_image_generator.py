#!/usr/bin/env python3
"""
EMF Chaos Engine - DALL-E Slide Image Generator
Rapid generation of investor deck slide images using OpenAI DALL-E 3

Usage:
    python3 emf_slide_image_generator.py --slide 3 --api-key YOUR_KEY
    python3 emf_slide_image_generator.py --all --api-key YOUR_KEY
"""

import os
import sys
import argparse
import requests
import json
from pathlib import Path
import time
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dalle_generation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EMFSlideImageGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/images/generations"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Slide prompts optimized for EMF Chaos Engine investor deck
        self.slide_prompts = {
            3: {
                "title": "AI-Enabled Surveillance Threat Landscape",
                "prompt": """Professional cybersecurity visualization showing urban surveillance network topology: 3D cityscape with interconnected threat layers - cell towers with glowing Stingray device overlays, Bluetooth beacon mesh networks pulsing with data collection points in electric blue, WiFi access points with expanding tracking radius indicators in red. Central smartphone in the foreground broadcasting multiple colored RF signal streams (WiFi in blue, Bluetooth in purple, cellular in green, NFC in orange, GPS in yellow). AI brain symbols floating above GitHub repositories generating new attack vectors with code streams. Heat map overlay showing surveillance density with red zones for high-threat areas. Animated data flow streams showing personal information being harvested and transmitted to corporate servers and government databases. Dark professional background with glowing network connections, electromagnetic field visualizations, and '50,000+ NEW TOOLS MONTHLY' text overlay. Professional cybersecurity infographic style with dark theme, electric blue and red accents, technical precision."""
            },
            4: {
                "title": "The Defense Gap Crisis",
                "prompt": """Professional cybersecurity infographic showing massive defense gap: Split-screen composition with 'ATTACK CAPABILITIES' on left showing exponential growth curve with AI-powered tools flooding from cloud servers, GitHub repositories spawning attack vectors, automated hacking frameworks multiplying rapidly. Right side shows 'CONSUMER DEFENSES' as nearly flat line with outdated antivirus icons, basic firewalls, and obsolete security measures. Central gap visualization as a widening chasm with '5 BILLION DEFENSELESS USERS' floating in the void. Background shows global map with red threat indicators overwhelming sparse blue defense points. Corporate logos (Google, Apple, Meta, Amazon) positioned as data collectors rather than protectors. Timeline showing 2020-2025 acceleration with AI democratization markers. Professional dark theme with red danger zones, minimal blue safe areas, and stark white gap highlighting the crisis."""
            },
            5: {
                "title": "EMF Chaos Engine Solution Architecture",
                "prompt": """Professional technical architecture diagram showing EMF Chaos Engine system: Central smartphone protected by electromagnetic shield visualization with concentric RF protection layers in golden/blue gradients. Multiple threat detection modules: Stingray detector with cellular tower analysis, Bluetooth threat scanner with device fingerprinting, WiFi security monitor with network topology mapping, RF spectrum analyzer with real-time frequency monitoring. AI-powered threat classification engine processing multiple data streams. User interface showing real-time threat alerts, protection status indicators, and security recommendations. Technical specifications overlay showing 288% range amplification, environmental modeling capabilities, and advanced signal processing. Dark professional background with electromagnetic field visualizations, circuit board patterns, and glowing data connections. Style: Professional cybersecurity architecture with technical precision, electric blue and golden accents."""
            },
            6: {
                "title": "Market Opportunity & Competitive Landscape",
                "prompt": """Professional market analysis visualization: Large pie chart showing $150B+ cybersecurity market with mobile security segment highlighted in electric blue. Competitive landscape showing traditional players (Norton, McAfee, Kaspersky) with outdated desktop-focused solutions versus EMF Chaos Engine's innovative RF-based mobile protection. Market growth trajectory from 2020-2030 with exponential mobile threat growth curve. Geographic heat map showing highest-risk markets (US, EU, Asia-Pacific) with revenue opportunity indicators. Consumer segments: Privacy advocates, corporate executives, government officials, journalists, activists - each with specific threat profiles and willingness to pay premium for protection. Investment opportunity metrics: $10M-20M valuation, projected $100M+ revenue by 2027, first-mover advantage in RF-based mobile security. Professional business presentation style with clean charts, corporate blue and gold color scheme."""
            }
        }
    
    def test_api_key(self):
        """Test if the API key is valid"""
        test_payload = {
            "model": "dall-e-3",
            "prompt": "A simple test image of a blue circle on white background",
            "n": 1,
            "size": "1024x1024",
            "quality": "standard"
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=test_payload)
            if response.status_code == 200:
                logger.info("✅ API key is valid and working!")
                return True
            else:
                logger.error(f"❌ API key test failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"❌ API key test error: {e}")
            return False
    
    def generate_slide_image(self, slide_number, output_dir="generated_images"):
        """Generate image for specific slide"""
        if slide_number not in self.slide_prompts:
            logger.error(f"❌ Slide {slide_number} not configured")
            return None
            
        slide_config = self.slide_prompts[slide_number]
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        logger.info(f"🎨 Generating Slide {slide_number}: {slide_config['title']}")
        
        payload = {
            "model": "dall-e-3",
            "prompt": slide_config["prompt"],
            "n": 1,
            "size": "1792x1024",  # 16:9 presentation format
            "quality": "hd",
            "style": "natural"
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                image_url = result['data'][0]['url']
                
                # Download the image
                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    filename = f"slide_{slide_number:02d}_{slide_config['title'].lower().replace(' ', '_')}.png"
                    filepath = output_dir / filename
                    
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    
                    logger.info(f"✅ Slide {slide_number} generated: {filepath}")
                    return filepath
                else:
                    logger.error(f"❌ Failed to download image: {img_response.status_code}")
                    return None
            else:
                logger.error(f"❌ Generation failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Generation error: {e}")
            return None
    
    def generate_all_slides(self, output_dir="generated_images"):
        """Generate all configured slide images"""
        logger.info(f"🚀 Generating all {len(self.slide_prompts)} slide images...")
        
        results = {}
        for slide_num in sorted(self.slide_prompts.keys()):
            filepath = self.generate_slide_image(slide_num, output_dir)
            results[slide_num] = filepath
            
            # Rate limiting - DALL-E has limits
            if slide_num < max(self.slide_prompts.keys()):
                logger.info("⏳ Waiting 10 seconds for rate limiting...")
                time.sleep(10)
        
        # Generate summary report
        self.generate_report(results, output_dir)
        return results
    
    def generate_report(self, results, output_dir):
        """Generate summary report of generated images"""
        report_path = Path(output_dir) / "generation_report.md"
        
        with open(report_path, 'w') as f:
            f.write(f"# EMF Chaos Engine - Slide Image Generation Report\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Generated Images\n\n")
            for slide_num, filepath in results.items():
                if filepath:
                    slide_config = self.slide_prompts[slide_num]
                    f.write(f"### Slide {slide_num}: {slide_config['title']}\n")
                    f.write(f"- **File:** `{filepath.name}`\n")
                    f.write(f"- **Status:** ✅ Generated successfully\n")
                    f.write(f"- **Size:** 1792x1024 (16:9 HD)\n\n")
                else:
                    f.write(f"### Slide {slide_num}: FAILED\n")
                    f.write(f"- **Status:** ❌ Generation failed\n\n")
            
            f.write("## Usage Instructions\n\n")
            f.write("1. Import images into your presentation software\n")
            f.write("2. Use as slide backgrounds or main visuals\n")
            f.write("3. Overlay text and branding as needed\n")
            f.write("4. Maintain 16:9 aspect ratio for best results\n")
        
        logger.info(f"📊 Generation report saved: {report_path}")

def main():
    parser = argparse.ArgumentParser(description='Generate EMF Chaos Engine investor deck slide images')
    parser.add_argument('--api-key', required=True, help='OpenAI API key')
    parser.add_argument('--slide', type=int, help='Generate specific slide number (3, 4, 5, 6)')
    parser.add_argument('--all', action='store_true', help='Generate all slide images')
    parser.add_argument('--output', default='generated_images', help='Output directory')
    parser.add_argument('--test', action='store_true', help='Test API key only')
    
    args = parser.parse_args()
    
    # Create generator
    generator = EMFSlideImageGenerator(args.api_key)
    
    if args.test:
        generator.test_api_key()
        return
    
    if not generator.test_api_key():
        logger.error("❌ API key validation failed. Cannot proceed.")
        sys.exit(1)
    
    if args.all:
        generator.generate_all_slides(args.output)
    elif args.slide:
        generator.generate_slide_image(args.slide, args.output)
    else:
        logger.error("❌ Specify --slide NUMBER or --all")
        sys.exit(1)

if __name__ == "__main__":
    main()
