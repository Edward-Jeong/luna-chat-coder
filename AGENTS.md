# Luna Chat Coder entry point

When repository development is requested from a chat surface with a disposable or sandboxed code-execution environment, read `.agents/skills/luna-chat-coder/SKILL.md` before working on the repository task.

For development, security review/testing, or production troubleshooting/incident analysis, also read `.agents/skills/luna-agent-teams/SKILL.md` and route the task to the smallest relevant Luna team and specialist set.

Loading either skill is a readiness step, not a reason to use GitHub Actions or every specialist. Normal engineering work should stay in the chat sandbox work container when it is available and sufficient.

The repository itself defines its runtimes, services, dependencies, architecture, build system, and verification requirements. Luna Chat Coder supplies continuity and missing execution capability; Luna Agent Teams supplies role separation, review gates, security coverage, and evidence-driven diagnosis. Neither should substitute technologies merely because they are easier to run.

Treat exact GitHub commit and PR state as durable source truth, preserve unrelated work, and do not make access to the user's computer a dependency of the workflow.

When this repository is used as a template, keep this entry point and add the project's own engineering instructions alongside it.
