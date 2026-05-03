{
  description = "TMP workshop relay — local helper that bridges browser demos to the Claude Code CLI.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        py = pkgs.python312;

        # Runtime python with aiohttp pre-installed. Used by both
        # `nix run` and the devShell.
        pyRuntime = py.withPackages (p: [ p.aiohttp ]);

        # Test python: runtime + pytest stack. Separate so we don't
        # download Playwright when only running the relay.
        pyTest = py.withPackages (p: with p; [
          aiohttp
          pytest
          pytest-playwright
          playwright
        ]);

        # Source root — the flake's working tree. The relay needs this
        # at runtime to find web/ and src/tmp_relay/. Repo root is the
        # parent of packaging/.
        repoRoot = ../.;
      in
      {
        # ── Run targets: `nix run .#relay` (or `nix run .`) ───────────
        # Spawns python3 relay.py from the source tree with aiohttp
        # already in the environment. Solves the "pip install on NixOS"
        # foot-gun. Honors TMP_RELAY_BIND / TMP_RELAY_PORT just like the
        # bare invocation would.
        apps = rec {
          relay = {
            type = "app";
            program = toString (pkgs.writeShellScript "tmp-relay-launch" ''
              cd ${repoRoot}
              exec ${pyRuntime}/bin/python3 relay.py "$@"
            '');
          };
          default = relay;
        };

        # ── Dev shell: `nix develop` ───────────────────────────────────
        # Solves the Phase 0 NixOS Playwright pain. Provides a
        # properly-wrapped chromium and points Playwright at it via
        # PLAYWRIGHT_BROWSERS_PATH / EXECUTABLE_PATH so the vendored
        # chromium-headless-shell isn't used (which dies on NixOS for
        # missing libstdc++ / libglib).
        devShells.default = pkgs.mkShell {
          packages = [
            pyTest
            pkgs.chromium
            pkgs.playwright-driver.browsers
          ];

          shellHook = ''
            # Use the nix-provided chromium for Playwright.
            export PLAYWRIGHT_BROWSERS_PATH=${pkgs.playwright-driver.browsers}
            export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true
            export PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=${pkgs.chromium}/bin/chromium

            cat <<'EOF'
╭──────────────────────────────────────────────────────────────╮
│  tmp-relay devShell                                          │
│                                                              │
│  python:    ${py.pythonVersion} (aiohttp, pytest, playwright)
│  chromium:  ${pkgs.chromium.version} (system, NOT vendored)
│                                                              │
│  Start the relay:    python3 relay.py                        │
│  Run tests:          ./run_tests.sh                          │
│  Run unit tests:     pytest tests/relay/test_relay_unit.py   │
│  Run e2e:            pytest tests/e2e/test_browser_smoke.py  │
╰──────────────────────────────────────────────────────────────╯
EOF
          '';
        };

        # Self-check: `nix flake check` will evaluate this and fail
        # noisily if the package set drifts.
        checks.devShell = self.devShells.${system}.default;
      });
}
