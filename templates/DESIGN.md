---
version: "alpha"
name: "{{PROJECT_NAME}}"
description: "Persistent design context for Luna-managed UI work. Replace placeholders and refine this file before material UI implementation."
colors:
  primary: "#111827"
  secondary: "#475569"
  accent: "#2563EB"
  background: "#F8FAFC"
  surface: "#FFFFFF"
  text: "#111827"
  text-muted: "#64748B"
  border: "#CBD5E1"
  success: "#15803D"
  warning: "#B45309"
  danger: "#B91C1C"
typography:
  heading-lg:
    fontFamily: "system-ui"
    fontSize: "2rem"
    fontWeight: 700
    lineHeight: 1.2
  heading-md:
    fontFamily: "system-ui"
    fontSize: "1.5rem"
    fontWeight: 650
    lineHeight: 1.3
  body-md:
    fontFamily: "system-ui"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.5
  label-sm:
    fontFamily: "system-ui"
    fontSize: "0.875rem"
    fontWeight: 600
    lineHeight: 1.4
rounded:
  sm: "4px"
  md: "8px"
  lg: "12px"
  full: "9999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  xxl: "48px"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: "12px"
  input-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: "12px"
  card-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.lg}"
    padding: "24px"
---

# {{PROJECT_NAME}} Design System

## Overview

Describe the product, primary users, working environment, information density, and the emotional/operational character the interface must convey.

For enterprise or operational software, prefer explicit context such as:

> A focused operational console used by professionals who need to scan status, compare records, identify exceptions, and complete routine actions quickly. The interface should feel like a dependable engineering tool rather than a marketing site.

Replace this example with project-specific design intent before significant UI implementation. Specific references and constraints are more useful to coding agents than generic adjectives such as "modern" or "premium".

## Colors

Use semantic roles consistently. Do not invent new colors in components when an existing token expresses the same role.

- **Primary:** Core brand/structural color.
- **Accent:** Primary interaction and focus color.
- **Background / Surface:** Page and contained-content layers.
- **Text / Text Muted:** Primary and secondary information hierarchy.
- **Success / Warning / Danger:** Operational states. Never rely on color alone to communicate meaning.

Project-specific palettes should replace the starter values above when brand guidance exists.

## Typography

Typography must optimize readability before decoration. Define project-specific type families and scales when available; otherwise retain a restrained system stack. Keep hierarchy semantic and reusable rather than assigning arbitrary font sizes per screen.

## Layout

Use a predictable responsive layout with clear content hierarchy. Start from the spacing tokens above and refine them only when project requirements justify a different rhythm.

Document here:

- target breakpoints and minimum supported viewport;
- maximum content width or fluid-grid behavior;
- navigation model;
- expected information density;
- table/form/dashboard layout rules;
- mobile behavior when applicable.

## Elevation & Depth

Prefer hierarchy through spacing, borders, surface contrast, and typography. Use shadows only where they communicate layering or interaction. Avoid decorative depth that reduces scanability.

## Shapes

Use the rounded scale consistently. Avoid arbitrary radii. Operational and enterprise interfaces should generally favor restrained shapes over decorative pill-heavy layouts unless the product identity requires otherwise.

## Components

Document project-specific component behavior and visual states as the implementation becomes concrete. Reuse the application's chosen component library and theme system; DESIGN.md defines intent and constraints, not a parallel UI framework.

At minimum define materially important states for:

- buttons and destructive actions;
- inputs, validation, and error feedback;
- navigation and selection;
- tables/lists and empty/loading/error states;
- dialogs/drawers;
- status/severity indicators.

## Accessibility

- Meet WCAG 2.2 AA contrast expectations for normal product UI unless the project has a stricter requirement.
- Do not communicate status, severity, selection, or errors using color alone.
- Preserve visible keyboard focus.
- Support keyboard operation for interactive controls.
- Use semantic HTML and accessible names before adding ARIA workarounds.
- Respect `prefers-reduced-motion` for non-essential motion.

## Motion

Motion should communicate state change, hierarchy, or continuity. Keep routine interaction feedback short and restrained. Avoid animation that delays task completion or obscures operational information.

## Data Visualization

When charts, security severity, health states, or metrics are present, define semantic visual mappings here. Keep mappings consistent across screens and provide non-color cues where interpretation matters.

## Do's and Don'ts

### Do

- Preserve the design intent in this file across sessions and agents.
- Prefer existing design tokens and established components.
- Keep critical state and primary actions visually unambiguous.
- Design loading, empty, error, disabled, hover, focus, and active states intentionally.
- Update DESIGN.md in the same change when a deliberate design-system decision changes.

### Don't

- Don't generate a marketing-style hero section for an operational application unless explicitly required.
- Don't add gradients, glassmorphism, glow, excessive shadows, or decorative animation by default.
- Don't create arbitrary one-off colors, spacing values, radii, or typography when tokens already exist.
- Don't hide essential information or actions behind hover-only interactions.
- Don't sacrifice accessibility or information density for visual novelty.
- Don't treat this starter file as immutable; project-specific evidence and requirements should replace generic defaults.
