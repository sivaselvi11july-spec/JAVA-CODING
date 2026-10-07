# PowerShell launcher for JavaCraft AI Chatbot
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "        JavaCraft AI: Java & OOP Chatbot Server         " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

$javac = Get-Command javac -ErrorAction SilentlyContinue
if ($javac) {
    $version = (javac -version 2>&1)
    Write-Host "Detected Java Compiler: $version" -ForegroundColor Green
} else {
    Write-Host "[WARNING] javac not found in PATH." -ForegroundColor Yellow
}

Write-Host "Starting server on http://localhost:8080 ..." -ForegroundColor Cyan
Start-Process "http://localhost:8080"
python server.py
