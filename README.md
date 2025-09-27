# PDF Report Title Changer

This project provides tools to process PDF files and change "KYC Report" to "PD Report" in the first page of each PDF file.

## Installation

Install uv package manager on Windows:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen the terminal, then run:
```bash
uv --version
```

Install project dependencies:
```bash
uv sync
```

## Usage

### Method 1: Python Script (Recommended)

Process PDFs using the clean method (best text coverage):
```bash
uv run pdf_processor.py --input-dir ./PD --method clean
```

Process PDFs using the minimal method (best layout preservation):
```bash
uv run pdf_processor.py --input-dir ./PD --method minimal
```

Process PDFs using the overlay method (best alignment preservation):
```bash
uv run pdf_processor.py --input-dir ./PD --method overlay
```

Process PDFs using the precise method (best formatting preservation):
```bash
uv run pdf_processor.py --input-dir ./PD --method precise
```

Process PDFs using the standard method (faster):
```bash
uv run pdf_processor.py --input-dir ./PD --method standard
```

Process PDFs using simple watermark method:
```bash
uv run pdf_processor.py --input-dir ./PD --method simple
```

Specify custom output directory:
```bash
uv run pdf_processor.py --input-dir ./PD --output-dir ./processed_pdfs
```

Enable verbose logging:
```bash
uv run pdf_processor.py --input-dir ./PD --verbose
```

### Method 2: Batch Script (Windows)

```cmd
process_pdfs.bat PD
```

### Method 3: PowerShell Script (Windows)

```powershell
.\process_pdfs.ps1 -InputDir "PD"
```

With custom output directory:
```powershell
.\process_pdfs.ps1 -InputDir "PD" -OutputDir "processed_pdfs"
```

## Features

- **Multiple Processing Methods**: 
  - **Clean**: Best text coverage (draws white rectangle + overlay)
  - **Minimal**: Best layout preservation (redaction + overlay)
  - **Overlay**: Best alignment preservation (redaction + exact positioning)
  - **Precise**: Best formatting preservation (recreates page with exact positioning)
  - **Standard**: Fast text replacement with redaction and overlay
  - **Simple**: Watermark overlay method (fallback)
- **Format Preservation**: Maintains original fonts, sizes, and uses specified color (#0066cc)
- **Batch Processing**: Processes all PDF files in a directory
- **Logging**: Detailed logging with optional verbose mode
- **Error Handling**: Robust error handling with automatic fallback methods
- **Cross-platform**: Works on Windows, macOS, and Linux

## Output

- Processed PDFs are saved to `input_directory/processed/` by default
- Original filenames are preserved
- Log file `pdf_processor.log` is created for debugging

## Dependencies

- PyMuPDF (fitz) - Advanced PDF manipulation
- PyPDF2 - PDF reading and writing
- reportlab - PDF generation and watermarking
- pdfplumber - PDF text extraction (optional)


