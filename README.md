# PDF Report Title Changer

This project provides tools to process PDF files and change "KYC Report" to "PD Report" in the first page of each PDF file. The script recursively processes all PDF files in a directory and its subdirectories, preserving the directory structure in the output.

## Features

- ✅ Recursive PDF processing (handles subdirectories)
- ✅ Preserves directory structure in output
- ✅ Multiple processing methods available
- ✅ Detailed logging and progress tracking
- ✅ Support for both venv and conda environments

## Setup Instructions

### Option 1: Using Python venv (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd PD_manipulation
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the project:**
   ```bash
   python main.py --input-dir "./PD" --verbose
   ```

### Option 2: Using Conda/Anaconda

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd PD_manipulation
   ```

2. **Create conda environment:**
   ```bash
   # Create new conda environment with Python 3.12
   conda create -n pd_manipulation python=3.12
   
   # Activate the environment
   conda activate pd_manipulation
   ```

3. **Install dependencies:**
   ```bash
   # Install from requirements.txt
   pip install -r requirements.txt
   
   # Or install individually:
   conda install -c conda-forge pymupdf
   pip install PyPDF2 reportlab pdfplumber
   ```

4. **Run the project:**
   ```bash
   python main.py --input-dir "./PD" --verbose
   ```

### Option 3: Using Anaconda Navigator + VSCode

1. **Open Anaconda Navigator**
2. **Create new environment:**
   - Click "Environments" tab
   - Click "Create" button
   - Name: `pd_manipulation`
   - Python version: 3.12
   - Click "Create"

3. **Open VSCode from Navigator:**
   - In the new environment, click "Open with VSCode"
   - Or open VSCode manually and select the conda environment

4. **Install dependencies in VSCode terminal:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the project:**
   ```bash
   python main.py --input-dir "./PD" --verbose
   ```

## Usage

### Basic Usage
```bash
python main.py --input-dir "./PD" --verbose
```

### Advanced Usage
```bash
# Process with specific output directory
python main.py --input-dir "./PD" --output-dir "./processed_pdfs" --verbose

# Use the advanced pdf_processor.py with different methods
python pdf_processor.py --input-dir "./PD" --method clean --verbose
```

### Command Line Options

- `--input-dir, -i`: Path to directory containing PDF files to process
- `--output-dir, -o`: Path to directory for processed PDF files (default: {input_dir}_processed)
- `--verbose, -v`: Enable verbose logging
- `--method`: Choose processing method (for pdf_processor.py only)

## Output Structure

The script creates a new directory with `_processed` suffix that mirrors the input directory structure:

```
Input: ./PD/
├── file1.pdf
├── subfolder/
│   └── file2.pdf
└── another/
    └── file3.pdf

Output: ./PD_processed/
├── file1.pdf (processed)
├── subfolder/
│   └── file2.pdf (processed)
└── another/
    └── file3.pdf (processed)
```

## Dependencies

- **PyMuPDF (fitz)** - Advanced PDF manipulation and text replacement
- **PyPDF2** - PDF reading and writing
- **reportlab** - PDF generation and watermarking
- **pdfplumber** - PDF text extraction (optional)

## Troubleshooting

### Common Issues

1. **"No module named 'PyPDF2'" error:**
   - Make sure your virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **PowerShell execution policy error:**
   - Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

3. **Conda environment not found:**
   - Make sure conda is installed and in PATH
   - Try: `conda activate pd_manipulation`

### Environment Verification

Check if your environment is set up correctly:
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Test import
python -c "import PyPDF2, fitz, reportlab; print('All dependencies installed successfully!')"
```

## Examples

```bash
# Process a single directory
python main.py --input-dir "./documents" --verbose

# Process with custom output location
python main.py --input-dir "./reports" --output-dir "./processed_reports" --verbose

# Use advanced processor with specific method
python pdf_processor.py --input-dir "./data" --method clean --verbose
```


