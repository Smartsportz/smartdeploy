---
name: Kinetic Velocity
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#c2c6d6'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#8c909f'
  outline-variant: '#424754'
  surface-tint: '#adc6ff'
  primary: '#adc6ff'
  on-primary: '#002e6a'
  primary-container: '#4d8eff'
  on-primary-container: '#00285d'
  inverse-primary: '#005ac2'
  secondary: '#ffb690'
  on-secondary: '#552100'
  secondary-container: '#ec6a06'
  on-secondary-container: '#4a1c00'
  tertiary: '#ffb3ad'
  on-tertiary: '#68000a'
  tertiary-container: '#ff5451'
  on-tertiary-container: '#5c0008'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004395'
  secondary-fixed: '#ffdbca'
  secondary-fixed-dim: '#ffb690'
  on-secondary-fixed: '#341100'
  on-secondary-fixed-variant: '#783200'
  tertiary-fixed: '#ffdad7'
  tertiary-fixed-dim: '#ffb3ad'
  on-tertiary-fixed: '#410004'
  on-tertiary-fixed-variant: '#930013'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display-xl:
    fontFamily: Anton
    fontSize: 72px
    fontWeight: '400'
    lineHeight: 72px
    letterSpacing: 0.02em
  headline-lg:
    fontFamily: Anton
    fontSize: 48px
    fontWeight: '400'
    lineHeight: 48px
  headline-lg-mobile:
    fontFamily: Anton
    fontSize: 32px
    fontWeight: '400'
    lineHeight: 32px
  headline-md:
    fontFamily: Anton
    fontSize: 24px
    fontWeight: '400'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.1em
  live-tag:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '700'
    lineHeight: 14px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 8px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
  max-width: 1440px
---

## Brand & Style
The design system is engineered for the high-stakes environment of sports management. It balances the raw energy of competitive athletics with the precision of advanced data analytics. The brand personality is **authoritative, kinetic, and elite**. It avoids the cluttered "spreadsheet" look of traditional management tools in favor of an immersive, media-rich experience that feels like a premium broadcast.

The visual style leverages **Glassmorphism** to maintain context while managing complex data layers. Surfaces use frosted translucency to allow background energy to peak through, creating a sense of depth and modernism. The aesthetic is "Stadium-Tech"—utilizing dark environments to make live data and vibrant brand colors pop with maximum contrast.

## Colors
The palette is rooted in a deep navy/charcoal base to minimize eye strain during long tournament days. 
- **Electric Blue (#3B82F6):** Used for primary actions, navigation states, and "Pro" tier features.
- **Vibrant Orange (#F97316):** Reserved for high-energy highlights, tournament progress, and conversion points.
- **Live Pulse (#EF4444):** A dedicated status color for real-time events.
- **Neutrals:** Range from a pitch-black background base to a slate-grey for secondary text and borders.

## Typography
The system uses a high-contrast typographic pairing to differentiate between "Atmosphere" and "Information."
- **Anton:** Used for all major headings. Its condensed, bold nature evokes classic sports jerseys and stadium jumbotrons. All Anton headings should be uppercase to maximize impact.
- **Inter:** The workhorse for all UI elements, data tables, and descriptions. Its neutral, systematic nature ensures legibility in dense tournament brackets.
- **JetBrains Mono:** Used for technical metadata, timestamps, and scoreboards to provide a "tech-readout" feel that implies precision timing and data accuracy.

## Layout & Spacing
The layout follows a **Fluid Grid** model with a strictly enforced 8px spatial rhythm.
- **Dashboard Layout:** Utilizes a sidebar navigation (collapsed on mobile) with a modular masonry grid for tournament cards.
- **Columns:** 12-column system for desktop, 8-column for tablet, and 4-column for mobile.
- **Gutters:** Generous 24px gutters to prevent the "data-clutter" common in sports management software.
- **Safe Areas:** Cards and overlays should utilize internal padding of 24px (3x base) to maintain the premium, airy feel of the glassmorphic style.

## Elevation & Depth
Depth is created through **Glassmorphism** rather than traditional drop shadows.
- **Level 1 (Base):** Solid navy (#0F172A).
- **Level 2 (Cards):** 70% opacity surface with a 12px Backdrop Blur. A 1px subtle border (White @ 10% opacity) defines the edge.
- **Level 3 (Overlays/Modals):** 85% opacity surface with a 24px Backdrop Blur. Use a faint primary-colored (Blue) outer glow instead of a black shadow to simulate light emission from the "screen."
- **Live Status:** Elements with the 'Live' status should have a subtle red ambient glow (#EF4444) to draw the eye immediately.

## Shapes
This design system uses a **Soft (1)** roundedness profile. While the brand is aggressive, the 0.25rem (4px) base radius ensures the interface feels modern and "engineered" rather than brutalist. 
- **Standard UI (Buttons, Inputs):** 4px radius.
- **Container Cards:** 8px radius (rounded-lg).
- **Status Tags:** Fully pill-shaped (rounded-full) to contrast against the structured grid of the tournament data.

## Components
- **Buttons:** Primary buttons are solid Electric Blue with white text, using a 2px bottom "border-shadow" of a darker blue to feel tactile. Secondary buttons use the "Ghost" style with the glassmorphic background.
- **Live Status Indicator:** A small circular dot next to the "LIVE" text label. It must include a CSS pulse animation: `scale(1)` to `scale(1.5)` with a `0.4` opacity fade.
- **Progress Bars:** Dual-layered. The track is a semi-transparent grey; the fill is a Vibrant Orange gradient.
- **Tournament Cards:** Feature a background image of the sport (low opacity) under the glass layer. Important stats (e.g., "Active Teams") use the JetBrains Mono font.
- **Real-time Status Indicators:** Small, high-contrast badges that change color based on tournament phase (e.g., Green for 'Registration', Orange for 'In-Progress', Blue for 'Finalized').
- **Inputs:** Dark field backgrounds with a 1px border that glows Electric Blue when focused.