<!-- Temporary icon wrapper for Svelte 5 compatibility -->
<script lang="ts">
  interface Props {
    name: string;
    class?: string;
    size?: number;
    color?: string;
    [key: string]: any;
  }

  const { name, class: className = "", size = 20, color = "currentColor" } = $props();

  // Simple icon mapping for most common icons
  const iconPaths: Record<string, string> = {
    // Panel icons
    "panel-left": "M3 4h18v16H3V4zm2 2v12h3V6H5zm5 0v12h9V6h-9z",
    "panel-right": "M3 4h18v16H3V4zm2 2v12h9V6h-9zm11 0v12h3V6h-3z",
    
    // Edit icons  
    "pencil": "M12 20h9v-1l-3.5-3.5-1-1L12 20zm1.41-11.59L5 16.83V19h2.17l8.41-8.41-2.17-2.17zM20.71 7.04a1 1 0 0 0 0-1.41l-2.34-2.34a1 1 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z",
    "eye": "M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.11-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z",
    
    // Action icons
    "undo": "M9 14l-4-4 4-4v3h5a4 4 0 0 1 0 8h-5v3z",
    "redo": "M15 14l4-4-4-4v3H9a4 4 0 0 0 0 8h6v3z",
    "download": "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3",
    "upload": "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 4v12",
    "save": "M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2zM17 21v-8H7v8M7 3v5h8",
    "cloud": "M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z",
    
    // User icons
    "log-in": "M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4M10 17l5-5-5-5M21 12H9",
    "log-out": "M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9",
    "user": "M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z",
    "loader2": "M21 12a9 9 0 1 1-6.219-8.56",
    "trash2": "M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6h14zM10 11v6M14 11v6",
    
    // Theme icons
    "sun": "M12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10zM12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42",
    "moon": "M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z",
    
    // Default fallback
    "default": "M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
  };

  const path = iconPaths[name] || iconPaths.default;
</script>

<svg 
  width={size} 
  height={size} 
  viewBox="0 0 24 24" 
  fill="none" 
  stroke={color} 
  stroke-width="2" 
  stroke-linecap="round" 
  stroke-linejoin="round" 
  class="{className} lucide lucide-{name}"
>
  <path d={path}></path>
  
  <!-- Special handling for loader2 (spinner) -->
  {#if name === "loader2"}
    <style>
      .lucide-loader2 {
        animation: spin 1s linear infinite;
      }
      @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
    </style>
  {/if}
</svg>
