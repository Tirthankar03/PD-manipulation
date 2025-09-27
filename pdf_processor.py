#!/usr/bin/env python3
"""
Advanced PDF Report Title Changer

This script processes PDF files in a directory and changes "KYC Report" to "PD Report"
in the first page of each PDF file using PyMuPDF for better text replacement capabilities.

Usage:
    python pdf_processor.py --input-dir <path_to_pdf_directory>
    python pdf_processor.py -i <path_to_pdf_directory>

Example:
    python pdf_processor.py --input-dir ./PD
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional
import logging

try:
    import fitz  # PyMuPDF
    import PyPDF2
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.colors import blue
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


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def replace_text_overlay(input_path: Path, output_path: Path, old_text: str, new_text: str) -> bool:
    """
    Replace text using overlay method with perfect alignment preservation.
    
    Args:
        input_path: Path to the input PDF file
        output_path: Path to save the modified PDF file
        old_text: Text to replace
        new_text: New text to insert
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Open the PDF document
        doc = fitz.open(input_path)
        page = doc[0]
        
        # Get text blocks with detailed formatting
        blocks = page.get_text("dict")["blocks"]
        
        # Find the target text span
        target_span = None
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if old_text in span["text"]:
                            target_span = span
                            break
                    if target_span:
                        break
                if target_span:
                    break
        
        if not target_span:
            logging.info(f"Text '{old_text}' not found in {input_path.name}")
            doc.close()
            return False
        
        logging.info(f"Found '{old_text}' with font: {target_span['font']}, size: {target_span['size']}")
        
        # Create a white rectangle to cover the old text
        rect = fitz.Rect(target_span["bbox"])
        page.add_redact_annot(rect, fill=(1, 1, 1))  # White fill
        page.apply_redactions()
        
        # Insert the new text with exact positioning and formatting
        point = fitz.Point(rect.x0, rect.y1 - 2)
        page.insert_text(
            point,
            new_text,
            fontsize=target_span["size"],
            fontname=target_span["font"],
            color=hex_to_rgb("#0066cc")
        )
        
        # Save the modified document
        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(output_path)
        doc.close()
        
        logging.info(f"Successfully replaced '{old_text}' with '{new_text}' in {input_path.name}")
        return True
        
    except Exception as e:
        logging.error(f"Error processing {input_path.name}: {str(e)}")
        return False

