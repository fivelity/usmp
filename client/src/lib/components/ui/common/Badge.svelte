<!-- Badge.svelte -->
<script lang="ts">
  export let variant: 'default' | 'primary' | 'success' | 'warning' | 'error' = 'default';
  export let size: 'sm' | 'md' | 'lg' = 'md';
  export let dot = false;
  export let className = '';

  $: variantClasses = {
    default: 'bg-gray-100 text-gray-700',
    primary: 'bg-primary-100 text-primary-700',
    success: 'bg-success-100 text-success-700',
    warning: 'bg-warning-100 text-warning-700',
    error: 'bg-error-100 text-error-700'
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
    class="inline-block rounded-full {variantClasses} {dotClasses} {className}"
    role="status"
  ></span>
{:else}
  <span
    class="inline-flex items-center justify-center font-medium rounded-full {variantClasses} {sizeClasses} {className}"
    role="status"
  >
    <slot />
  </span>
{/if}

 