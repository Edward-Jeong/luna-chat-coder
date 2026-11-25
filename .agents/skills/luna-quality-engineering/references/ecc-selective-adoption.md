# ECC selective techniques within Luna Quality Engineering

Source of ideas: https://github.com/affaan-m/ECC (MIT License,
Copyright (c) 2026 Affaan Mustafa). This reference and audit helper are
Luna-native adaptations. ECC is not vendored or installed.

The canonical Luna Core Engineering Protocol v2 owns execution, review,
approval and readiness. Quality Engineering already owns gate selection.
Use the three refinements below only when their trigger matters.

## Change-impact evidence (before and after)

Trigger: cross-module interfaces, schema/data migrations, authentication,
public API, deployment or other nontrivial blast radius.

Before implementing:
1. State authoritative requirements and observable contracts.
2. Identify impacted callers, consumers, data, API, security boundaries,
   tests, deployment, rollback and migrations using actual repository evidence.
3. Classify claimed dependencies as observed, inferred or unverified.
4. Select minimum downstream checks and rollback/target acceptance evidence.

After implementing:
1. Compare predicted impact against the final diff; report additions and misses.
2. Confirm relevant downstream tests and contracts with executed evidence.
3. Flag unverified consumers, operational checks and rollback uncertainties.
4. Feed findings into Luna's existing dual-axis review and readiness decision.

A small mapping is sufficient: surface | predicted | actual | evidence | risk.
Do not create mandatory reports for trivial or easily reversible edits.

## Read-only MCP dependency review

Trigger: new or changed repository-local MCP configuration or package selector.

Use the optional standard-library helper:

~~~bash
python scripts/luna_mcp_audit.py --root .
python scripts/luna_mcp_audit.py --root . --config .mcp.json --fail-on-mutable
~~~

Defaults are bounded to repository-local known JSON and Codex TOML paths. A
non-default file must be specified explicitly and stay within the repository.
No commands are run, dependencies installed, MCP sessions opened, home configs
read, or credentials printed.

- pinned: exact direct npm selector for supported npx/dlx patterns; NOT
  proof of a locked transitive graph, integrity or absence of vulnerabilities.
- mutable: unversioned npm selector, version range or distribution tag.
  This is a reproducibility risk, not evidence of compromise.
- review: unsupported command, malformed configuration, symlink/path
  escape, ambiguous syntax or TOML on Python 3.10.

Use --fail-on-review only where the user or repository explicitly requires
all unassessed cases to fail CI. Security Team still owns threat findings and
risk acceptance. Do not overwrite user-level Codex config, global Git hooks,
MCP services or credentials.

## Agent evaluation design (opt-in)

Trigger: a change to Luna agent selection, model routing, skills or instruction
policy accompanied by a performance/reliability claim.

Define versioned cases before changing behavior, using the existing test suite,
the Router's recorded verified outcomes, and repository CI rather than starting
another evaluation service or database. Each case needs:
- stable ID, task category, risk, input fixture, authorization boundary;
- observable acceptance criterion and independent grader (test, rule or human);
- baseline and candidate source/model/effort plus comparable conditions;
- per-run test evidence, tokens when reported, failure classification, and
  known environmental limits;
- repeated trials or holdouts for stochastic behavior, and a predeclared
  regression threshold.

Never equate CLI exit code 0, green syntax checks, or an LLM's self-judgment
with user-outcome success. Do not claim a model is superior from one example.
No paid testing, remote agent dispatch or production execution is authorized
by this document.

## Ownership boundaries

Core Protocol remains canonical; Quality Engineering owns conditional gates;
Security Ops owns assessment scope; Luna Model Router owns model decisions and
token accounting. No ECC-wide installation, alternate router, global hooks,
80% blanket coverage quota, new memory vault, or automatic existing-project
policy migration is introduced.
