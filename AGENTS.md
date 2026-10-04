# Luna Chat Coder entry point

For material engineering work, read `docs/CORE_ENGINEERING_PROTOCOL_V2.md`. It is the canonical shared execution, review-independence, verification, approval, and readiness contract. Keep project-specific instructions alongside this entry point; preserve their technology choices, security boundaries, and stricter checks.

Load only the policy relevant to the task:

- Repository development from a disposable chat sandbox: `.agents/skills/luna-chat-coder/SKILL.md` for exact source, execution, publication, and recovery.
- Development, security assurance, or incident diagnosis: `.agents/skills/luna-agent-teams/SKILL.md` for one lead team and minimum useful specialists. Infer the route without asking the user to select a team.
- Material implementation or quality review: `.agents/skills/luna-quality-engineering/SKILL.md` for risk-appropriate quality gates.
- Material UI/frontend work: `.agents/skills/luna-design-system/SKILL.md`. Read root `DESIGN.md`; create it from `templates/DESIGN.md` for a new/material surface when missing. Refine defaults from project evidence and apply Design Review.
- Public web content intended for search discovery: `.agents/skills/luna-search-visibility/SKILL.md`. Exclude private/admin/internal/closed-network and backend/CLI-only surfaces; classify mixed routes separately. Never weaken private boundaries for discoverability.
- Explicit Luna health audit or `$doctor`: `.agents/skills/doctor/SKILL.md` on demand.

Reading a policy does not require every specialist or GitHub Actions. Use exact GitHub state, preserve unrelated work, and use the sandbox when sufficient. Each project defines its runtime, architecture, dependencies, and checks.

For template-generated UI projects, instantiate root `DESIGN.md` during setup. Existing projects do not inherit template edits automatically: use `scripts/apply-luna-policy.py` and `docs/POLICY_UPDATES.ko.md` for a reviewed update that preserves project instructions. Do not fetch or execute mutable remote policy on every task.
