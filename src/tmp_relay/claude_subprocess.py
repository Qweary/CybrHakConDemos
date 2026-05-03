"""Subprocess plumbing for the claude CLI.

Two responsibilities:
  - claude_path()  → absolute path to the `claude` binary, or None.
  - build_args()   → the argv list for a `claude -p` invocation in
                     either JSON or streaming mode.

Both consciously avoid taking a settings object — they accept their
inputs explicitly so they can be unit-tested without environment setup.

Cross-platform note: shutil.which on Windows resolves `claude.cmd` (the
npm wrapper). On Python 3.12+, asyncio.create_subprocess_exec routes
.cmd / .bat through cmd.exe automatically. On 3.11 and earlier, exec'ing
a .cmd directly fails — Phase 8 will add a startup version check.
"""

from __future__ import annotations

import shutil


def claude_path() -> str | None:
    """Return the absolute path to the `claude` binary on PATH, or None."""
    return shutil.which('claude')


def build_args(binary: str, system: str, model: str, *, streaming: bool) -> list[str]:
    """Build the argv for `claude -p`. The user prompt is NOT included
    here — it flows over stdin (see write_user_prompt_chunked) because
    accumulated workshop context routinely exceeds ARG_MAX once a forge
    run reaches Phase 3+.

    Flags chosen here turn `claude -p` into a thin LLM completion endpoint
    rather than a full Claude-Code-as-agent invocation:

      --tools ""                strip the built-in tool set so the model
                                isn't reasoning about Read/Write/Bash/
                                WebSearch on every call. ~30k cached
                                tokens → ~3k.
      --disable-slash-commands  skip skill/slash-command resolution.
      --setting-sources ""      skip CLAUDE.md auto-discovery and hooks.
      --no-session-persistence  one-shot completion, doesn't touch saved
                                Claude Code sessions.
      --permission-mode bypass  no permission prompts.

    The SYSTEM prompt is passed via --system-prompt (bounded by the
    advisor template, well under ARG_MAX).
    """
    args = [
        binary,
        '-p',
        '--model', model,
        '--no-session-persistence',
        '--permission-mode', 'bypassPermissions',
        '--tools', '',
        '--disable-slash-commands',
        '--setting-sources', '',
    ]
    if streaming:
        # stream-json + include-partial-messages emits NDJSON content_block_delta
        # frames as the model produces them. --verbose is required by the CLI
        # when combining stream-json with --print.
        args += ['--output-format', 'stream-json',
                 '--include-partial-messages', '--verbose']
    else:
        args += ['--output-format', 'json']
    if system:
        args += ['--system-prompt', system]
    return args
