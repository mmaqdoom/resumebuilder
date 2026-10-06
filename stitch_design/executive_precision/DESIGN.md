---
name: Executive Precision
colors:
  surface: '#faf8ff'
  surface-dim: '#d2d9f4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#eaedff'
  surface-container-high: '#e2e7ff'
  surface-container-highest: '#dae2fd'
  on-surface: '#131b2e'
  on-surface-variant: '#464555'
  inverse-surface: '#283044'
  inverse-on-surface: '#eef0ff'
  outline: '#777587'
  outline-variant: '#c7c4d8'
  surface-tint: '#4d44e3'
  primary: '#3525cd'
  on-primary: '#ffffff'
  primary-container: '#4f46e5'
  on-primary-container: '#dad7ff'
  inverse-primary: '#c3c0ff'
  secondary: '#006c49'
  on-secondary: '#ffffff'
  secondary-container: '#6cf8bb'
  on-secondary-container: '#00714d'
  tertiary: '#3130c0'
  on-tertiary: '#ffffff'
  tertiary-container: '#4b4dd8'
  on-tertiary-container: '#d9d8ff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e2dfff'
  primary-fixed-dim: '#c3c0ff'
  on-primary-fixed: '#0f0069'
  on-primary-fixed-variant: '#3323cc'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#e1e0ff'
  tertiary-fixed-dim: '#c0c1ff'
  on-tertiary-fixed: '#07006c'
  on-tertiary-fixed-variant: '#2f2ebe'
  background: '#faf8ff'
  on-background: '#131b2e'
  surface-variant: '#dae2fd'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.025em
  display-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0em
  label-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.04em
  mono-code:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-sm: 1rem
  margin: 2rem
  margin-sm: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system is tailored for students and early-career job seekers seeking high-conviction, professional outcomes without cognitive overload. It adopts an editorial yet technical SaaS visual posture—blending the focused utility of Linear, the document clarity of Notion, and the structural confidence of Stripe. 

The emotional target is clarity, momentum, and authority. The interface operates in the background, treating the user's resume as the primary visual artifact while providing surgical tools and real-time ATS feedback. Visual friction is minimized through strict low-contrast borders, purposeful typographic hierarchy, and tactical micro-interactions.

## Colors

The palette establishes a high-contrast canvas with controlled, expressive points of focus:

- **Primary Canvas & Surfaces**: The application defaults to pristine slate off-white (`#F8FAFC`) with cards and input surfaces elevated in pure white (`#FFFFFF`). Dark slate (`#0F172A`) serves as the dominant anchor for typography, structural icons, and deep contrast headers.
- **Accents & CTAs**: Deep indigo (`#4F46E5`) handles primary interactive states, accompanied by electric indigo (`#6366F1`) for secondary focuses, interactive indicators, and progress bars. Pressed/hover states step to `#4338CA`.
- **System Feedback & ATS Scoring**: Emerald green (`#10B981`) denotes ATS optimization benchmarks, valid section completions, and success metrics. Tinted backgrounds for positive states derive from a soft 8% tint of emerald.
- **Delimiters**: Structural lines rely entirely on crisp zinc/slate dividers (`#E2E8F0` for interior borders, `#CBD5E1` for active or focused boundaries).

## Typography

The type system pairs **Plus Jakarta Sans** for display, page headers, and section groupings with **Inter** for all utility, data entry, resume rendering, and status metadata. 

- **Headings**: Plus Jakarta Sans applies tight negative tracking (-0.02em) to provide a modern, product-led finish with robust geometric balance.
- **Form & Document Text**: Inter is configured at optical weights 400 and 500 to maximize legibility inside editing fields, preview sheets, and data tables.
- **Labels & Tags**: Uppercase micro-labels (`label-sm`) utilize 0.04em letter-spacing to cleanly differentiate metadata tags, keyword alerts, and validation rules from input text.

## Layout & Spacing

The application employs a dual-pane workspace model:
- **Left Panel (Form/Editor)**: Fixed to fluid allocation depending on resolution, anchoring input controls within structured 1-column and 2-column inline forms.
- **Right Panel (Document Canvas)**: Fluid, centered workspace presenting a proportional 8.5" x 11" (Letter/A4) canvas surrounded by dynamic breathing room.

