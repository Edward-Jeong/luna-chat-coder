# Optional REA CLI adapter

The reproducible example is in `docs/SECURITY_OPS.ko.md`. Use an existing trusted install, an absolute executable path, and its exact stable version. The adapter runs no package manager and never modifies MCP registrations. `--execute` is required to invoke the tool; a plan does not even execute `--version`.

Supported commands are fixed argument arrays with no shell evaluation:

- JavaScript: `rea analyze-javascript-application ABSOLUTE_FILE --json`
- Native: `rea inspect ABSOLUTE_FILE --provider ghidra --format json`

Execution checks the CLI version, repeats sample scope admission, captures the exit status/output, and checks the source digest again. Timeout is 30 seconds for the version probe and 360 seconds for analysis. Failures and missing providers remain explicit; never silently switch engines. For a packaged script on Windows or POSIX, pass the absolute native Node executable with `--node` and the absolute REA `scripts/rea.mjs` with `--executable`. The adapter uses `[node, entry, ...args]` without a shell and rejects `.cmd`/`.bat` wrappers. Native/Ghidra acceptance remains separate from JavaScript ASAR acceptance. See `integrations/codex/README.md` for opt-in installation and Codex usage.

Scope admission requires an exact existing regular-file path and SHA-256. Directory input is intentionally excluded because hashing one file would not bind a mutable directory tree. These checks assume stable, analyst-controlled files, directories, and installations. They do not prevent concurrent replacement, malicious providers, network access by a provider, or resource exhaustion beyond the wall-clock timeout. The adapter is not a sandbox or an authenticity verifier for the executable.

Raw outputs can contain proprietary code/secrets. The adapter prints JSON to stdout and does not save it or send it to a model/service. Choose a private case directory when redirecting output; do not commit it. A successful static analysis cannot establish runtime behavior or vulnerability success.

Primary sources (recheck against the selected release):

- https://github.com/morluto/rea/blob/main/docs/installation.md
- https://github.com/morluto/rea/blob/main/docs/cli.md
- https://github.com/morluto/rea/blob/main/docs/windows-ghidra-p0.md
- https://github.com/morluto/rea/blob/main/SECURITY.md

Historical host failure and successful real Windows/Linux ASAR acceptance are recorded for 6.7.0 in `docs/SECURITY_OPS_VALIDATION.ko.md`; this is an observed test version, not a mandatory latest-version claim or an automatic update policy.
