<script lang="ts">
  import type { BaseComponentProps } from '$lib/types';

  interface Props extends BaseComponentProps {
    label?: string;
    description?: string;
    checked: boolean;
    disabled?: boolean;
    size?: 'sm' | 'md' | 'lg';
    color?: 'primary' | 'secondary' | 'success' | 'warning' | 'error';
    labelPosition?: 'left' | 'right';
    onchange?: (value: boolean) => void;
  }

  let {
    label,
    description,
    checked = false,
    disabled = false,
    size = 'md',
    color = 'primary',
    labelPosition = 'right',
    class: className = '',
    onchange
  }: Props = $props();

  // Size variants
  const sizeClasses = {
    sm: {
      track: 'w-8 h-4',
      thumb: 'w-3 h-3',
      translate: 'translate-x-4'
    },
    md: {
      track: 'w-11 h-6',
      thumb: 'w-5 h-5',
      translate: 'translate-x-5'
    },
    lg: {
      track: 'w-14 h-7',
      thumb: 'w-6 h-6',
      translate: 'translate-x-7'
    }
  };

  // Color variants
  const colorClasses = {
    primary: 'bg-blue-600',
    secondary: 'bg-gray-600',
    success: 'bg-green-600',
    warning: 'bg-yellow-600',
    error: 'bg-red-600'
  };

  const currentSize = $derived(sizeClasses[size]);
  const currentColor = $derived(colorClasses[color]);

  function handleToggle() {
    if (!disabled && onchange) {
      onchange(!checked);
    }
  }

  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === ' ' || event.key === 'Enter') {
      event.preventDefault();
      handleToggle();
    }
  }
</script>

<div class="flex flex-col {className}">
  <div class="flex items-start gap-3" class:flex-row-reverse={labelPosition === 'left'}>
    <!-- Toggle Switch -->
    <button
      type="button"
      class="relative border-none rounded-full cursor-pointer transition-all duration-200 flex-shrink-0 outline-none overflow-hidden {currentSize.track} {checked ? currentColor : 'bg-gray-300'} hover:scale-105 hover:shadow-md focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
      class:checked
      class:disabled
      onclick={handleToggle}
      onkeydown={handleKeyDown}
      role="switch"
      aria-checked={checked}
      aria-label={label || 'Toggle switch'}
      {disabled}
    >
      <!-- Track Background -->
      <div class="absolute inset-0 rounded-full bg-gradient-to-br from-white/10 via-transparent to-black/10 pointer-events-none"></div>
      
      <!-- Thumb -->
      <div 
        class="relative bg-white rounded-full transition-all duration-200 ease-out shadow-sm flex items-center justify-center m-0.5 {currentSize.thumb} {checked ? currentSize.translate : ''} {checked ? 'shadow-md' : ''} {disabled ? 'bg-gray-200' : ''}"
        class:checked
        class:disabled
      >
        <!-- Inner highlight -->
        <div class="w-3/5 h-3/5 bg-gradient-to-br from-white/80 to-white/20 rounded-full transition-opacity duration-200 {checked ? 'opacity-70' : ''}"></div>
      </div>
    </button>

    <!-- Label and Description -->
    {#if label || description}
      <div class="flex flex-col gap-1 min-w-0">
        {#if label}
          <label for="toggle" class="text-sm font-medium text-gray-700 cursor-pointer transition-colors leading-tight {disabled ? 'text-gray-400 cursor-not-allowed' : ''}">
            {label}
          </label>
        {/if}
        {#if description}
          <p class="text-xs text-gray-500 m-0 leading-relaxed transition-colors {disabled ? 'text-gray-400' : ''}">
            {description}
          </p>
        {/if}
      </div>
    {/if}
  </div>
  {#if label}
    <input type="checkbox" id="toggle" class="sr-only" checked={checked} disabled={disabled} />
  {/if}
</div>


