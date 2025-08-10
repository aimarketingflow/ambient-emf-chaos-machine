#!/usr/bin/env python3
"""
PDF Guide Generator for EMF Chaos Engine
Converts markdown guide to professional PDF with AIMF LLC branding
"""

import markdown
import weasyprint
from pathlib import Path

def create_pdf_guide():
    """Convert markdown guide to professional PDF"""
    
    # Read the markdown content
    md_file = Path("EMF_Chaos_Engine_Guide.md")
    if not md_file.exists():
        print("❌ Guide markdown file not found!")
        return
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['tables', 'toc'])
    
    # Create professional HTML with CSS styling
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>EMF Ambient Chaos Engine - Technical Guide</title>
        <style>
            @page {{
                size: A4;
                margin: 1in;
                @top-center {{
                    content: "EMF Ambient Chaos Engine - AIMF LLC";
                    font-size: 10pt;
                    color: #666;
                }}
                @bottom-center {{
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 10pt;
                    color: #666;
                }}
            }}
            
            body {{
                font-family: 'Georgia', 'Times New Roman', serif;
                line-height: 1.6;
                color: #333;
                max-width: 100%;
                margin: 0;
                padding: 0;
            }}
            
            h1 {{
                color: #1a472a;
                border-bottom: 3px solid #2e7d32;
                padding-bottom: 10px;
                margin-top: 30px;
                page-break-before: auto;
            }}
            
            h2 {{
                color: #2e7d32;
                border-bottom: 2px solid #4caf50;
                padding-bottom: 5px;
                margin-top: 25px;
            }}
            
            h3 {{
                color: #388e3c;
                margin-top: 20px;
            }}
            
            h4 {{
                color: #4caf50;
                margin-top: 15px;
            }}
            
            code {{
                background-color: #f5f5f5;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
            }}
            
            pre {{
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                overflow-x: auto;
                margin: 15px 0;
            }}
            
            pre code {{
                background-color: transparent;
                padding: 0;
            }}
            
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
            }}
            
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            
            blockquote {{
                border-left: 4px solid #4caf50;
                margin: 15px 0;
                padding-left: 15px;
                font-style: italic;
                color: #666;
            }}
            
            .title-page {{
                text-align: center;
                page-break-after: always;
                margin-top: 100px;
            }}
            
            .title-page h1 {{
                font-size: 2.5em;
                color: #1a472a;
                margin-bottom: 20px;
                border: none;
            }}
            
            .title-page h2 {{
                font-size: 1.5em;
                color: #2e7d32;
                margin-bottom: 40px;
                border: none;
            }}
            
            .company-info {{
                margin-top: 60px;
                font-size: 1.2em;
                color: #666;
            }}
            
            .version-info {{
                margin-top: 40px;
                font-size: 1em;
                color: #888;
            }}
            
            ul, ol {{
                margin: 10px 0;
                padding-left: 30px;
            }}
            
            li {{
                margin: 5px 0;
            }}
            
            .highlight {{
                background-color: #fff3cd;
                padding: 10px;
                border-left: 4px solid #ffc107;
                margin: 15px 0;
            }}
            
            .warning {{
                background-color: #f8d7da;
                padding: 10px;
                border-left: 4px solid #dc3545;
                margin: 15px 0;
            }}
            
            .success {{
                background-color: #d4edda;
                padding: 10px;
                border-left: 4px solid #28a745;
                margin: 15px 0;
            }}
        </style>
    </head>
    <body>
        <div class="title-page">
            <h1>⚡ EMF Ambient Chaos Engine</h1>
            <h2>Technical Guide & Philosophy</h2>
            <div class="company-info">
                <strong>AIMF LLC</strong><br>
                Advanced RF Research & Development
            </div>
            <div class="version-info">
                Version 1.0<br>
                August 2025<br>
                <em>"Just a weekend project exploring EMF chaos patterns"</em>
            </div>
        </div>
        
        {html_content}
    </body>
    </html>
    """
    
    # Generate PDF
    try:
        print("🌊 Converting guide to PDF...")
        pdf_file = Path("EMF_Chaos_Engine_Guide.pdf")
        
        # Create PDF with WeasyPrint
        weasyprint.HTML(string=styled_html).write_pdf(pdf_file)
        
        print(f"✅ PDF guide created successfully: {pdf_file}")
        print(f"📄 File size: {pdf_file.stat().st_size / 1024:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        return False

if __name__ == "__main__":
    print("🎯 EMF Chaos Engine PDF Guide Generator")
    print("=" * 50)
    
    success = create_pdf_guide()
    
    if success:
        print("\n🔥 LEGENDARY PDF guide created!")
        print("📖 Your 'casual weekend project' now has professional documentation")
        print("⚡ Ready to intimidate the RF engineering world!")
    else:
        print("\n❌ PDF creation failed")
        print("💡 Check dependencies and file permissions")
