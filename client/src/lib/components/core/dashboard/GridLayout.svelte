<script lang="ts">
  // import type { Size } from '$lib/types'; // Removed unused import
  
  const {
    columns = 1,
    gap = '1rem',
    minWidth = '250px',
    maxWidth = '1fr',
    padding = '1rem',
    className = ''
  } = $props<{
    columns?: number;
    gap?: string;
    minWidth?: string;
    maxWidth?: string;
    padding?: string;
    className?: string;
  }>();
  
  // Responsive breakpoints (removed unused variable)
  // const breakpoints = {
  //   sm: '640px',
  //   md: '768px',
  //   lg: '1024px',
  //   xl: '1280px'
  // };
  
  // Generate responsive grid template columns
  const getGridTemplateColumns = (cols: number): string => {
    return `repeat(${cols}, minmax(${minWidth}, ${maxWidth}))`;
  };
</script>

<div 
  class="grid-layout {className}"
  style="
    display: grid;
    grid-template-columns: {getGridTemplateColumns(columns)};
    gap: {gap};
    padding: {padding};
  "
>
  <slot />
</div>

<style>
  .grid-layout {
    width: 100%;
  }
  
  /* Responsive adjustments */
  @media (max-width: 640px) {
    .grid-layout {
      grid-template-columns: 1fr !important;
    }
  }
  
  @media (min-width: 641px) and (max-width: 768px) {
    .grid-layout {
      grid-template-columns: repeat(2, 1fr) !important;
    }
  }
  
  @media (min-width: 769px) and (max-width: 1024px) {
    .grid-layout {
      grid-template-columns: repeat(3, 1fr) !important;
    }
  }
  
  @media (min-width: 1025px) {
    .grid-layout {
      grid-template-columns: repeat(4, 1fr) !important;
    }
  }
</style> 