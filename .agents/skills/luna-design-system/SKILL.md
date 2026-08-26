---
name: luna-design-system
description: Keep Luna-managed UI projects visually coherent by creating and maintaining DESIGN.md as persistent design context, routing UI work through a Design Specialist, and applying an independent Design Reviewer gate.
license: MIT
compatibility: Designed for Agent Skills hosts and Codex custom agents. The optional Google design.md CLI may be used when available, but it is not required.
metadata:
  version: "0.1.0"
---

# Luna Design System

Use this skill for repository work that materially creates or changes a user interface, visual component system, frontend layout, dashboard, form workflow, design tokens, accessibility behavior, or other product-facing presentation.

Luna Design System does not create a separate always-on team. It extends the Coding Team with a conditional **Design Specialist** and an independent **Design Reviewer**. Keep the existing Luna Router principle: use the smallest specialist set that materially reduces risk.

## DESIGN.md is the design source of truth

For Luna-managed UI work, `DESIGN.md` is persistent design context for humans and coding agents. It combines machine-readable design tokens in YAML front matter with human-readable design rationale and constraints in Markdown.

The prose is not decorative documentation. It explains the product context, audience, information density, visual character, constraints, and reasons behind the tokens. Prefer specific references and operational context over generic adjectives such as "modern", "clean", or "premium".

Do not treat `DESIGN.md` as a replacement for CSS, Tailwind configuration, component libraries, design files, or framework-native themes. It describes intent and stable constraints; implementation stays in the project's chosen technologies.

## Automatic project behavior

Before material UI implementation:

1. Determine whether the requested work is materially UI-facing. Examples include web/mobile screens, dashboards, forms, frontend navigation, component libraries, visualizations, styling systems, or significant visual redesigns.
2. Look for a repository-root `DESIGN.md`.
3. If it exists, read it before architecture or implementation decisions that affect UI and preserve intentional project-specific choices.
4. If it does not exist, instantiate `templates/DESIGN.md` as repository-root `DESIGN.md` when the Luna template is available. Replace `{{PROJECT_NAME}}`, then refine generic starter content using known product requirements, existing UI evidence, brand guidance, and repository conventions.
5. When the template is not locally available, create an equivalent minimal `DESIGN.md` with the same core sections rather than silently proceeding without persistent design context.
6. Do not invent brand facts. Leave an explicit project-specific TODO or retain a neutral starter token when evidence is missing and that value is safe to defer.
7. A missing `DESIGN.md` is not a reason to block tiny UI bug fixes when creating one would be disproportionate. Create it for new UI projects, new product surfaces, material redesigns, or any work likely to establish reusable visual decisions.

When a repository is created from the Luna project template, carry `templates/DESIGN.md` with it and instantiate the root `DESIGN.md` during the initial project setup whenever the architecture includes a UI surface.

## Design Specialist protocol

The Design Specialist participates before implementation when UI decisions are material.

1. Read existing product requirements, screenshots/design references if supplied, component/theme configuration, and `DESIGN.md`.
2. Define or refine design intent, target users, task context, information density, layout behavior, semantic color roles, typography, spacing, shapes, component behavior, accessibility, motion, and data-visualization constraints as applicable.
3. Prefer semantic tokens and reusable rules over screen-specific one-off values.
4. Respect existing product identity and implementation conventions. Do not redesign established interfaces merely to match the starter template.
5. Record deliberate reusable design-system changes in `DESIGN.md` in the same feature branch.
6. Hand implementation constraints to the Implementation Engineer in concrete, testable terms.

## Design Reviewer gate

After material UI implementation and before the Coding Team declares the change review-ready, independently review:

- consistency with `DESIGN.md` intent and tokens;
- responsive layout behavior appropriate to supported viewports;
- component and interaction-state consistency;
- information hierarchy and operational scanability;
- accessibility, including semantic structure, keyboard/focus behavior, contrast, non-color cues, and reduced-motion behavior where applicable;
- loading, empty, error, disabled, hover, focus, active, and destructive-action states that materially apply;
- visual drift such as arbitrary one-off colors, spacing, radii, typography, gradients, shadows, or decorative patterns that contradict the design source of truth.

Classify findings as **blocker**, **suggestion**, or **nit**. A Design Reviewer blocker prevents the Coding Team from presenting the UI change as ready for merge.

A Design Reviewer is not a substitute for browser/E2E/visual verification. Use executable verification when the repository supports it, and never claim a visual or accessibility check that did not run.

## Optional DESIGN.md validation

If `@google/design.md` / `designmd` is already available or can be used without introducing an unjustified dependency, it may validate structure, token references, and supported contrast checks. Do not make the Luna workflow depend on the package merely to read or maintain `DESIGN.md`.

If used, record the exact command and result. On Windows prefer the dot-free `designmd` alias form when shell association makes `design.md` ambiguous.

## Routing handoffs

- Coding -> Design Specialist when material UI behavior, design system, frontend layout, accessibility, or data presentation is involved.
- Design Specialist -> Security when UI changes materially affect authentication, authorization, sensitive-data exposure, privileged actions, security warnings, or trust boundaries.
- Design Reviewer -> Coding when implementation changes are required.
- Design Reviewer -> Design Specialist when the source-of-truth itself is incomplete or internally inconsistent.
- Incident -> Design only when the diagnosed defect is actually a UI/interaction/design-system problem; do not route infrastructure or runtime incidents through Design.

## Completion evidence

For material UI changes, the completion report should state:

- whether `DESIGN.md` existed, was created, or was updated;
- which design-specific checks actually ran;
- Design Reviewer findings and whether any blocker remains;
- the exact repository/branch/commit or PR state;
- whether the change is merge-ready, review-ready, or still blocked.

Read `references/design-review.md` for the compact review checklist and decision rules.