def replace_text_direct(input_path: Path, output_path: Path, old_text: str, new_text: str) -> bool:
    """
    Replace text using direct text replacement without redaction to preserve layout.
    
    Args:
        input_path: Path to the input PDF file
        output_path: Path to save the modified PDF file
        old_text: Text to replace
        new_text: New text to insert
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Open the PDF document
        doc = fitz.open(input_path)
        page = doc[0]
        
        # Get text blocks with detailed formatting
        blocks = page.get_text("dict")["blocks"]
        
        # Find the target text span
        target_span = None
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if old_text in span["text"]:
                            target_span = span
                            break
                    if target_span:
                        break
                if target_span:
                    break
        
        if not target_span:
            logging.info(f"Text '{old_text}' not found in {input_path.name}")
            doc.close()
            return False
        
        logging.info(f"Found '{old_text}' with font: {target_span['font']}, size: {target_span['size']}")
        
        # Create a new page with the same dimensions
        new_page = doc.new_page(width=page.rect.width, height=page.rect.height)
        
        # Copy all content from original page with exact positioning
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        span_text = span["text"]
                        
                        # Replace the target text
                        if old_text in span_text:
                            span_text = span_text.replace(old_text, new_text)
                            logging.info(f"Replacing '{old_text}' with '{new_text}'")
                        
                        # Insert text with exact formatting and positioning
                        if span_text.strip():  # Only insert non-empty text
                            # Use the specified blue color for the title
                            if new_text in span_text:
                                color = hex_to_rgb("#0066cc")  # Use the specified blue color
                            else:
                                # Keep original color for other text
                                color = span.get("color", (0, 0, 0))
                                if isinstance(color, (int, float)):
                                    if color > 0:
                                        color = (0, 0, 0)  # Keep original color for non-title text
                                    else:
                                        color = (0, 0, 0)  # Black for default
                                elif not isinstance(color, (tuple, list)) or len(color) not in [1, 3, 4]:
                                    color = (0, 0, 0)  # Default to black
                            
                            # Use exact positioning from the original span
                            new_page.insert_text(
                                fitz.Point(span["bbox"][0], span["bbox"][3] - 2),
                                span_text,
                                fontsize=span["size"],
                                fontname=span["font"],
                                color=color
                            )
        
        # Replace the original page with the new one
        doc.delete_page(0)
        doc.insert_page(0, new_page)
        
        # Save the modified document
        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(output_path)
        doc.close()
        
        logging.info(f"Successfully replaced '{old_text}' with '{new_text}' in {input_path.name}")
        return True
        
    except Exception as e:
        logging.error(f"Error processing {input_path.name}: {str(e)}")
        return False

def replace_text_clean(input_path: Path, output_path: Path, old_text: str, new_text: str) -> bool:
    """
    Replace text using clean approach - draw white rectangle then overlay new text.
    
    Args:
        input_path: Path to the input PDF file
        output_path: Path to save the modified PDF file
        old_text: Text to replace
        new_text: New text to insert
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Open the PDF document
        doc = fitz.open(input_path)
        page = doc[0]
        
        # Get text blocks with detailed formatting
        blocks = page.get_text("dict")["blocks"]
        
        # Find the target text span
        target_span = None
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if old_text in span["text"]:
                            target_span = span
                            break
                    if target_span:
                        break
                if target_span:
                    break
        
        if not target_span:
            logging.info(f"Text '{old_text}' not found in {input_path.name}")
            doc.close()
            return False
        
        logging.info(f"Found '{old_text}' with font: {target_span['font']}, size: {target_span['size']}")
        
        # Draw a white rectangle to cover the old text
        bbox = target_span["bbox"]
        # Expand the rectangle to ensure complete coverage
        expanded_rect = fitz.Rect(
            bbox[0] - 3,  # Left: extend more
            bbox[1] - 3,  # Top: extend more
            bbox[2] + 3,  # Right: extend more
            bbox[3] + 3   # Bottom: extend more
        )
        
        # Draw white rectangle
        page.draw_rect(expanded_rect, color=(1, 1, 1), fill=(1, 1, 1))
        
        # Insert the new text at the exact position (moved up slightly)
        point = fitz.Point(bbox[0], bbox[3] - 5)
        page.insert_text(
            point,
            new_text,
            fontsize=target_span["size"],
            fontname=target_span["font"],
            color=hex_to_rgb("#0066cc")
        )
        
        # Save the modified document
        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(output_path)
        doc.close()
        
        logging.info(f"Successfully replaced '{old_text}' with '{new_text}' in {input_path.name}")
        return True
        
    except Exception as e:
        logging.error(f"Error processing {input_path.name}: {str(e)}")
        return False

