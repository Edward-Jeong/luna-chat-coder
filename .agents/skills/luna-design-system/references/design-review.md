# Luna Design Review Gate

Use this checklist only for material UI work. Skip irrelevant items rather than manufacturing findings.

## Source of truth

- Repository-root `DESIGN.md` exists for a new/material UI surface.
- The implementation follows deliberate project-specific design decisions rather than blindly preserving starter defaults.
- Reusable design decisions introduced by the change are reflected in `DESIGN.md`.
- Existing component/theme conventions are preserved unless the change intentionally migrates them.

## Visual consistency

- Semantic colors, typography, spacing, radii, elevation, and component states are consistent with `DESIGN.md`.
- No unexplained one-off visual values create design drift.
- Primary, secondary, destructive, disabled, selected, hover, focus, active, loading, empty, and error states are coherent where applicable.
- Operational interfaces prioritize scanability and task completion over decorative novelty.

## Responsive behavior

- Layout remains usable at the repository-defined supported viewports.
- Navigation, tables, forms, dialogs, cards, and data visualizations do not rely on accidental desktop-only dimensions unless explicitly scoped to desktop.
- Overflow behavior is intentional.

## Accessibility

- Semantic HTML is used where practical.
- Interactive controls have accessible names.
- Keyboard operation and visible focus are preserved.
- Important states are not communicated by color alone.
- Text/control contrast is appropriate for the project's accessibility target.
- Non-essential motion respects reduced-motion preferences when motion exists.

## Design verification

Prefer executable evidence in this order when the repository supports it:

1. existing component/unit tests for interaction states;
2. browser or E2E checks at relevant viewports;
3. existing accessibility automation;
4. existing visual regression/screenshot comparison;
5. `designmd lint DESIGN.md` when the optional Google design.md CLI is already available or justified.

Do not introduce a new heavy test stack only to satisfy this checklist unless the feature warrants it.

## Finding severity

- **Blocker** — materially violates required design intent, breaks a supported viewport/critical interaction, creates a meaningful accessibility failure, or leaves a new/material UI project without persistent design context.
- **Suggestion** — improves consistency, clarity, maintainability, or accessibility without blocking correct use.
- **Nit** — low-impact polish with no meaningful correctness or consistency risk.

Any blocker means the UI change is not merge-ready.
