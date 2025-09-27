@echo off
REM Batch script to process PDF files
REM Usage: process_pdfs.bat <input_directory>

if "%1"=="" (
    echo Usage: process_pdfs.bat ^<input_directory^>
    echo Example: process_pdfs.bat PD
    exit /b 1
)

echo Processing PDFs in directory: %1
python pdf_processor.py --input-dir "%1" --verbose

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Processing completed successfully!
    echo Check the processed folder in %1 for the modified PDFs.
) else (
    echo.
    echo Processing failed. Check the log file for details.
)

pause
