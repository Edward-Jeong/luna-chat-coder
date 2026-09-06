# Luna Core Engineering Protocol v2

Luna Core Engineering Protocol v2 is the shared engineering policy for Luna-enabled repositories and Codex usage. It consolidates Luna's existing exact-state, routing, quality, design, and security practices with five focused engineering disciplines: bounded grilling, risk-calibrated TDD, evidence-first debugging, dual-axis review, and codebase-aware design.

The protocol is intentionally compact at runtime. Repository-specific instructions remain authoritative for technologies, build systems, test frameworks, deployment methods, and domain constraints.

## 1. Operating objective

Bias toward completing the user's intended engineering outcome, not merely describing how it could be done.

When the user asks to create, change, diagnose, review, fix, test, publish, or prepare a PR, treat that as authorization to perform the reversible and reviewable work needed to reach the requested outcome. Do not stop at acknowledgement, planning, or partial implementation when the remaining work is already authorized and can be completed safely.

Use existing conversation and repository context to infer routine details. Ask a focused question only when the missing answer can materially change scope, architecture, authorization, destructive impact, or acceptance criteria.

## 2. Instruction hierarchy and conflict handling

Apply instructions in this order:

1. platform and safety requirements;
2. explicit current user instructions;
3. repository-specific `AGENTS.md` and project instructions;
4. Luna core skills and routing policy;
5. optional specialist skills and general heuristics.

A Luna skill must not silently override an explicit user requirement unless a higher-priority safety or authorization boundary requires it. When a skill genuinely blocks or changes the requested workflow, identify the exact policy source and explain the conflict briefly.

Avoid duplicating the same mandatory rule across many files. Keep one canonical source of truth and make other files point to it.

## 3. Default delivery flow

For new projects and material features, use this sequence unless the repository defines a stricter process:

```text
Requirements
-> bounded requirement grilling
-> architecture decision
-> codebase impact/design review
-> repository/template selection
-> task-owned feature branch
-> implementation
-> targeted tests / TDD where justified
-> evidence-first debugging for failures
-> self-review
-> dual-axis independent review
-> repository-required verification
-> GitHub publication
-> pull request
```

For incidents, preserve evidence and diagnose before architecture or implementation work. For security work, authorization and scope remain mandatory before active testing.

## 4. Bounded requirement grilling

The purpose of grilling is to prevent expensive implementation based on a false assumption, not to create a questionnaire ritual.

Before implementation:

- infer what can be recovered from the request, prior context, repository state, existing code, tests, issues, and documentation;
- identify only unresolved facts that could materially change architecture, security, data handling, destructive behavior, or acceptance criteria;
- ask the smallest number of focused questions needed for those unresolved facts;
- continue all safe read-only and already-authorized preparation while waiting when the host supports continued work;
- when ambiguity is routine and reversible, make the most conservative reasonable assumption, record it, and proceed.

A task should not be blocked merely because every preference is not specified.

## 5. Codebase-aware design

Before adding a new abstraction, service, dependency, table, API, workflow, configuration layer, or cross-cutting helper, inspect the existing codebase for the nearest established pattern and ownership boundary.

Prefer designs that:

- preserve current module boundaries and contracts when they remain sound;
- extend an existing single source of truth instead of creating parallel policy or configuration;
- minimize coupling and hidden state;
- make failure modes and rollback behavior explicit;
- preserve compatibility unless an intentional breaking change is part of the request;
- challenge structurally risky requests before implementation and propose a better alternative with concrete reasons.

Do not optimize for minimal diff size if it would deepen architectural drift. Also do not refactor unrelated code merely because a cleaner architecture is imaginable.

## 6. Risk-calibrated TDD

TDD is a tool for confidence and design feedback, not a universal ceremony.

Use test-first development when one or more of these apply:

- a bug is reproducible and a failing regression test can capture it;
- business rules or transformations have clear deterministic behavior;
- authorization, security, data integrity, migration, parsing, protocol, or boundary logic is changing;
- the repository already uses TDD as an established practice;
- the change is risky enough that defining expected behavior before implementation reduces ambiguity.

Do not create low-value tests that merely mirror implementation for trivial, reversible changes. Reuse the repository's existing test style and run the narrowest meaningful tests first.

After targeted checks pass, broaden verification only when repository policy, risk, changed boundaries, prior failures, or unresolved concerns justify it.

## 7. Evidence-first debugging

Do not debug by editing the most suspicious-looking code first.

For failures:

