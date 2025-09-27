# PDF Report Title Changer

This project provides tools to process PDF files and change "KYC Report" to "PD Report" in the first page of each PDF file.

## Installation

Install uv package manager on Windows (copy paste this command to the powershell):
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

uv run pdf_processor.py --input-dir "provide input directory path" --method clean --verbose

E.g here: 
```bash
uv run pdf_processor.py --input-dir ./PD --method clean --verbose
```

## Dependencies

- PyMuPDF (fitz) - Advanced PDF manipulation
- PyPDF2 - PDF reading and writing
- reportlab - PDF generation and watermarking
- pdfplumber - PDF text extraction (optional)


