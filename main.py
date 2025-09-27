#!/usr/bin/env python3
"""
PDF Report Title Changer

This script processes PDF files in a directory and changes "KYC Report" to "PD Report"
in the first page of each PDF file. The processed files are saved to an output directory.

Usage:
    python main.py --input-dir <path_to_pdf_directory>
    python main.py -i <path_to_pdf_directory>

Example:
    python main.py --input-dir ./PD
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional
import logging
from io import BytesIO

try:
    import PyPDF2
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.colors import blue
    from reportlab.lib.units import inch
except ImportError as e:
    print(f"Error: Required dependencies not installed. Please run: uv sync")
    print(f"Missing dependency: {e}")
    sys.exit(1)


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('pdf_processor.log')
        ]
    )


def find_pdf_files(directory: Path) -> List[Path]:
    """
    Find all PDF files in the given directory.
    
    Args:
        directory: Path to the directory to search
        
    Returns:
        List of Path objects for PDF files
    """
    if not directory.exists():
        raise FileNotFoundError(f"Directory {directory} does not exist")
    
    if not directory.is_dir():
        raise NotADirectoryError(f"{directory} is not a directory")
    
    pdf_files = list(directory.glob("*.pdf"))
    logging.info(f"Found {len(pdf_files)} PDF files in {directory}")
    
    return pdf_files


def create_watermark_page(text: str, font_size: int = 24) -> bytes:
    """
    Create a watermark page with the given text.
    
    Args:
        text: Text to display on the watermark
        font_size: Font size for the text
        
    Returns:
        Bytes of the watermark page
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Set font and color
    c.setFont("Helvetica-Bold", font_size)
    c.setFillColor(blue)
    
    # Get page dimensions
    width, height = letter
    
    # Position text (adjust as needed based on your PDF layout)
    x = 50  # Left margin
    y = height - 100  # Top margin
    
    c.drawString(x, y, text)
    c.save()
    
    buffer.seek(0)
    return buffer.getvalue()


def process_pdf(input_path: Path, output_path: Path) -> bool:
    """
    Process a single PDF file to change "KYC Report" to "PD Report".
    
    Args:
        input_path: Path to the input PDF file
        output_path: Path to save the processed PDF file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Read the input PDF
        with open(input_path, 'rb') as input_file:
            pdf_reader = PyPDF2.PdfReader(input_file)
            pdf_writer = PyPDF2.PdfWriter()
            
            # Process each page
            for page_num, page in enumerate(pdf_reader.pages):
                if page_num == 0:  # Only modify the first page
                    # Extract text to check if it contains "KYC Report"
                    page_text = page.extract_text()
                    
                    if "KYC Report" in page_text:
                        logging.info(f"Found 'KYC Report' in {input_path.name}, page {page_num + 1}")
                        
                        # Create a new page with modified content
                        # This is a simplified approach - for more complex PDFs, 
                        # you might need to use more advanced libraries like pdfplumber or fitz
                        
                        # For now, we'll add a watermark overlay
                        watermark_bytes = create_watermark_page("PD Report")
                        watermark_reader = PyPDF2.PdfReader(BytesIO(watermark_bytes))
                        watermark_page = watermark_reader.pages[0]
                        
                        # Merge the original page with the watermark
                        page.merge_page(watermark_page)
                        logging.info(f"Modified page {page_num + 1} in {input_path.name}")
                    else:
                        logging.info(f"No 'KYC Report' found in {input_path.name}, page {page_num + 1}")
                
                pdf_writer.add_page(page)
            
            # Write the output PDF
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            logging.info(f"Successfully processed {input_path.name} -> {output_path.name}")
            return True
            
    except Exception as e:
        logging.error(f"Error processing {input_path.name}: {str(e)}")
        return False


def process_directory(input_dir: Path, output_dir: Optional[Path] = None) -> None:
    """
    Process all PDF files in the input directory.
    
    Args:
        input_dir: Directory containing PDF files to process
        output_dir: Directory to save processed files (defaults to input_dir/processed)
    """
    if output_dir is None:
        output_dir = input_dir / "processed"
    
    # Find all PDF files
    pdf_files = find_pdf_files(input_dir)
    
    if not pdf_files:
        logging.warning(f"No PDF files found in {input_dir}")
        return
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    logging.info(f"Output directory: {output_dir}")
    
    # Process each PDF file
    successful = 0
    failed = 0
    
    for pdf_file in pdf_files:
        output_file = output_dir / pdf_file.name
        
        if process_pdf(pdf_file, output_file):
            successful += 1
        else:
            failed += 1
    
    logging.info(f"Processing complete: {successful} successful, {failed} failed")


def main():
    """Main function to handle command line arguments and process PDFs."""
    parser = argparse.ArgumentParser(
        description="Process PDF files to change 'KYC Report' to 'PD Report'",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --input-dir ./PD
  python main.py -i /path/to/pdf/directory
  python main.py --input-dir ./PD --output-dir ./processed_pdfs
        """
    )
    
    parser.add_argument(
        '--input-dir', '-i',
        type=str,
        required=True,
        help='Path to directory containing PDF files to process'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        help='Path to directory for processed PDF files (default: input_dir/processed)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Convert paths to Path objects
    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else None
    
    try:
        logging.info(f"Starting PDF processing...")
        logging.info(f"Input directory: {input_dir}")
        
        process_directory(input_dir, output_dir)
        
        logging.info("PDF processing completed successfully!")
        
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
