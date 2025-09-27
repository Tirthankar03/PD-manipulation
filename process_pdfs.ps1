# PowerShell script to process PDF files
# Usage: .\process_pdfs.ps1 -InputDir <path_to_pdf_directory>

param(
    [Parameter(Mandatory=$true)]
    [string]$InputDir,
    
    [string]$OutputDir,
    
    [switch]$Simple,
    
    [switch]$Verbose
)

Write-Host "Processing PDFs in directory: $InputDir" -ForegroundColor Green

# Build the command
$cmd = "python pdf_processor.py --input-dir `"$InputDir`""

if ($OutputDir) {
    $cmd += " --output-dir `"$OutputDir`""
}

if ($Simple) {
    $cmd += " --simple"
}

if ($Verbose) {
    $cmd += " --verbose"
}

Write-Host "Executing: $cmd" -ForegroundColor Yellow

# Execute the command
Invoke-Expression $cmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nProcessing completed successfully!" -ForegroundColor Green
    if (-not $OutputDir) {
        Write-Host "Check the 'processed' folder in $InputDir for the modified PDFs." -ForegroundColor Cyan
    } else {
        Write-Host "Check the '$OutputDir' folder for the modified PDFs." -ForegroundColor Cyan
    }
} else {
    Write-Host "`nProcessing failed. Check the log file for details." -ForegroundColor Red
}

Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
