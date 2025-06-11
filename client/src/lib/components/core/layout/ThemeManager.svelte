<script lang="ts">
  import { visualSettings } from '$lib/stores/core/visual.svelte';
  import { browser } from '$app/environment';

  $effect(() => {
    if (browser && visualSettings) {
      const root = document.documentElement;
      
      // Apply Tailwind dark mode class
      if (visualSettings.theme === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }

      // Apply theme class for color scheme (prefixed with theme- on body for custom CSS)
      const currentThemeClass = [...document.body.classList].find(c => c.startsWith('theme-'));
      if (currentThemeClass) {
        document.body.classList.remove(currentThemeClass);
      }
      document.body.classList.add(`theme-${visualSettings.color_scheme}`);

      // Apply other visual properties
      root.style.setProperty('--font-family', visualSettings.font_family);
      root.style.setProperty('--grid-size', `${visualSettings.grid_size}px`);
      root.style.setProperty('--animation-level', visualSettings.animation_level.toString());

      if (visualSettings.reduce_motion) {
        document.body.classList.add('reduce-motion');
      } else {
        document.body.classList.remove('reduce-motion');
      }
    }
  });
</script> 