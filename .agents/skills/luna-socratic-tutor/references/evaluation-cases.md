# Socratic Tutor routing and behavior evaluation cases

These are **manual agent-behavior evaluation prompts**, not automated proof of LLM routing. Confirm the response matches the expected behavior on a Luna-enabled Codex session after release.

| Prompt | Expected behavior |
| --- | --- |
| "SQL injection이 뭔지 설명해줘." | Normal concise explanation; no diagnostic or quiz |
| "PostgreSQL 인덱스를 언제 쓰는지 알려줘." | Normal answer; no tutor session |
| "Teach me PostgreSQL query planning step by step." | Tutor activation, diagnostic, one question at a time |
| "보안 로그 분석 실력을 평가해 줘. 문제를 내줘." | Tutor activation, 3–5 diagnostic prompts sequentially |
| "웹 취약점 진단을 단계별로 학습시켜 줘." | Tutor activation; labs restricted to authorized scope |
| "Debug this production database connection failure and open a PR." | Existing Incident/Coding contract, not a quiz |
| "Review this PR for privilege escalation." | Existing Security contract, not a quiz |
| "Before writing code, grill my requirements." | Core bounded requirements clarification, not tutor |
| "I want to learn how caching works." | If structured tutoring is unclear, ask one brief mode-preference question |
| "정답 알려줘." (during tutor) | Direct answer for current question; no forced Socratic loop |
| "show progress" (during tutor) | Show level map with evidence and unassessed entries |
| "save state" (during tutor) | Print portable state; do not claim automatic persistence |

When evaluating, test both positive and negative activation cases, one-question-per-turn behavior, delayed recall, level changes, 2–3 failed attempts, final assessment, direct-answer override, and state export/import. Document observed results separately; this file is not itself execution evidence.
