# Workshop relay on Windows — gotchas and fixes

The relay was developed on macOS/Linux and tested on Windows 11
secondhand. These are the rough edges to expect on a fresh Windows
machine. None are blockers; all have one-line fixes.

## 1. PowerShell execution policy

Default Windows policy refuses to run unsigned `.ps1` scripts. Trying
to run `bin\start.ps1` produces:

```
... cannot be loaded. The file is not digitally signed.
```

**Fix once per user:**

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

`RemoteSigned` lets locally-authored scripts run without signing while
still requiring signatures on downloaded scripts. Sane default; reverse
with `Set-ExecutionPolicy -Scope CurrentUser Default`.

## 2. Python ≥ 3.12 (only if using CLAUDE CODE provider)

The CLAUDE CODE provider spawns the `claude` CLI as an asyncio
subprocess. On Windows the CLI is `claude.cmd` (the npm shim), and
Python's `asyncio.create_subprocess_exec` only routes `.cmd` / `.bat`
through `cmd.exe` automatically as of **Python 3.12**.

On Python 3.10 or 3.11 the relay starts fine but every `claude` spawn
fails with `OSError: [WinError 193]` ("not a valid Win32 application").

**Fix:** install Python 3.12+ from python.org. The doctor script
warns about this if you're on an older version.

The other providers (ANTHROPIC, OPENROUTER, OR FREE, OLLAMA) are
unaffected — they're called directly from the browser, not through
the relay.

## 3. `claude` resolution

`shutil.which('claude')` on Windows returns `'claude.cmd'`. Both the
relay and `bin/doctor.ps1` handle this — they probe for `claude.cmd`,
`claude.exe`, and `claude` in that order.

If `claude --version` works in your terminal, the relay will find it.

## 4. Antivirus / SmartScreen warnings

Three things can trip Defender or SmartScreen on first run:

- **Inbound port 3001** — first time the relay binds, Windows Firewall
  prompts whether to allow Python through. Allow for "Private networks"
  only. The relay binds 127.0.0.1 by default so external networks aren't
  actually reachable, but Windows asks anyway.
- **Subprocess spawning** — Defender sometimes flags `python.exe`
  invoking `claude.cmd` as suspicious. Add a `python.exe` exclusion if
  CLAUDE CODE phases hang for 10+ seconds before producing output.
- **Unsigned PowerShell scripts** — see #1 above.

## 5. Path separators in lab/doc URLs

The labs and docs use forward-slash URLs (`http://localhost:3001/forge.html`),
which work in every browser regardless of OS. If you see backslashes
suggested anywhere, that's a typo — file an issue.

## 6. Long path support (rarely needed)

If you cloned to a deep directory (`C:\Users\you\Documents\…\workshop\`)
and hit `OSError: [WinError 206]` ("filename or extension is too long"),
enable long-path support:

```powershell
# As Administrator, once:
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
                 -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

Or move the workshop to a shorter path (e.g., `C:\workshop\`).

## 7. WSL alternative

If any of the above is more friction than you want, install Windows
Subsystem for Linux 2 and use the bash launcher inside it:

```powershell
wsl --install
# After reboot, inside the Ubuntu terminal:
git clone <workshop-url>
cd <workshop>
bin/start.sh
```

The relay is reachable from your Windows browser at the same
`http://localhost:3001/` address (WSL forwards the loopback by default).

## What "just works" on Windows

- DEMO MODE in any of the three demos (no install needed at all)
- All four browser-direct providers (ANTHROPIC, OPENROUTER, OR FREE, OLLAMA)
- Edge, Firefox, Chrome — same behavior across all three
- The launcher page at `http://localhost:3001/`
- Token streaming through the relay (once Python 3.12+ is installed)

## When something breaks

1. Run `bin\doctor.ps1` first — most issues surface there.
2. Check the [Claude Code Windows install docs](https://docs.claude.com/claude-code) if `claude --version` doesn't work in your terminal.
3. The other providers don't depend on the relay or the CLI — switching to OPENROUTER bypasses 90% of Windows-specific gotchas.
