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

<div class="toggle-switch-container {className}">
  <div class="toggle-switch-wrapper" class:reverse={labelPosition === 'left'}>
    <!-- Toggle Switch -->
    <button
      type="button"
      class="toggle-switch {currentSize.track}"
      class:checked
      class:disabled
      style="background-color: {checked ? currentColor : '#d1d5db'}"
      onclick={handleToggle}
      onkeydown={handleKeyDown}
      role="switch"
      aria-checked={checked}
      aria-label={label || 'Toggle switch'}
      {disabled}
    >
      <!-- Track Background -->
      <div class="toggle-track"></div>
      
      <!-- Thumb -->
      <div 
        class="toggle-thumb {currentSize.thumb}"
        class:checked
        class:disabled
        style="transform: translateX({checked ? currentSize.translate.split(' ')[0].replace('translate-x-', '') + 'px' : '0px'})"
      >
        <!-- Inner highlight -->
        <div class="thumb-highlight"></div>
      </div>

      <!-- Focus ring -->
      <div class="focus-ring"></div>
    </button>

    <!-- Label and Description -->
    {#if label || description}
      <div class="toggle-content">
        {#if label}
          <label for="toggle" class="toggle-label" class:disabled>
            {label}
          </label>
        {/if}
        {#if description}
          <p class="toggle-description" class:disabled>
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

<style>
  .toggle-switch-container {
    display: flex;
    flex-direction: column;
  }

  .toggle-switch-wrapper {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .toggle-switch-wrapper.reverse {
    flex-direction: row-reverse;
  }

  .toggle-switch {
    position: relative;
    border: none;
    border-radius: 9999px;
    cursor: pointer;
    transition: all 0.2s ease;
    flex-shrink: 0;
    outline: none;
    overflow: hidden;
  }

  .toggle-switch:hover:not(.disabled) {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .toggle-switch:focus-visible .focus-ring {
    opacity: 1;
    transform: scale(1.1);
  }

  .toggle-switch.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .toggle-track {
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, transparent 50%, rgba(0, 0, 0, 0.1) 100%);
    pointer-events: none;
  }

  .toggle-thumb {
    position: relative;
    background: white;
    border-radius: 50%;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 1px;
  }

  .toggle-thumb.checked {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  }

  .toggle-thumb.disabled {
    background: #f3f4f6;
  }

  .thumb-highlight {
    width: 60%;
    height: 60%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0.2) 100%);
    border-radius: 50%;
    transition: opacity 0.2s ease;
  }

  .toggle-thumb.checked .thumb-highlight {
    opacity: 0.7;
  }

  .focus-ring {
    position: absolute;
    inset: -3px;
    border: 2px solid #3b82f6;
    border-radius: inherit;
    opacity: 0;
    transition: all 0.2s ease;
    pointer-events: none;
  }

  .toggle-content {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    min-width: 0;
  }

  .toggle-label {
    font-size: 0.875rem;
    font-weight: 500;
    color: #374151;
    cursor: pointer;
    transition: color 0.2s ease;
    line-height: 1.25;
  }

  .toggle-label.disabled {
    color: #9ca3af;
    cursor: not-allowed;
  }

  .toggle-description {
    font-size: 0.75rem;
    color: #6b7280;
    margin: 0;
    line-height: 1.4;
    transition: color 0.2s ease;
  }

  .toggle-description.disabled {
    color: #9ca3af;
  }

  /* Animation for state changes */
  @keyframes toggleOn {
    0% {
      transform: translateX(0) scale(1);
    }
    50% {
      transform: translateX(0.25rem) scale(1.1);
    }
    100% {
      transform: translateX(var(--translate-distance)) scale(1);
    }
  }

  @keyframes toggleOff {
    0% {
      transform: translateX(var(--translate-distance)) scale(1);
    }
    50% {
      transform: translateX(calc(var(--translate-distance) - 0.25rem)) scale(1.1);
    }
    100% {
      transform: translateX(0) scale(1);
    }
  }
</style>
