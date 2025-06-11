---
trigger: always_on
description: Svelte 5 best practices, UI principles, and interactions.
---

# 02-frontend-development

## Frontend Development (SvelteKit & UI)

STRICT REQUIREMENT:
- Svelte 5 Runes Adoption: Use `$state`, `$derived`, and `$effect` for reactivity. Avoid `$:` unless strictly necessary, and such instances must be clearly commented.
- UI Aesthetics: Allow for easy theme switching to change the overall look.
  - Default: a modern, clean interface with a preferred dark theme. 'Github Dark' / 'Github Light' inspired aesthetic. 
  - Custom Themes (json, import/export): allow extensive aesthetic adjustments.
    - Included Custom Themes: 
      - 'Gamer': a theme inspired by Battlefield 2042 & Escape from Tarkov UI design aesthetic. googleFont: 'Chakra Petch'.
      - 'Techi': a tech enthusiast inspired theme (sharper corners, innovative & pro FUI design aesthetic). googleFont: 'Orbitron'.
- Consistency: Use `"Inter"` font unless specified otherwise. Maintain consistent corners on all elements.
- Responsiveness: Fully adaptable UI without fixed pixel values—use `%`, `vw`, or Tailwind responsive prefixes (`sm:`, `md:`, `lg:`).
- Interactivity: Buttons and links must reliably respond to mouse clicks and touch taps.
- No Cumulative Layout Shifts (CLS): Prevent unexpected layout jumps.
- Dashboard Customization: 
  Support:
  - Adding/removing/moving widgets dynamically.
  - Drag-n-Drop placement.
  - Resizing widgets.
  Widget customization:
  - Edit/change gauge type.
  - Edit/change sensor source.
  - Show/hide sensor display name.
  - Edit/change sensor display name.
  - Show/hide sensor metric/unit (i.e. ℃, MHz, MB, etc.)
  - Edit/change gauge attributes (i.e. Radial Gauge: Arc-start-position: 235 degrees; Arc-end-position: 115 degrees; Arc-stroke-thickness: 4px; Arc-dashes: true; etc.)
  - Saving/loading custom dashboard layouts.
    - Widget placement, gauge type, sensor, size, style.
    - Include custom UI elements (i.e. User-uploaded custom gauges, widgets, images, image-sequence-gauges)
  - Custom Gauges: User-uploaded image-sequence (Aida64 sensor panel custom gauge inspired)
    - Allow user to upload multiple images to make up a sequence that will be used to render custom gauges.
    - Maximum of 24 images/sequence.