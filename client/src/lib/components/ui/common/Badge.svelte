<!-- Badge.svelte -->
<script lang="ts">
  export let variant: 'default' | 'primary' | 'success' | 'warning' | 'error' = 'default';
  export let size: 'sm' | 'md' | 'lg' = 'md';
  export let dot = false;
  export let className = '';

  $: variantClasses = {
    default: 'bg-surface-elevated text-text',
    primary: 'bg-primary/20 text-primary',
    success: 'bg-success/20 text-success',
    warning: 'bg-warning/20 text-warning',
    error: 'bg-error/20 text-error'
  }[variant];

  $: sizeClasses = {
    sm: 'text-xs px-1.5 py-0.5',
    md: 'text-sm px-2 py-0.5',
    lg: 'text-base px-2.5 py-1'
  }[size];

  $: dotClasses = {
    sm: 'w-1.5 h-1.5',
    md: 'w-2 h-2',
    lg: 'w-2.5 h-2.5'
  }[size];
</script>

{#if dot}
  <span
    class="badge-dot {variantClasses} {dotClasses} {className}"
    role="status"
  />
{:else}
  <span
    class="badge {variantClasses} {sizeClasses} {className}"
    role="status"
  >
    <slot />
  </span>
{/if}

<style>
  .badge {
    @apply inline-flex items-center justify-center font-medium rounded-full;
  }

  .badge-dot {
    @apply inline-block rounded-full;
  }
</style> 