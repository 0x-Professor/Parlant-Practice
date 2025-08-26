# PowerShell script to set up Gemini environment variables
# Run this in PowerShell as: .\setup_gemini_env.ps1

Write-Host "🚀 Gemini Environment Setup for Parlant" -ForegroundColor Green
Write-Host "=" * 45

# Check if GEMINI_API_KEY is already set
if ($env:GEMINI_API_KEY) {
    $maskedKey = $env:GEMINI_API_KEY.Substring(0, 10) + "..."
    Write-Host "✅ GEMINI_API_KEY is already set: $maskedKey" -ForegroundColor Green
    
    $choice = Read-Host "Do you want to update it? (y/N)"
    if ($choice -ne 'y' -and $choice -ne 'Y') {
        Write-Host "Keeping existing API key." -ForegroundColor Yellow
    } else {
        Remove-Variable -Name GEMINI_API_KEY -Scope Global -ErrorAction SilentlyContinue
    }
}

# Get API key if not set or user wants to update
if (-not $env:GEMINI_API_KEY) {
    Write-Host ""
    Write-Host "🔑 To get your Gemini API key:" -ForegroundColor Cyan
    Write-Host "1. Visit https://makersuite.google.com/app/apikey"
    Write-Host "2. Sign in with your Google account"
    Write-Host "3. Click 'Create API Key'"
    Write-Host "4. Copy the generated key"
    Write-Host ""
    
    $apiKey = Read-Host "Enter your Gemini API key"
    
    if ($apiKey) {
        $env:GEMINI_API_KEY = $apiKey
        Write-Host "✅ API key set for current session" -ForegroundColor Green
    } else {
        Write-Host "❌ No API key provided. Exiting." -ForegroundColor Red
        exit 1
    }
}

# Model selection
Write-Host ""
Write-Host "🤖 Select Gemini Model:" -ForegroundColor Cyan
Write-Host "1. gemini-1.5-flash (Recommended - Fast & Cost-effective)"
Write-Host "2. gemini-1.5-pro (Most Capable - Higher cost)"
Write-Host "3. gemini-pro (Legacy - Older generation)"

$modelChoice = Read-Host "Select model (1-3) or press Enter for default (1)"

$models = @{
    "1" = "gemini-1.5-flash"
    "2" = "gemini-1.5-pro"
    "3" = "gemini-pro"
    ""  = "gemini-1.5-flash"
}

$selectedModel = $models[$modelChoice]
if (-not $selectedModel) {
    $selectedModel = "gemini-1.5-flash"
}

$env:GEMINI_MODEL = $selectedModel

Write-Host ""
Write-Host "✅ Environment configured!" -ForegroundColor Green
Write-Host "   API Key: $($env:GEMINI_API_KEY.Substring(0, 10))..." -ForegroundColor Gray
Write-Host "   Model: $selectedModel" -ForegroundColor Gray

Write-Host ""
Write-Host "💾 To make these settings permanent, add to your PowerShell profile:" -ForegroundColor Yellow
Write-Host "   `$env:GEMINI_API_KEY = `"$($env:GEMINI_API_KEY)`"" -ForegroundColor Gray
Write-Host "   `$env:GEMINI_MODEL = `"$selectedModel`"" -ForegroundColor Gray

Write-Host ""
Write-Host "🧪 Test your setup:" -ForegroundColor Cyan
Write-Host "   U:/Parlant-Practice/starter/.venv/Scripts/python.exe test_gemini.py"

Write-Host ""
Write-Host "🚀 Run the main application:" -ForegroundColor Cyan  
Write-Host "   U:/Parlant-Practice/starter/.venv/Scripts/python.exe main.py"

Write-Host ""
Write-Host "🎉 Setup complete! Your Gemini integration is ready." -ForegroundColor Green
