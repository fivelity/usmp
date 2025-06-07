<script lang="ts">
  const {
  variant = 'spinner',
  size = 'md',
  text = undefined,
  fullScreen = false
} = $props<{
  variant?: 'spinner' | 'pulse' | 'skeleton';
  size?: 'sm' | 'md' | 'lg';
  text?: string | undefined;
  fullScreen?: boolean;
}>();
  
  const sizeClasses = $derived((() => {
    const classes = {
      sm: 'w-4 h-4',
      md: 'w-8 h-8',
      lg: 'w-12 h-12'
    } as const;
    return classes[size as keyof typeof classes];
  })());
  
  const textSizes = $derived((() => {
    const classes = {
      sm: 'text-sm',
      md: 'text-base',
      lg: 'text-lg'
    } as const;
    return classes[size as keyof typeof classes];
  })());
</script>

{#if fullScreen}
  <div class="fixed inset-0 bg-gray-50 bg-opacity-80 backdrop-blur-sm flex items-center justify-center z-50">
    <div class="flex flex-col items-center gap-4">
      {#if variant === 'spinner'}
        <div class="border-4 border-primary-200 rounded-full {sizeClasses}" style="border-top-color: var(--theme-primary); animation: spin 1s linear infinite;"></div>
      {:else if variant === 'pulse'}
        <div class="bg-primary-500 rounded-full {sizeClasses}" style="animation: pulse 1.5s ease-in-out infinite;"></div>
      {:else}
        <div class="bg-gray-200 dark:bg-gray-700 rounded {sizeClasses}" style="animation: skeleton 1.5s ease-in-out infinite;"></div>
      {/if}
      
      {#if text}
        <p class="text-gray-500 dark:text-gray-400 font-medium {textSizes}">{text}</p>
      {/if}
    </div>
  </div>
{:else}
  <div class="flex flex-col items-center gap-2">
    {#if variant === 'spinner'}
      <div class="border-4 border-primary-200 rounded-full {sizeClasses}" style="border-top-color: var(--theme-primary); animation: spin 1s linear infinite;"></div>
    {:else if variant === 'pulse'}
      <div class="bg-primary-500 rounded-full {sizeClasses}" style="animation: pulse 1.5s ease-in-out infinite;"></div>
    {:else}
      <div class="bg-gray-200 dark:bg-gray-700 rounded {sizeClasses}" style="animation: skeleton 1.5s ease-in-out infinite;"></div>
    {/if}
    
    {#if text}
      <p class="text-gray-500 dark:text-gray-400 font-medium {textSizes}">{text}</p>
    {/if}
  </div>
{/if}

<style>
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