def replace_text_minimal(input_path: Path, output_path: Path, old_text: str, new_text: str) -> bool:
    """
    Replace text using minimal approach - cover old text with white rectangle then overlay new text.
    
    Args:
        input_path: Path to the input PDF file
        output_path: Path to save the modified PDF file
        old_text: Text to replace
        new_text: New text to insert
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Open the PDF document
        doc = fitz.open(input_path)
        page = doc[0]
        
        # Get text blocks with detailed formatting
        blocks = page.get_text("dict")["blocks"]
        
        # Find the target text span
        target_span = None
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if old_text in span["text"]:
                            target_span = span
                            break
                    if target_span:
                        break
                if target_span:
                    break
        
        if not target_span:
            logging.info(f"Text '{old_text}' not found in {input_path.name}")
            doc.close()
            return False
        
        logging.info(f"Found '{old_text}' with font: {target_span['font']}, size: {target_span['size']}")
        
        # Create a larger white rectangle to ensure complete coverage of the old text
        bbox = target_span["bbox"]
        # Expand the rectangle slightly to ensure complete coverage
        expanded_rect = fitz.Rect(
            bbox[0] - 2,  # Left: extend slightly left
            bbox[1] - 2,  # Top: extend slightly up
            bbox[2] + 2,  # Right: extend slightly right
            bbox[3] + 2   # Bottom: extend slightly down
        )
        page.add_redact_annot(expanded_rect, fill=(1, 1, 1))  # White fill
        page.apply_redactions()
        
        # Insert the new text at the exact position
        point = fitz.Point(bbox[0], bbox[3] - 2)
        page.insert_text(
            point,
            new_text,
            fontsize=target_span["size"],
            fontname=target_span["font"],
            color=hex_to_rgb("#0066cc")
        )
        
        # Save the modified document
        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(output_path)
        doc.close()
        
        logging.info(f"Successfully replaced '{old_text}' with '{new_text}' in {input_path.name}")
        return True
        
    except Exception as e:
        logging.error(f"Error processing {input_path.name}: {str(e)}")
        return False

def replace_text_precise(input_path: Path, output_path: Path, old_text: str, new_text: str) -> bool:
    """
    Replace text in a PDF file using PyMuPDF with precise formatting preservation.
    
    Args:
        input_path: Path to the input PDF file
        output_path: Path to save the modified PDF file
        old_text: Text to replace
        new_text: New text to insert
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Open the PDF document
        doc = fitz.open(input_path)
        
        # Process only the first page
        page = doc[0]
        
        # Get text blocks with detailed formatting
        blocks = page.get_text("dict")["blocks"]
        
        # Find the text block containing our target text
        target_span = None
        
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if old_text in span["text"]:
                            target_span = span
                            break
                    if target_span:
                        break
                if target_span:
                    break
        
        if not target_span:
            logging.info(f"Text '{old_text}' not found in {input_path.name}")
            doc.close()
            return False
        
        logging.info(f"Found '{old_text}' with font: {target_span['font']}, size: {target_span['size']}")
        
        # Create a new page with the same dimensions
        new_page = doc.new_page(width=page.rect.width, height=page.rect.height)
        
        # Copy all content from original page with exact positioning
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        span_text = span["text"]
                        
                        # Replace the target text
                        if old_text in span_text:
                            span_text = span_text.replace(old_text, new_text)
                            logging.info(f"Replacing '{old_text}' with '{new_text}'")
                        
                        # Insert text with exact formatting and positioning
                        if span_text.strip():  # Only insert non-empty text
                            # Use the specified blue color for the title
                            if new_text in span_text:
                                color = hex_to_rgb("#0066cc")  # Use the specified blue color
                            else:
                                # Handle color conversion for other text
                                color = span.get("color", (0, 0, 0))
                                if isinstance(color, (int, float)):
                                    if color > 0:
                                        color = (0, 0, 0)  # Keep original color for non-title text
                                    else:
                                        color = (0, 0, 0)  # Black for default
                                elif not isinstance(color, (tuple, list)) or len(color) not in [1, 3, 4]:
                                    color = (0, 0, 0)  # Default to black
                            
                            # Use exact positioning from the original span
                            new_page.insert_text(
                                fitz.Point(span["bbox"][0], span["bbox"][3] - 2),
                                span_text,
                                fontsize=span["size"],
                                fontname=span["font"],
                                color=color
                            )
        
        # Replace the original page with the new one
        doc.delete_page(0)
        doc.insert_page(0, new_page)
        
        # Save the modified document
        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(output_path)
        doc.close()
        
        logging.info(f"Successfully replaced '{old_text}' with '{new_text}' in {input_path.name}")
        return True
        
    except Exception as e:
        logging.error(f"Error processing {input_path.name}: {str(e)}")
        return False


def replace_text_in_pdf(input_path: Path, output_path: Path, old_text: str, new_text: str) -> bool:
    """
    Replace text in a PDF file using PyMuPDF with better formatting preservation.
    
    Args:
        input_path: Path to the input PDF file
        output_path: Path to save the modified PDF file
        old_text: Text to replace
        new_text: New text to insert
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Open the PDF document
        doc = fitz.open(input_path)
        
        # Process only the first page
        page = doc[0]
        
        # Get detailed text information
        text_dict = page.get_text("dict")
        
        # Find the exact text instance with formatting info
        target_span = None
        for block in text_dict["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if old_text in span["text"]:
                            target_span = span
                            break
                    if target_span:
                        break
                if target_span:
                    break
        
        if not target_span:
            logging.info(f"Text '{old_text}' not found in {input_path.name}")
            doc.close()
            return False
        
        logging.info(f"Found '{old_text}' in {input_path.name} with font: {target_span['font']}, size: {target_span['size']}")
        
        # Search for the text to replace
        text_instances = page.search_for(old_text)
        
        if not text_instances:
            logging.info(f"Text '{old_text}' not found in {input_path.name}")
            doc.close()
            return False
        
        logging.info(f"Found {len(text_instances)} instances of '{old_text}' in {input_path.name}")
        
        # Replace each instance with exact formatting
        for rect in text_instances:
            # Add a white rectangle to cover the old text (exact size)
            page.add_redact_annot(rect, fill=(1, 1, 1))  # White fill
            page.apply_redactions()
            
            # Insert the new text with exact original formatting
            point = fitz.Point(rect.x0, rect.y1 - 2)  # Position at the exact location
            
            # Use the specified blue color for the title
            color = hex_to_rgb("#0066cc")  # Use the specified blue color
            
            # Use the exact font and size from the original text
            page.insert_text(
                point,
                new_text,
                fontsize=target_span["size"],
                fontname=target_span["font"],
                color=color
            )
        
        # Save the modified document
        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(output_path)
        doc.close()
        
        logging.info(f"Successfully replaced '{old_text}' with '{new_text}' in {input_path.name}")
        return True
        
    except Exception as e:
        logging.error(f"Error processing {input_path.name}: {str(e)}")
        return False


def process_pdf_simple(input_path: Path, output_path: Path) -> bool:
    """
    Simple PDF processing using PyPDF2 (fallback method).
    
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
                        
                        # Create a watermark with "PD Report"
                        from io import BytesIO
                        buffer = BytesIO()
                        c = canvas.Canvas(buffer, pagesize=letter)
                        c.setFont("Helvetica-Bold", 24)
                        c.setFillColor(blue)
                        
                        # Position the text (adjust coordinates as needed)
                        width, height = letter
                        x = 50
                        y = height - 100
                        
                        c.drawString(x, y, "PD Report")
                        c.save()
                        
                        buffer.seek(0)
                        watermark_reader = PyPDF2.PdfReader(buffer)
                        watermark_page = watermark_reader.pages[0]
                        
                        # Merge the original page with the watermark
                        page.merge_page(watermark_page)
                        logging.info(f"Added watermark to page {page_num + 1} in {input_path.name}")
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


