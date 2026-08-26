# Luna Chat Coder entry point

When repository development is requested from a chat surface with a disposable or sandboxed code-execution environment, read `.agents/skills/luna-chat-coder/SKILL.md` before working on the repository task.

For development, security review/testing, or production troubleshooting/incident analysis, also read `.agents/skills/luna-agent-teams/SKILL.md`. Apply Luna Router automatically: infer the lead team and minimum specialists from the user's natural-language intent, current system state, dominant risk, and requested outcome. Do not ask the user to select a team when the route is inferable.

For material repository work, also apply `.agents/skills/luna-quality-engineering/SKILL.md`. The Quality Engineering Layer selects the minimum useful quality gates for the task: requirement validation, multi-lens review, self-review, fresh-eyes review, SSOT audit, clean rebuild evaluation, factual verification, and project catch-up. Do not run every gate mechanically.

For work that materially creates or changes a user interface, frontend layout, visual component system, dashboard, form workflow, styling system, accessibility behavior, or data presentation, also read `.agents/skills/luna-design-system/SKILL.md`. Treat repository-root `DESIGN.md` as persistent design source of truth. For a new or material UI surface, create `DESIGN.md` from `templates/DESIGN.md` when it is missing, refine it from known project evidence, read it before implementation, and apply the Design Reviewer gate before claiming merge readiness.

Loading these skills is a readiness step, not a reason to use GitHub Actions or every specialist. Normal engineering work should stay in the chat sandbox work container when it is available and sufficient. UI routing must remain conditional; do not burden backend-only, CLI-only, infrastructure, or unrelated incident work with design steps.

The repository itself defines its runtimes, services, dependencies, architecture, build system, verification requirements, and established UI implementation conventions. Luna Chat Coder supplies continuity and missing execution capability; Luna Agent Teams supplies automatic routing and role separation; Luna Quality Engineering supplies evidence-driven quality gates; Luna Design System supplies persistent visual intent and UI review. None should substitute technologies merely because they are easier to run.

Treat exact GitHub commit and PR state as durable source truth, preserve unrelated work, and do not make access to the user's computer a dependency of the workflow.

When this repository is used as a template, keep this entry point and add the project's own engineering instructions alongside it. If the generated project includes a UI surface, instantiate repository-root `DESIGN.md` from `templates/DESIGN.md` during initial project setup.
