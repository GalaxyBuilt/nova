# Nova Publishing Script
# Usage: .\publish.ps1 [test|prod]

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('test','prod')]
    [string]$Target = 'test'
)

Write-Host "🚀 Nova Publishing Script" -ForegroundColor Cyan
Write-Host "Target: $Target" -ForegroundColor Yellow

# Clean previous builds
Write-Host "`n📦 Cleaning previous builds..." -ForegroundColor Green
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

# Build package
Write-Host "`n🔨 Building package..." -ForegroundColor Green
python -m build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Build successful!" -ForegroundColor Green
Write-Host "`nPackage contents:" -ForegroundColor Cyan
Get-ChildItem dist/ | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor White }

# Check package
Write-Host "`n🔍 Checking package..." -ForegroundColor Green
python -m twine check dist/*

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Package check failed!" -ForegroundColor Red
    exit 1
}

# Upload
if ($Target -eq 'test') {
    Write-Host "`n📤 Uploading to TestPyPI..." -ForegroundColor Green
    Write-Host "You can test install with:" -ForegroundColor Yellow
    Write-Host "  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ nova-scanner" -ForegroundColor White
    Write-Host ""
    python -m twine upload --repository testpypi dist/*
} else {
    Write-Host "`n📤 Uploading to PyPI..." -ForegroundColor Green
    Write-Host "After upload, install with:" -ForegroundColor Yellow
    Write-Host "  pip install nova-scanner" -ForegroundColor White
    Write-Host ""
    python -m twine upload dist/*
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Successfully published to $Target!" -ForegroundColor Green
    if ($Target -eq 'prod') {
        Write-Host "`n🎉 Nova is now live on PyPI!" -ForegroundColor Cyan
        Write-Host "View at: https://pypi.org/project/nova-scanner/" -ForegroundColor White
    } else {
        Write-Host "`nView at: https://test.pypi.org/project/nova-scanner/" -ForegroundColor White
    }
} else {
    Write-Host "`n❌ Upload failed!" -ForegroundColor Red
    exit 1
}