def process_pdf(input_path: Path, output_path: Path, method: str = 'clean') -> bool:
    """
    Process a single PDF file to change "KYC Report" to "PD Report".
    
    Args:
        input_path: Path to the input PDF file
        output_path: Path to save the processed PDF file
        method: Processing method ('clean', 'minimal', 'direct', 'overlay', 'precise', 'standard', or 'simple')
        
    Returns:
        True if successful, False otherwise
    """
    if method == 'clean':
        # Try clean method first (best text coverage)
        success = replace_text_clean(input_path, output_path, "KYC Report", "PD Report")
        if success:
            return True
        else:
            logging.warning(f"Clean method failed for {input_path.name}, trying minimal method")
            method = 'minimal'
    
    if method == 'minimal':
        # Try minimal method (good layout preservation)
        success = replace_text_minimal(input_path, output_path, "KYC Report", "PD Report")
        if success:
            return True
        else:
            logging.warning(f"Minimal method failed for {input_path.name}, trying direct method")
            method = 'direct'
    
    if method == 'direct':
        # Try direct method (good layout preservation)
        success = replace_text_direct(input_path, output_path, "KYC Report", "PD Report")
        if success:
            return True
        else:
            logging.warning(f"Direct method failed for {input_path.name}, trying overlay method")
            method = 'overlay'
    
    if method == 'overlay':
        # Try overlay method (good alignment preservation)
        success = replace_text_overlay(input_path, output_path, "KYC Report", "PD Report")
        if success:
            return True
        else:
            logging.warning(f"Overlay method failed for {input_path.name}, trying precise method")
            method = 'precise'
    
    if method == 'precise':
        # Try precise method
        success = replace_text_precise(input_path, output_path, "KYC Report", "PD Report")
        if success:
            return True
        else:
            logging.warning(f"Precise method failed for {input_path.name}, trying standard method")
            method = 'standard'
    
    if method == 'standard':
        # Try standard advanced method
        success = replace_text_in_pdf(input_path, output_path, "KYC Report", "PD Report")
        if success:
            return True
        else:
            logging.warning(f"Standard method failed for {input_path.name}, trying simple method")
            method = 'simple'
    
    if method == 'simple':
        # Fallback to simple method
        return process_pdf_simple(input_path, output_path)
    
    return False


def process_directory(input_dir: Path, output_dir: Optional[Path] = None, method: str = 'clean') -> None:
    """
    Process all PDF files in the input directory.
    
    Args:
        input_dir: Directory containing PDF files to process
        output_dir: Directory to save processed files (defaults to input_dir/processed)
        method: Processing method ('clean', 'minimal', 'direct', 'overlay', 'precise', 'standard', or 'simple')
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
        
        if process_pdf(pdf_file, output_file, method):
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
  python pdf_processor.py --input-dir ./PD
  python pdf_processor.py -i /path/to/pdf/directory
  python pdf_processor.py --input-dir ./PD --output-dir ./processed_pdfs
  python pdf_processor.py --input-dir ./PD --simple
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
        '--simple',
        action='store_true',
        help='Use simple watermark method instead of advanced text replacement'
    )
    
    parser.add_argument(
        '--method',
        choices=['clean', 'minimal', 'direct', 'overlay', 'precise', 'standard', 'simple'],
        default='clean',
        help='Choose processing method: clean (best text coverage), minimal (best layout), direct (good layout), overlay (best alignment), precise (best formatting), standard (faster), or simple (watermark)'
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
        
        # Determine processing method
        if args.simple:
            method = 'simple'
        else:
            method = args.method
            
        logging.info(f"Using {method} processing method")
        
        process_directory(input_dir, output_dir, method)
        
        logging.info("PDF processing completed successfully!")
        
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