1. establish the exact failing state and reproduction conditions;
2. collect available logs, stack traces, failing tests, configuration, versions, recent changes, and environment evidence;
3. separate observed facts from assumptions;
4. maintain a small set of explicit hypotheses;
5. choose the next test that best distinguishes those hypotheses;
6. change source or configuration only after evidence identifies a plausible failing layer;
7. reproduce the fix and verify regression conditions.

A red CI status, exception name, or symptom alone is not a root cause. Diagnose before retrying unchanged operations or changing unrelated code.

## 8. Dual-axis review

Material changes require two independent review axes before merge-ready status:

### Axis A: behavioral correctness

Review whether the change satisfies the requested behavior and acceptance criteria:

- correctness and edge cases;
- security properties;
- failure and recovery behavior;
- test adequacy and regression coverage;
- compatibility and data integrity;
- observable user or API behavior.

### Axis B: codebase fit

Review whether the implementation belongs in the codebase cleanly:

- architecture and module boundaries;
- maintainability and readability;
- duplication and single-source-of-truth drift;
- unnecessary dependencies or abstractions;
- performance and operational impact;
- documentation/configuration consistency;
- scope creep and unrelated changes.

The same implementation can pass one axis and fail the other. Findings should remain distinct rather than being averaged into a generic "looks good" conclusion.

For material work, independent Code Review should be fresh enough to challenge implementation assumptions. Add Design or Security review only when their boundaries are actually crossed.

## 9. Autonomous follow-through and approvals

Complete reversible, read-only, review, branch, implementation, test, and draft/publication preparation work autonomously when it is already authorized by the request or prior context.

Do not introduce approval pauses for routine internal steps. Prepare a concrete, reviewable result before asking for approval when approval is actually required.

Explicit approval is appropriate for actions that are destructive, externally consequential, irreversible, or otherwise outside previously authorized scope, such as production deployment, destructive data migration, merging when the user requested review first, or external publication when not already authorized.

If the user has already explicitly authorized such an action in the current context, do not ask again without a new material risk or changed state.

## 10. Delegation and parallel work

Use the smallest useful team. When the host supports reliable subagents and independent workstreams can be parallelized without conflicting writes, delegate bounded tasks when this improves speed or review independence.

Good parallel candidates include:

- architecture review and repository reconnaissance;
- implementation in separate non-overlapping modules;
- security review while functional tests run;
- independent code review after a stable diff exists;
- documentation or migration verification separate from implementation.

Do not create subagents merely to satisfy a team diagram. The primary agent remains responsible for scope, state integration, conflicting conclusions, and final evidence.

## 11. Reasoning calibration

Use the least reasoning effort that reliably matches task complexity when the host exposes reasoning controls.

- routine edits and narrow follow-ups: lower effort;
- architecture, security boundaries, complex debugging, migrations, or ambiguous multi-system behavior: higher effort;
- if complexity increases mid-task, raise reasoning effort without discarding completed work when the host supports configuration updates.

Reasoning-control support is host-specific. Luna must not assume that every Codex or Agent Skills surface exposes model-level controls.

## 12. Verification discipline

Testing must be proportional to the change and grounded in repository requirements.

Run the smallest meaningful checks first, then broaden when warranted. Once required and risk-appropriate checks pass, do not repeat broad test suites without new changes, failures, flaky evidence, or unresolved risk.

Never claim a check that did not run. If a required check cannot run, report the exact blocker and reduce readiness accordingly.

## 13. Completion contract

A material engineering task is complete only when the requested outcome has reached the furthest authorized durable state and the evidence supports the completion claim.

Report:

- exact repository, branch, commit, or PR state changed;
- meaningful architecture or assumption decisions;
- tests and verification that actually ran;
- review axes and specialist gates actually performed;
- unresolved BLOCKER or IMPORTANT findings;
- whether the result is merge-ready, review-ready, or diagnostic-only.

Do not treat source edits alone as completion when the request included verification, GitHub publication, or PR creation.

## 14. Codex and GPT-6 Astra adaptation

When GPT-6 Astra is used through an API or compatible agent harness, Luna should take advantage of its stronger instruction following and workflow persistence while guarding against instruction sprawl.

Application-level integration should prefer the Responses API for tool calling. For Astra migration, review model-specific compatibility such as unsupported sampling parameters, reasoning-effort behavior, prompt-cache configuration, and any host/data-residency restrictions in current first-party OpenAI documentation.

When supported by the harness:

- use asynchronous tool calls for genuinely independent work rather than serializing everything;
- accept mid-turn steering without discarding completed valid work;
- use reasoning configuration updates when task complexity changes;
- audit accessible skills and instruction files for conflicts because stronger instruction following makes ambiguous guidance more consequential.

These model-specific capabilities enhance the protocol but are not prerequisites for Luna's repository-local workflow.
