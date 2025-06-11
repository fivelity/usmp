---
trigger: always_on
description: 
globs: 
---
# 02-frontend-development
## Frontend Development (SvelteKit & UI)
### Svelte 5 best practices, UI principles, and interactions.
STRICT REQUIREMENT:
- Svelte 5 Runes Adoption: Use `$state`, `$derived`, and `$effect` for reactivity. Avoid `$:` unless strictly necessary, and such instances must be clearly commented.
- UI Aesthetics: Maintain a modern, clean interface with a preferred dark theme.
- Consistency: Use `"Inter"` font unless specified otherwise. Maintain rounded corners on all elements.
- Responsiveness: Fully adaptable UI without fixed pixel values—use `%`, `vw`, or Tailwind responsive prefixes (`sm:`, `md:`, `lg:`).
- Interactivity: Buttons and links must reliably respond to mouse clicks and touch taps.
- No Cumulative Layout Shifts (CLS): Prevent unexpected layout jumps.
- Dashboard Customization: Support:
  - Adding/removing widgets dynamically.
  - Resizing widgets (even if drag-and-drop is not implemented yet).


  - Saving/loading custom dashboard layouts.