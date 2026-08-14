#!/usr/bin/env python3
"""
OLH PDF Watermarking Script
Adds OLH branding and GitHub link to all PDF downloads
"""

import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import HexColor
import io
import os
from pathlib import Path

def add_watermark_to_pdf(input_pdf, output_pdf, github_url="https://github.com/nathantechz/ovs"):
    """
    Add OLH watermark with GitHub link to a PDF

    Args:
        input_pdf: Path to input PDF
        output_pdf: Path to output PDF with watermark
        github_url: GitHub repository URL
    """

    # Create watermark PDF
    watermark_buffer = io.BytesIO()

    # Get first page dimensions to match
    try:
        with open(input_pdf, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            first_page = reader.pages[0]
            page_width = float(first_page.mediabox.width)
            page_height = float(first_page.mediabox.height)
    except Exception as e:
        print(f"Error reading PDF dimensions: {e}")
        page_width, page_height = 612, 792  # Default letter size

    # Create watermark with footer text
    c = canvas.Canvas(watermark_buffer, pagesize=(page_width, page_height))

    # Add subtle watermark in background
    c.setFillColor(HexColor('#f0f0f0'))
    c.setFont("Helvetica", 60)
    c.rotate(45)
    c.drawString(100, 100, "OLH")
    c.rotate(-45)

    # Add footer with GitHub link
    c.setFont("Helvetica", 9)
    c.setFillColor(HexColor('#666666'))
    footer_text = f"OLH - Optometry Learning Hub | {github_url}"

    # Draw footer line
    c.line(30, 40, page_width - 30, 40)

    # Draw footer text centered
    text_width = c.stringWidth(footer_text)
    x_position = (page_width - text_width) / 2
    c.drawString(x_position, 25, footer_text)

    # Add clickable hyperlink to GitHub
    c.linkURL(github_url, (x_position, 20, x_position + c.stringWidth(github_url), 35), relative=0)

    c.save()
    watermark_buffer.seek(0)

    # Read watermark PDF
    watermark_pdf = PyPDF2.PdfReader(watermark_buffer)
    watermark_page = watermark_pdf.pages[0]

    # Read input PDF
    with open(input_pdf, 'rb') as f:
        input_reader = PyPDF2.PdfReader(f)
        output_writer = PyPDF2.PdfWriter()

        # Apply watermark to all pages
        for page_num, page in enumerate(input_reader.pages):
            page.merge_page(watermark_page)
            output_writer.add_page(page)

        # Write output
        with open(output_pdf, 'wb') as out:
            output_writer.write(out)

    print(f"✅ Watermarked: {output_pdf}")

def process_all_pdfs(materials_dir="materials"):
    """
    Process all PDFs in materials directory

    Args:
        materials_dir: Root materials directory
    """
    materials_path = Path(materials_dir)

    if not materials_path.exists():
        print(f"❌ Materials directory not found: {materials_dir}")
        return

    pdf_count = 0

    for pdf_file in materials_path.rglob('*.pdf'):
        # Skip if already watermarked
        if 'watermarked' in pdf_file.name:
            continue

        # Create watermarked version
        watermarked_name = pdf_file.stem + '_watermarked.pdf'
        watermarked_path = pdf_file.parent / watermarked_name

        try:
            add_watermark_to_pdf(str(pdf_file), str(watermarked_path))
            pdf_count += 1
        except Exception as e:
            print(f"❌ Error processing {pdf_file}: {e}")

    print(f"\n✅ Processed {pdf_count} PDF files")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == '--process-all':
            materials_dir = sys.argv[2] if len(sys.argv) > 2 else 'materials'
            process_all_pdfs(materials_dir)
        else:
            input_pdf = sys.argv[1]
            output_pdf = sys.argv[2] if len(sys.argv) > 2 else input_pdf.replace('.pdf', '_watermarked.pdf')
            add_watermark_to_pdf(input_pdf, output_pdf)
    else:
        print("OLH PDF Watermarking Tool")
        print("\nUsage:")
        print("  python add-watermark.py <input.pdf> [output.pdf]")
        print("  python add-watermark.py --process-all [materials_dir]")
        print("\nThis script adds OLH branding and GitHub link to PDF downloads.")
