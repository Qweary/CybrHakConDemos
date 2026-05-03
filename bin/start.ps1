# bin/start.ps1 — launch the workshop relay (Windows).
#
# Picks the best Python interpreter available, ensures aiohttp is
# installed, and starts the relay. Optionally opens the launcher in
# your default browser.
#
# Interpreter preference (first that works):
#   1. uv  — fastest; treats the in-tree pyproject.toml as the source
#   2. existing .venv-e2e\  — created by previous test setup
#   3. fresh .venv\ at workshop root — created on first run
#   4. py.exe / python.exe (last resort; may fail PEP 668 on some setups)
#
# Toggles:
#   -Port N         override port 3001
#   -Bind ADDR      override 127.0.0.1 — DANGER, exposes relay on LAN
#   -NoBrowser      don't auto-open
#   -SkipChecks     skip bin\doctor.ps1
#
# Stop with Ctrl+C; the relay shuts down cleanly.

[CmdletBinding()]
param(
    [int]$Port = 3001,
    [string]$Bind = '127.0.0.1',
    [switch]$NoBrowser,
    [switch]$SkipChecks
)

$ErrorActionPreference = 'Stop'
$Workshop = Resolve-Path (Join-Path $PSScriptRoot '..')
Set-Location $Workshop

if ($Bind -ne '127.0.0.1' -and $Bind -ne 'localhost') {
    Write-Host ""
    Write-Host "WARNING: -Bind $Bind exposes the relay beyond loopback. Anyone on" -ForegroundColor Yellow
    Write-Host "  your network who can reach this host can use your claude CLI session" -ForegroundColor Yellow
    Write-Host "  for free model calls. Make sure you know who's on the network before" -ForegroundColor Yellow
    Write-Host "  proceeding. Press Ctrl+C now to abort, or wait 5s to continue." -ForegroundColor Yellow
    Write-Host ""
    Start-Sleep -Seconds 5
}

# --- Pre-flight ----------------------------------------------------------
if (-not $SkipChecks) {
    & (Join-Path $PSScriptRoot 'doctor.ps1')
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "doctor.ps1 reported failures. Fix above issues or pass -SkipChecks." -ForegroundColor Red
        exit 1
    }
}

# --- Pick interpreter ----------------------------------------------------
$python = $null
$launchVia = $null

# 1. uv preferred
if (Get-Command uv -ErrorAction SilentlyContinue) {
    Write-Host "-> Using uv (resolved via pyproject.toml)" -ForegroundColor Cyan
    $launchVia = 'uv'
}

# 2. existing .venv-e2e\
if (-not $launchVia) {
    $venvE2e = Join-Path $Workshop '.venv-e2e\Scripts\python.exe'
    if (Test-Path $venvE2e) {
        & $venvE2e -c "import aiohttp" 2>$null
        if ($LASTEXITCODE -eq 0) {
            $python = $venvE2e
            $ver = (& $python --version)
            Write-Host "-> Using existing .venv-e2e\ ($ver)" -ForegroundColor Cyan
            $launchVia = 'venv'
        }
    }
}

# 3. existing .venv\
if (-not $launchVia) {
    $venv = Join-Path $Workshop '.venv\Scripts\python.exe'
    if (Test-Path $venv) {
        & $venv -c "import aiohttp" 2>$null
        if ($LASTEXITCODE -eq 0) {
            $python = $venv
            $ver = (& $python --version)
            Write-Host "-> Using existing .venv\ ($ver)" -ForegroundColor Cyan
            $launchVia = 'venv'
        }
    }
}

# 4. system python (or create .venv\)
if (-not $launchVia) {
    $sysPython = $null
    foreach ($candidate in @('py', 'python', 'python3')) {
        if (Get-Command $candidate -ErrorAction SilentlyContinue) {
            $sysPython = $candidate
            break
        }
    }
    if (-not $sysPython) {
        Write-Host "no python found -- install Python 3.10+ from python.org" -ForegroundColor Red
        exit 1
    }
    & $sysPython -c "import aiohttp" 2>$null
    if ($LASTEXITCODE -eq 0) {
        $python = $sysPython
        $ver = (& $python --version)
        Write-Host "-> Using system python ($ver) -- has aiohttp" -ForegroundColor Cyan
        $launchVia = 'venv'
    } else {
        Write-Host "-> Creating .venv\ and installing aiohttp..." -ForegroundColor Cyan
        & $sysPython -m venv .venv
        $venv = Join-Path $Workshop '.venv\Scripts\python.exe'
        & (Join-Path $Workshop '.venv\Scripts\pip.exe') install --quiet aiohttp
        $python = $venv
        $launchVia = 'venv'
    }
}

# --- Launch --------------------------------------------------------------
$url = "http://$($Bind):$($Port)/"
Write-Host ""
Write-Host "--- Starting relay -----------------------------------------"
Write-Host "    URL:   $url"
Write-Host "    Bind:  $Bind"
Write-Host "    Port:  $Port"
Write-Host "    Quit:  Ctrl+C"
Write-Host "------------------------------------------------------------"
Write-Host ""

if (-not $NoBrowser) {
    Start-Job -ScriptBlock {
        param($u)
        Start-Sleep -Seconds 1.5
        Start-Process $u
    } -ArgumentList $url | Out-Null
}

# -Port and -Bind are honored via env-var overrides understood by
# settings.py (TMP_RELAY_PORT / TMP_RELAY_BIND).
$env:TMP_RELAY_PORT = $Port
$env:TMP_RELAY_BIND = $Bind

if ($launchVia -eq 'uv') {
    & uv run --quiet python relay.py
} else {
    & $python relay.py
}
