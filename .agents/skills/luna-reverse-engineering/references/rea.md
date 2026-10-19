# Optional REA CLI adapter

The reproducible example is in `docs/SECURITY_OPS.ko.md`. Use an existing trusted install, an absolute executable path, and its exact stable version. The adapter runs no package manager and never modifies MCP registrations. `--execute` is required to invoke the tool; a plan does not even execute `--version`.

Supported commands are fixed argument arrays with no shell evaluation:

- JavaScript: `rea analyze-javascript-application ABSOLUTE_FILE --json`
- Native: `rea inspect ABSOLUTE_FILE --provider ghidra --format json`

Execution checks the CLI version, repeats sample scope admission, captures the exit status/output, and checks the source digest again. Timeout is 30 seconds for the version probe and 360 seconds for analysis. Failures and missing providers remain explicit; never silently switch engines. On Windows choose an executable supported by Python's direct process creation; npm `.cmd` wrappers are not supported by this adapter. Use a verified POSIX environment for the current integration. Windows native/provider acceptance is still unverified here.

Scope admission requires an exact existing regular-file path and SHA-256. Directory input is intentionally excluded because hashing one file would not bind a mutable directory tree. These checks assume stable, analyst-controlled files, directories, and installations. They do not prevent concurrent replacement, malicious providers, network access by a provider, or resource exhaustion beyond the wall-clock timeout. The adapter is not a sandbox or an authenticity verifier for the executable.

Raw outputs can contain proprietary code/secrets. The adapter prints JSON to stdout and does not save it or send it to a model/service. Choose a private case directory when redirecting output; do not commit it. A successful static analysis cannot establish runtime behavior or vulnerability success.

Primary sources (recheck against the selected release):

- https://github.com/morluto/rea/blob/main/docs/installation.md
- https://github.com/morluto/rea/blob/main/docs/cli.md
- https://github.com/morluto/rea/blob/main/docs/windows-ghidra-p0.md
- https://github.com/morluto/rea/blob/main/SECURITY.md

The real JavaScript CLI acceptance attempt and host blocker are recorded for 6.7.0 in `docs/SECURITY_OPS_VALIDATION.ko.md`; this is an observed test version, not a mandatory latest-version claim or an automatic update policy.
