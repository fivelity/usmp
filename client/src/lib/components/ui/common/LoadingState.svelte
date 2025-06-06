<script lang="ts">
  export let variant: 'spinner' | 'pulse' | 'skeleton' = 'spinner';
  export let size: 'sm' | 'md' | 'lg' = 'md';
  export let text: string | undefined = undefined;
  export let fullScreen: boolean = false;
  
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };
  
  const textSizes = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg'
  };
</script>

{#if fullScreen}
  <div class="loading-fullscreen">
    <div class="loading-content">
      {#if variant === 'spinner'}
        <div class="spinner {sizeClasses[size]}" />
      {:else if variant === 'pulse'}
        <div class="pulse {sizeClasses[size]}" />
      {:else}
        <div class="skeleton {sizeClasses[size]}" />
      {/if}
      
      {#if text}
        <p class="loading-text {textSizes[size]}">{text}</p>
      {/if}
    </div>
  </div>
{:else}
  <div class="loading-container">
    {#if variant === 'spinner'}
      <div class="spinner {sizeClasses[size]}" />
    {:else if variant === 'pulse'}
      <div class="pulse {sizeClasses[size]}" />
    {:else}
      <div class="skeleton {sizeClasses[size]}" />
    {/if}
    
    {#if text}
      <p class="loading-text {textSizes[size]}">{text}</p>
    {/if}
  </div>
{/if}

<style>
  .loading-fullscreen {
    @apply fixed inset-0 bg-background/80 backdrop-blur-sm flex items-center justify-center z-50;
  }
  
  .loading-content {
    @apply flex flex-col items-center gap-4;
  }
  
  .loading-container {
    @apply flex flex-col items-center gap-2;
  }
  
  .spinner {
    @apply border-4 border-primary/20 rounded-full;
    border-top-color: var(--theme-primary);
    animation: spin 1s linear infinite;
  }
  
  .pulse {
    @apply bg-primary rounded-full;
    animation: pulse 1.5s ease-in-out infinite;
  }
  
  .skeleton {
    @apply bg-surface-elevated rounded;
    animation: skeleton 1.5s ease-in-out infinite;
  }
  
  .loading-text {
    @apply text-text-muted font-medium;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }
  
  @keyframes skeleton {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 0.8; }
  }
</style> 