$ErrorActionPreference = "Stop"

Set-Location (Join-Path $PSScriptRoot "..")

python -m pip install --user .

Write-Host "Installed SpotiTerm."
Write-Host 'Run: spotiterm "night drive"'
Write-Host "If spotiterm is not found, restart PowerShell or add Python Scripts to PATH."
