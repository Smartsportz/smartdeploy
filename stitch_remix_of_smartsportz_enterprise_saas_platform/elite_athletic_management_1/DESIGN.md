---
name: Elite Athletic Management
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#3e4a41'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#6e7a70'
  outline-variant: '#bdcabe'
  surface-tint: '#006d40'
  primary: '#006c40'
  on-primary: '#ffffff'
  primary-container: '#0b8852'
  on-primary-container: '#ffffff'
  inverse-primary: '#72db9d'
  secondary: '#545f73'
  on-secondary: '#ffffff'
  secondary-container: '#d5e0f8'
  on-secondary-container: '#586377'
  tertiary: '#9e3e44'
  on-tertiary: '#ffffff'
  tertiary-container: '#bd565b'
  on-tertiary-container: '#ffffff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#8ef8b7'
  primary-fixed-dim: '#72db9d'
  on-primary-fixed: '#002110'
  on-primary-fixed-variant: '#00522f'
  secondary-fixed: '#d8e3fb'
  secondary-fixed-dim: '#bcc7de'
  on-secondary-fixed: '#111c2d'
  on-secondary-fixed-variant: '#3c475a'
  tertiary-fixed: '#ffdad9'
  tertiary-fixed-dim: '#ffb3b3'
  on-tertiary-fixed: '#40000a'
  on-tertiary-fixed-variant: '#7f272f'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Poppins
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Poppins
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Poppins
    fontSize: 30px
    fontWeight: '600'
    lineHeight: '1.3'
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Poppins
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Be Vietnam Pro
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Be Vietnam Pro
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  body-sm:
    fontFamily: Be Vietnam Pro
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-md:
    fontFamily: Be Vietnam Pro
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Be Vietnam Pro
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  section-gap-lg: 120px
  section-gap-md: 80px
  gutter: 24px
  margin-desktop: 40px
  margin-mobile: 16px
  container-max: 1280px
---

## Brand & Style

The design system is engineered for elite performance management, targeting high-stakes athletic organizations and professional sports tech. It adopts a **Premium Light** aesthetic inspired by the precision of Stripe and the refined minimalism of Apple. 

The visual narrative focuses on clarity, speed, and high-fidelity execution. By utilizing a "clean-room" philosophy—characterized by expansive white space and surgical precision in alignment—the interface recedes to let performance data take center stage. The emotional response is one of absolute reliability, professional rigor, and modern sophistication.

## Colors

The palette is anchored by **Emerald Green**, used strategically for high-intent actions, key metrics, and brand presence. This is balanced against **Deep Slate** for primary information architecture to ensure maximum legibility and a grounded, authoritative feel.

- **Primary (Emerald Green):** Reserved for primary CTAs, active states, and success indicators.
- **Secondary (Deep Slate):** Used for headings, primary text, and heavy iconography.
- **Neutral:** A range of grays used for secondary text and structural borders.
- **Backgrounds:** Pure white (#FFFFFF) is the primary canvas, with Very Light Gray (#F8FAFC) used to differentiate surface areas like sidebars or secondary content sections.

## Typography

The typographic system utilizes a dual-font strategy to balance impact with utility. 

**Poppins** is the headline face, providing a geometric, modern, and confident structure for titles and display metrics. **Be Vietnam Pro** serves as the primary engine for body copy and interface labels; its contemporary, humanist qualities ensure high readability in data-dense environments while maintaining a friendly, approachable tone.

Maintain tight tracking on larger display types to reinforce the "Premium" feel. Use generous line heights for body copy to prevent visual fatigue during long periods of data analysis.

## Layout & Spacing

This design system employs a **12-column fluid grid** for internal application pages, transitioning to a fixed-width container for landing and marketing-heavy views. 

The defining characteristic is the **generous vertical rhythm**. Standard sections are separated by 80px to 120px of whitespace, creating a sense of "breathe" that distinguishes the product from cluttered legacy athletic software. 

- **Desktop:** 12 columns, 24px gutters, 40px side margins.
- **Tablet:** 8 columns, 20px gutters, 24px side margins.
- **Mobile:** 4 columns, 16px gutters, 16px side margins.

## Elevation & Depth

Depth is articulated through **soft, ambient shadows** rather than harsh borders or heavy overlays. Surfaces should feel light and lifted off the background.

The signature "Soft Shadow" is defined as `0 10px 15px -3px rgba(0, 0, 0, 0.1)`. This is applied primarily to cards and floating menus. To maintain the minimalist aesthetic, avoid stacking multiple layers of elevation; use a maximum of two levels (Base background and Elevated surface). For secondary interactive elements, use low-contrast 1px outlines (`#E2E8F0`) to define boundaries without adding visual weight.

## Shapes

The shape language is sophisticated and approachable. All primary containers and cards utilize a **18px border radius**, creating a distinct "Premium" silhouette that is softer than standard corporate systems but more structured than consumer-grade "pill" designs.

Buttons and input fields follow a standard 8px (0.5rem) radius to maintain a functional, precise appearance within the larger, softer containers.

## Components

- **Buttons:** Primary buttons use a solid Emerald Green fill with white text and 8px rounded corners. Secondary buttons use a subtle gray ghost style with a 1px border.
- **Cards:** White backgrounds (#FFFFFF) with the signature 18px radius and soft ambient shadow. Cards should never have a heavy border.
- **Input Fields:** Soft gray backgrounds (#F8FAFC) or white with a 1px #E2E8F0 border. Focus states must use a 2px Emerald Green ring.
- **Chips/Badges:** Small, 4px rounded corners. Use light tints of the status color (e.g., light green background with dark green text for "Active").
- **Lists:** Clean, borderless rows separated by subtle 1px horizontal lines (#F1F5F9). Use generous 16px-20px vertical padding per row.
- **Specialty Components:** 
    - *Metric Tiles:* Large Poppins display numbers with small Be Vietnam Pro labels.
    - *Progress Rings:* Use thin-stroke Emerald Green circular indicators for athlete performance tracking.