### Breakpoints & Adaptive Layout
- **Desktop (≥ 1280px)**: 12-column layout with 24px gutters and 32px page margins. Split-screen workstation (50% inputs, 50% live paper preview).
- **Tablet (768px – 1279px)**: Split-pane collapses into a stacked view or tabbed toggle ("Edit" / "Preview"). Margins contract to 24px, gutters to 16px.
- **Mobile (< 768px)**: Strict single-column stack with persistent floating action bar for section switching and PDF generation. Margins reduce to 16px.

## Elevation & Depth

Visual separation relies predominantly on **tonal contrast** and **subtle, diffused ambient shadows** paired with razor-thin structural borders (`1px solid #E2E8F0`).

- **Surface Floor (`#F8FAFC`)**: Base page environment.
- **Interactive Sheets & Cards (`#FFFFFF`)**: Bordered with `#E2E8F0`, elevated with subtle multi-stop drop shadows:
  - Default: `0 1px 3px 0 rgba(15, 23, 42, 0.04), 0 1px 2px -1px rgba(15, 23, 42, 0.03)`
  - Elevated/Hover: `0 4px 6px -1px rgba(15, 23, 42, 0.06), 0 2px 4px -2px rgba(15, 23, 42, 0.04)`
- **A4 Live Resume Document**: Distinct elevated sheet with enhanced focus depth:
  - `0 10px 15px -3px rgba(15, 23, 42, 0.07), 0 4px 6px -4px rgba(15, 23, 42, 0.04)`
- **Overlays, Popovers, & Menus**: Float above the canvas using soft containment:
  - `0 20px 25px -5px rgba(15, 23, 42, 0.08), 0 8px 10px -6px rgba(15, 23, 42, 0.03)`, backed by a `1px solid rgba(226, 232, 240, 0.8)` border.

## Shapes

The design uses balanced, modern SaaS curvature. Interactive containers, cards, and input fields adhere to an **8px to 10px corner radius** (`roundedness: 2`), delivering clean geometry without feeling harsh. 

Pills are preserved strictly for status badges, keyword tags, ATS optimization scores, and toggle switches (`rounded-full` / 9999px), creating a stark semantic contrast against rectangular form fields and document cards.

## Components

### Buttons
- **Primary**: Solid background in `#4F46E5`, crisp white text, 8px radius, height: 38px (medium). Subtle interior highlight (`inset 0 1px 0 rgba(255, 255, 255, 0.15)`). Hover transforms to `#4338CA`.
- **Secondary / Outline**: `#FFFFFF` background, border `1px solid #CBD5E1`, text `#0F172A`. Hover background shifts to `#F8FAFC`.
- **Ghost**: Zero border, text `#475569`, shifts to `#0F172A` with `#F1F5F9` background on hover.

### Badges & Status Chips
- Pill-shaped (`rounded-full`), padded 4px 10px with `label-sm` uppercase styling.
- **ATS Pass / Success**: Light emerald base (`rgba(16, 185, 129, 0.1)`) with text `#065F46` and `#10B981` leading micro-dot.
- **Keyword Match**: Neutral base (`#F1F5F9`), text `#334155`, border `1px solid #E2E8F0`.

### Form Fields & Inputs
- Height: 40px, 8px radius, border `1px solid #CBD5E1`, surface `#FFFFFF`.
- Typography: Inter 14px regular (`body-md`), placeholder in `#94A3B8`.
- Focus state: Border transitions to `#4F46E5` with a subtle focus ring (`0 0 0 3px rgba(79, 70, 229, 0.15)`).

### Cards & Section Containers
- Modular building blocks for resume segments (Education, Experience, Skills).
- Solid white surface, 10px radius, bounded by `1px solid #E2E8F0`. Includes drag-and-drop grab handles styled with subtle `#94A3B8` icon dots.

### Selection Controls (Checkboxes & Radios)
- Checkboxes: 16px × 16px, 4px corner radius. Unchecked border `#CBD5E1`. Checked state transitions to `#4F46E5` with a crisp white check vector.
- Toggle Switches: 36px wide by 20px tall pill track with a 16px white circular thumb.