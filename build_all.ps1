Set-Location $PSScriptRoot

$srcDir = ".\src"
$distDir = ".\dist"

# Delete old files
if (Test-Path $distDir) { Remove-Item -Recurse -Force $distDir }

# Get all Python files
$pyFiles = Get-ChildItem -Path $srcDir -Filter "*.py" -Recurse

# Build all .exe files
foreach ($file in $pyFiles) {
    $relativeDir = $file.DirectoryName.Replace((Get-Item $srcDir).FullName, "")
    $targetDist = Join-Path $distDir $relativeDir

    Write-Host "--- Building: $($file.Name) ---" -ForegroundColor Cyan

    # You potentially must first install pyinstaller: "pip install pyinstaller"
    # Also command might fail cause Windows garbage PATH handling - maybe add "py -m"
    pyinstaller --onefile --clean `
                --distpath "$targetDist" `
                --workpath ".\build\temp" `
                --specpath ".\build\specs" `
                $file.FullName
}

Write-Host "Build Complete!" -ForegroundColor Green