<script lang="ts">
  import type { BaseComponentProps } from '$lib/types';

  interface Props extends BaseComponentProps {
    size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
    color?: 'primary' | 'secondary' | 'white' | 'gray';
    text?: string;
    overlay?: boolean;
    onfoo?: () => void; // Example of a callback prop
  }

  let {
    size = 'md',
    color = 'primary',
    text,
    overlay = false,
    class: className = '',
    onfoo, // Example of using the callback prop
    ...restProps
  }: Props = $props();

  // Size variants
  const sizeClasses = {
    xs: 'w-3 h-3',
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
    xl: 'w-12 h-12'
  };

  // Color variants
  const colorClasses = {
    primary: 'text-blue-600',
    secondary: 'text-gray-600',
    white: 'text-white',
    gray: 'text-gray-400'
  };

  // Function to handle foo event
  function handleFoo() {
    if (onfoo) {
      onfoo();
    }
  }
</script>

<div 
  class="loading-spinner {className}"
  class:overlay
  {...restProps}
  onclick={handleFoo}
>
  <div class="spinner-content">
    <svg 
      class="animate-spin {sizeClasses[size]} {colorClasses[color]}" 
      fill="none" 
      viewBox="0 0 24 24"
    >
      <circle 
        class="opacity-25" 
        cx="12" 
        cy="12" 
        r="10" 
        stroke="currentColor" 
        stroke-width="4"
      ></circle>
      <path 
        class="opacity-75" 
        fill="currentColor" 
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
    
    {#if text}
      <span class="spinner-text {colorClasses[color]}">
        {text}
      </span>
    {/if}
  </div>
</div>

<style>
  .loading-spinner {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .loading-spinner.overlay {
    position: fixed;
    inset: 0;
    z-index: 50;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(2px);
  }

  .spinner-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
  }

  .spinner-text {
    font-size: 0.875rem;
    font-weight: 500;
  }
</style>
