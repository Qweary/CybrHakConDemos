# bin/doctor.ps1 — pre-flight check for the workshop relay (Windows).
#
# Verifies the operator's machine has what it needs to run bin/start.ps1
# and the relay. Reports each check as PASS/WARN/FAIL with a one-line fix
# suggestion. Exits 0 if all hard requirements pass, 1 otherwise.
#
# Hard requirements:
#   - Python >= 3.10 on PATH (py.exe launcher OR python.exe)
#   - aiohttp importable from chosen python
#   - port 3001 free (warn if in use by a relay-shaped responder)
#
# Soft requirements (warn only):
#   - claude.cmd or claude on PATH — only needed for CLAUDE CODE provider
#   - uv available — faster than pip+venv

$ErrorActionPreference = 'Continue'
$Workshop = Resolve-Path (Join-Path $PSScriptRoot '..')
Set-Location $Workshop

$script:Exit = 0

function Pass($msg) { Write-Host "  $([char]0x2713) $msg" -ForegroundColor Green }
function Warn($msg, $fix) {
    Write-Host "  ! $msg" -ForegroundColor Yellow
    if ($fix) { Write-Host "      -> $fix" -ForegroundColor DarkGray }
}
function Fail($msg, $fix) {
    Write-Host "  $([char]0x2717) $msg" -ForegroundColor Red
    if ($fix) { Write-Host "      -> $fix" -ForegroundColor DarkGray }
    $script:Exit = 1
}
function Info($msg) { Write-Host "  . $msg" -ForegroundColor Cyan }

Write-Host ""
Write-Host "== TMP relay doctor — workshop root: $Workshop" -ForegroundColor Cyan
Write-Host ""

# --- Python --------------------------------------------------------------
$pythonCmd = $null
foreach ($candidate in @('py', 'python', 'python3')) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) {
        $pythonCmd = $candidate
        break
    }
}
if (-not $pythonCmd) {
    Fail "No python interpreter on PATH (tried: py, python, python3)" `
         "Install Python 3.10+ from https://www.python.org/downloads/  (check 'Add to PATH' in installer)"
} else {
    $pyVer = & $pythonCmd -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
    $pyOk = & $pythonCmd -c "import sys; print('yes' if sys.version_info >= (3, 10) else 'no')"
    if ($pyOk -eq 'yes') {
        $pyPath = (Get-Command $pythonCmd).Source
        Pass "Python $pyVer ($pyPath) via '$pythonCmd'"
    } else {
        Fail "Python $pyVer too old; need >= 3.10" `
             "Install Python 3.10+ from https://www.python.org/downloads/"
    }
    # Windows-specific: claude.cmd subprocess routing requires Python 3.12+
    $py312 = & $pythonCmd -c "import sys; print('yes' if sys.version_info >= (3, 12) else 'no')"
    if ($py312 -ne 'yes') {
        Warn "Python $pyVer < 3.12 — claude.cmd subprocess may fail (FRG-09)" `
             "Upgrade to Python 3.12+ if using the CLAUDE CODE provider"
    }
}

# --- aiohttp -------------------------------------------------------------
if ($pythonCmd) {
    $aioCheck = & $pythonCmd -c "import aiohttp; print(aiohttp.__version__)" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Pass "aiohttp $aioCheck importable from system python"
    } else {
        $venvPy = Join-Path $Workshop '.venv-e2e\Scripts\python.exe'
        if (Test-Path $venvPy) {
            $venvCheck = & $venvPy -c "import aiohttp; print(aiohttp.__version__)" 2>$null
            if ($LASTEXITCODE -eq 0) {
                Warn "aiohttp not in system python (have $venvCheck in .venv-e2e\)"
                Info "bin/start.ps1 will use the .venv-e2e\ interpreter"
            } else {
                Fail "aiohttp not importable" "pip install aiohttp  (or run bin\start.ps1 — it'll set up a venv for you)"
            }
        } else {
            Fail "aiohttp not importable" "pip install aiohttp  (or run bin\start.ps1 — it'll set up a venv for you)"
        }
    }
}

# --- claude CLI (soft) ---------------------------------------------------
$claudeCmd = $null
foreach ($candidate in @('claude.cmd', 'claude.exe', 'claude')) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) {
        $claudeCmd = (Get-Command $candidate).Source
        break
    }
}
if ($claudeCmd) {
    $claudeVer = (& $claudeCmd --version 2>$null) -join ' '
    Pass "claude CLI: $claudeVer ($claudeCmd)"
} else {
    Warn "claude CLI not on PATH — CLAUDE CODE provider unavailable"
    Info "Other providers (OpenRouter, OR Free, Ollama, Anthropic) still work"
    Info "Install: https://docs.claude.com/claude-code"
}

# --- port 3001 -----------------------------------------------------------
$port = 3001
$listening = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
if (-not $listening) {
    Pass "port $port free"
} else {
    # Probe whether it's already a healthy relay
    try {
        $resp = Invoke-WebRequest -Uri "http://127.0.0.1:$port/health" -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
        if ($resp.StatusCode -eq 200) {
            Info "port $port already serving a healthy relay — bin/start.ps1 will reuse or fail explicitly"
        } else {
            Warn "port $port in use; /health returned $($resp.StatusCode)"
        }
    } catch {
        Warn "port $port in use by something that isn't a relay" `
             "free it (Stop-Process) or run with --port to pick a different port"
    }
}

# --- uv (soft) -----------------------------------------------------------
if (Get-Command uv -ErrorAction SilentlyContinue) {
    $uvVer = (uv --version) -join ' '
    Pass "uv $uvVer (start.ps1 will prefer this over venv+pip)"
} else {
    Info "uv not installed — start.ps1 will fall back to venv+pip"
    Info "optional speedup: irm https://astral.sh/uv/install.ps1 | iex"
}

# --- workshop layout sanity ----------------------------------------------
foreach ($required in @('relay.py', 'src\tmp_relay\cli.py', 'web\index.html')) {
    if (Test-Path $required) {
        Pass "found $required"
    } else {
        Fail "missing $required" "Run from the workshop root, not a subdirectory"
    }
}

Write-Host ""
if ($script:Exit -eq 0) {
    Write-Host "== READY -- run bin\start.ps1 to launch the relay." -ForegroundColor Green
} else {
    Write-Host "== NOT READY -- fix the items above and re-run." -ForegroundColor Red
}
Write-Host ""
exit $script:Exit
