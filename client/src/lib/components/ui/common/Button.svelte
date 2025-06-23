<script lang="ts">
  interface Props {
    variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
    size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'icon';
    fullWidth?: boolean;
    leftIcon?: string | undefined;
    rightIcon?: string | undefined;
    href?: string | undefined;
    target?: string | undefined;
    type?: 'button' | 'submit' | 'reset';
    disabled?: boolean;
    loading?: boolean;
    onClick?: ((event: MouseEvent) => void) | undefined;
    onclick?: ((event: MouseEvent) => void) | undefined;
    className?: string;
    children?: import('svelte').Snippet;
    title?: string;
  }

  let {
    variant = 'primary',
    size = 'md',
    fullWidth = false,
    leftIcon = undefined,
    rightIcon = undefined,
    href = undefined,
    target = undefined,
    type = 'button',
    disabled = false,
    loading = false,
    onClick = undefined,
    onclick = undefined,
    className = '',
    children,
    title = undefined
  }: Props = $props();

  function handleClick(event: MouseEvent) {
    if (!disabled && !loading) {
      onClick?.(event);
      onclick?.(event);
    }
  }

  // Variant styles
  const variantClasses = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white border-transparent shadow-sm',
    secondary: 'bg-gray-600 hover:bg-gray-700 text-white border-transparent shadow-sm',
    outline: 'bg-transparent hover:bg-gray-50 text-gray-700 border-gray-300',
    ghost: 'bg-transparent hover:bg-gray-100 text-gray-700 border-transparent',
    danger: 'bg-red-600 hover:bg-red-700 text-white border-transparent shadow-sm'
  };

  // Size styles
  const sizeClasses = {
    xs: 'px-2 py-1 text-xs',
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base',
    xl: 'px-8 py-4 text-lg',
    icon: 'h-10 w-10'
  };

  let isDisabled = $derived(disabled || loading);
  
  let baseClasses = $derived([
    'inline-flex items-center justify-center gap-2 font-medium rounded-lg border',
    'transition-all duration-200 ease-in-out focus:outline-none focus:ring-2',
    'focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed',
    variantClasses[variant],
    sizeClasses[size],
    fullWidth ? 'w-full' : '',
    className
  ].filter(Boolean).join(' '));
</script>

{#if href}
  <a
    {href}
    {target}
    {title}
    class={baseClasses}
    class:opacity-50={isDisabled}
    class:cursor-not-allowed={isDisabled}
    onclick={handleClick}
    role="button"
    tabindex={isDisabled ? -1 : 0}
    aria-disabled={isDisabled}
  >
    {#if loading}
      <svg class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24" aria-hidden="true">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span class="sr-only">Loading</span>
    {:else if leftIcon}
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={leftIcon} />
      </svg>
    {/if}
    
    {@render children?.()}
    
    {#if rightIcon && !loading}
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={rightIcon} />
      </svg>
    {/if}
  </a>
{:else}
  <button
    {type}
    {title}
    class={baseClasses}
    disabled={isDisabled}
    onclick={handleClick}
    aria-disabled={isDisabled}
  >
    {#if loading}
      <svg class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24" aria-hidden="true">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span class="sr-only">Loading</span>
    {:else if leftIcon}
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={leftIcon} />
      </svg>
    {/if}
    
    {@render children?.()}
    
    {#if rightIcon && !loading}
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={rightIcon} />
      </svg>
    {/if}
  </button>
{/if}
