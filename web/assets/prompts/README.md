# Workshop Agent Prompts

Human-readable export of every system prompt embedded in the three demos.
**These files are derived artifacts**, not the runtime source — the demos
load their prompts from inline `SYS_*` / `SYS.*` JavaScript constants.
The `.md` files exist so a person (or an LLM assistant) can read a single
prompt without scanning ~165KB of HTML.

## Layout

```
forge/        — 11 prompts driving the FORGE swarm-design pipeline
  advisors/   — 4 T2 domain-advisor prompts (one per swarm vertical)
combat/       — 23 prompts for IRONCLAD + PHANTOM FEED red/blue stages
evolve/       —  4 prompts for the ARBITER → SCULPTOR → CHALLENGER → RERUN loop
```

Filename = the constant name lowercased, kebab-cased, dot-segments mapped
to subdirectories. Examples:

| Constant in HTML        | Exported as                         |
|---|---|
| `SYS.OPPENHEIMER`       | `forge/oppenheimer.md`              |
| `SYS.LATTICE_VRA`       | `forge/lattice-vra.md`              |
| `SYS.ADVISORS.NEUTRON`  | `forge/advisors/neutron.md`         |
| `SYS_RED_RECON`         | `combat/red-recon.md`               |
| `SYS_PHANTOM_BLUE_HUNT` | `combat/phantom-blue-hunt.md`       |

## Drift protection

`test_snapshots.py prompts` runs three checks:

1. **JSON snapshot vs. live HTML extraction** — fails if a prompt body
   in the demo HTML changes without `--update`.
2. **`.md` export vs. live HTML extraction** — fails if the inline
   constant and its derived `.md` file diverge.
3. **No stray `.md` files** — fails if the directory contains files
   that no constant maps to.

If you intentionally edit a prompt:

```bash
# Edit in the demo HTML (the runtime source), then:
python3 test_snapshots.py --update prompts
git add web/assets/prompts/ tests/snapshots/prompts.json web/<demo>.html
```

## Note on `${var}` placeholders

Combat and evolve prompts include JS template-literal interpolations like
`${net}`, `${redAction}`, `${prev}`. Those are preserved verbatim in the
`.md` files — when the prompt is consumed, the demo's `(args) => \`...\``
arrow function fills them in. A future fetch-loader refactor would need
a small `interpolate(template, vars)` helper.
