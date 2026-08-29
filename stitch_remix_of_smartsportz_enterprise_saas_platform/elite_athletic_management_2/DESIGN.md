---
name: Elite Athletic Management
colors:
  surface: '#101415'
  surface-dim: '#101415'
  surface-bright: '#363a3b'
  surface-container-lowest: '#0b0f10'
  surface-container-low: '#191c1e'
  surface-container: '#1d2022'
  surface-container-high: '#272a2c'
  surface-container-highest: '#323537'
  on-surface: '#e0e3e5'
  on-surface-variant: '#bdcabe'
  inverse-surface: '#e0e3e5'
  inverse-on-surface: '#2d3133'
  outline: '#889489'
  outline-variant: '#3e4a41'
  surface-tint: '#72db9d'
  primary: '#72db9d'
  on-primary: '#00391f'
  primary-container: '#0b8852'
  on-primary-container: '#ffffff'
  inverse-primary: '#006d40'
  secondary: '#b9c7e4'
  on-secondary: '#233148'
  secondary-container: '#3c4962'
  on-secondary-container: '#abb9d6'
  tertiary: '#b6c6ed'
  on-tertiary: '#20304f'
  tertiary-container: '#67779a'
  on-tertiary-container: '#000514'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#8ef8b7'
  primary-fixed-dim: '#72db9d'
  on-primary-fixed: '#002110'
  on-primary-fixed-variant: '#00522f'
  secondary-fixed: '#d6e3ff'
  secondary-fixed-dim: '#b9c7e4'
  on-secondary-fixed: '#0d1c32'
  on-secondary-fixed-variant: '#39475f'
  tertiary-fixed: '#d8e2ff'
  tertiary-fixed-dim: '#b6c6ed'
  on-tertiary-fixed: '#091b39'
  on-tertiary-fixed-variant: '#374767'
  background: '#101415'
  on-background: '#e0e3e5'
  surface-variant: '#323537'
typography:
  display-lg:
    fontFamily: Be Vietnam Pro
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Be Vietnam Pro
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Be Vietnam Pro
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-md:
    fontFamily: Be Vietnam Pro
    fontSize: 20px
    fontWeight: '500'
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
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  stats-xl:
    fontFamily: Be Vietnam Pro
    fontSize: 40px
    fontWeight: '800'
    lineHeight: 40px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 1440px
  gutter: 24px
  margin-desktop: 40px
  margin-mobile: 16px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style
The design system is engineered for professional sports environments, prioritizing high-performance data visualization and elite management workflows. The brand personality is authoritative, energetic, and technologically advanced, evoking the focus of a professional locker room and the precision of a high-end analytics dashboard.

The aesthetic follows a **Corporate / Modern** direction with subtle **Glassmorphism** influences. This creates a premium SaaS feel where high-contrast data is layered over deep, sophisticated backgrounds. The UI should feel fast and resilient, using sharp visual hierarchy to guide sports directors and coaches through complex leaderboards and athlete performance metrics.

## Colors
This design system utilizes a high-fidelity dark-mode foundation to reduce eye strain during prolonged data analysis.

*   **Primary (#0b8852):** A vibrant "Championship Green" used for primary actions, success states, and key performance indicators.
*   **Secondary (#0a192f):** A deep "Stadium Navy" serving as the primary canvas color.
*   **Tertiary (#112240):** A lighter navy used for card surfaces, navigation sidebars, and elevated containers.
*   **Neutral (#f8fafc):** Used exclusively for high-readability typography and icons to ensure maximum contrast against the dark background.

## Typography
The typography system balances the editorial strength of **Be Vietnam Pro** (replacing Poppins for a more contemporary, athletic edge) with the utilitarian precision of **Inter**. 

**JetBrains Mono** is introduced for labels and tabular data to ensure that jersey numbers and stopwatch timings are perfectly aligned in leaderboards. All headlines use a tight letter-spacing to maintain a bold, "locked-in" appearance typical of premium sports broadcasting.

## Layout & Spacing
The design system employs a **12-column fluid grid** for dashboard views, transitioning to a single-column stack on mobile. 

*   **Desktop:** 40px outer margins provide "breathing room" for dense data.
*   **Guttering:** A consistent 24px gutter ensures clear separation between data widgets.
*   **Rhythm:** An 8px base grid governs all padding and margins. Vertical rhythm should be generous to allow the high-fidelity elements to feel premium and uncrowded.

## Elevation & Depth
Depth is created through **Tonal Layering** rather than traditional drop shadows. 

1.  **Level 0 (Background):** Stadium Navy (#0a192f).
2.  **Level 1 (Cards/Panels):** Tertiary Navy (#112240) with a subtle 1px inner border (opacity 10% white) to define edges.
3.  **Level 2 (Modals/Popovers):** Slightly lighter navy with a 20px backdrop blur (Glassmorphism) and a soft, deep navy shadow to simulate physical lift.

Data points and leaderboards should use high-contrast text to "pop" off these layered surfaces.

## Shapes
In accordance with the "Elite Athletic" requirement, the design system utilizes a specific **18px corner radius** for all primary containers, cards, and modal windows. 

*   **Standard Cards:** 18px radius.
*   **Buttons:** 8px radius (to maintain a professional, slightly more rigid feel compared to larger cards).
*   **Data Inputs:** 8px radius.
*   **Avatar/Profile:** Circular (fully rounded).

## Components

### Buttons
Primary buttons use the Championship Green background with white text. Hover states should involve a subtle brightening of the green. "Ghost" buttons for secondary actions use a 1px border of the primary green and no fill.

### Leaderboards & Tables
Rows should have a subtle hover effect (a 5% white overlay). Columns containing numbers (ranks, points, times) must use the **label-sm** (JetBrains Mono) font for perfect vertical alignment. 

### Cards
All dashboard cards must adhere to the 18px corner radius. They should feature a padding of 24px (stack-lg) to ensure data visualization doesn't feel cramped.

### Input Fields
Inputs use the Tertiary Navy background with a 1px border. Upon focus, the border transitions to Championship Green with a soft outer glow.

### Athlete Chips
Small, rounded-pill indicators used for status (e.g., "Active", "Injured", "Bench"). Use a low-opacity version of the status color for the background and a high-opacity version for the text.

### Performance Gauges
Circular or linear progress bars should use the primary green against a dark navy track to visualize athlete KPIs or training completion percentages.