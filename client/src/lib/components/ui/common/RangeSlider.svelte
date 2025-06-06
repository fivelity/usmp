<script lang="ts">
  import type { BaseComponentProps } from '$lib/types';

  interface Props extends BaseComponentProps {
    label?: string;
    value: number;
    min?: number;
    max?: number;
    step?: number;
    unit?: string;
    disabled?: boolean;
    showInput?: boolean;
    size?: 'sm' | 'md' | 'lg';
    color?: 'primary' | 'secondary' | 'success' | 'warning' | 'error';
    onchange?: (value: number) => void;
  }

  let {
    label,
    value = 0,
    min = 0,
    max = 100,
    step = 1,
    unit = '',
    disabled = false,
    showInput = true,
    size = 'md',
    color = 'primary',
    class: className = '',
    onchange,
    ...restProps
  }: Props = $props();

  let internalValue = $state(value);
  let isDragging = $state(false);

  // Update internal value when prop changes
  $effect(() => {
    internalValue = value;
  });

  function handleSliderChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const newValue = parseFloat(target.value);
    internalValue = newValue;
    if (onchange) {
      onchange(newValue);
    }
  }

  function handleInputChange(event: Event) {
    const target = event.target as HTMLInputElement;
    let newValue = parseFloat(target.value);
    
    // Clamp value to min/max
    newValue = Math.max(min, Math.min(max, newValue));
    
    if (!isNaN(newValue)) {
      internalValue = newValue;
      if (onchange) {
        onchange(newValue);
      }
    }
  }

  function handleMouseDown() {
    isDragging = true;
  }

  function handleMouseUp() {
    isDragging = false;
  }

  // Calculate percentage for visual feedback
  const percentage = $derived(((internalValue - min) / (max - min)) * 100);

  // Size variants
  const sizeClasses = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3'
  };

  const thumbSizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6'
  };

  const inputSizeClasses = {
    sm: 'text-xs px-2 py-1 w-16',
    md: 'text-sm px-3 py-2 w-20',
    lg: 'text-base px-4 py-3 w-24'
  };

  // Color variants
  const colorClasses = {
    primary: 'bg-blue-500',
    secondary: 'bg-gray-500',
    success: 'bg-green-500',
    warning: 'bg-yellow-500',
    error: 'bg-red-500'
  };
</script>

<div class="range-slider-container {className}" {...restProps}>
  {#if label}
    <div class="range-slider-header">
      <label class="range-slider-label" class:disabled for="range-slider-input">
        {label}
      </label>
      <div class="range-slider-value">
        {internalValue}{unit}
      </div>
    </div>
  {/if}

  <div class="range-slider-wrapper">
    <!-- Slider Track -->
    <div class="range-slider-track-container">
      <div class="range-slider-track {sizeClasses[size]}">
        <!-- Progress Fill -->
        <div 
          class="range-slider-fill {sizeClasses[size]} {colorClasses[color]}"
          style="width: {percentage}%"
        ></div>
        
        <!-- Slider Input -->
        <input
          id="range-slider-input"
          type="range"
          class="range-slider-input"
          class:dragging={isDragging}
          {min}
          {max}
          {step}
          {disabled}
          value={internalValue}
          onclick={handleSliderChange}
          onmousedown={handleMouseDown}
          onmouseup={handleMouseUp}
          aria-label={label || 'Range slider'}
        />
        
        <!-- Custom Thumb -->
        <div 
          class="range-slider-thumb {thumbSizeClasses[size]} {colorClasses[color]}"
          class:dragging={isDragging}
          class:disabled
          style="left: {percentage}%"
        >
          <div class="thumb-inner"></div>
        </div>
      </div>

      <!-- Min/Max Labels -->
      <div class="range-slider-labels">
        <span class="range-label">{min}{unit}</span>
        <span class="range-label">{max}{unit}</span>
      </div>
    </div>

    <!-- Number Input -->
    {#if showInput}
      <input
        type="number"
        class="range-slider-number-input {inputSizeClasses[size]}"
        class:disabled
        {min}
        {max}
        {step}
        {disabled}
        value={internalValue}
        oninput={handleInputChange}
      />
    {/if}
  </div>
</div>

<style>
  .range-slider-container {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .range-slider-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .range-slider-label {
    font-size: 0.875rem;
    font-weight: 500;
    color: #374151;
    transition: color 0.2s ease;
  }

  .range-slider-label.disabled {
    color: #9ca3af;
  }

  .range-slider-value {
    font-size: 0.875rem;
    font-weight: 600;
    color: #1f2937;
    font-family: 'JetBrains Mono', monospace;
    background: #f3f4f6;
    padding: 0.25rem 0.5rem;
    border-radius: 0.375rem;
  }

  .range-slider-wrapper {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .range-slider-track-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .range-slider-track {
    position: relative;
    background: #e5e7eb;
    border-radius: 9999px;
    overflow: hidden;
    transition: all 0.2s ease;
  }

  .range-slider-fill {
    position: absolute;
    top: 0;
    left: 0;
    border-radius: inherit;
    transition: width 0.2s ease;
    background: linear-gradient(90deg, currentColor 0%, currentColor 80%, rgba(255, 255, 255, 0.2) 100%);
  }

  .range-slider-input {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
    margin: 0;
  }

  .range-slider-input:disabled {
    cursor: not-allowed;
  }

  .range-slider-thumb {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    border: 2px solid white;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    pointer-events: none;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .range-slider-thumb:hover:not(.disabled) {
    transform: translate(-50%, -50%) scale(1.1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }

  .range-slider-thumb.dragging {
    transform: translate(-50%, -50%) scale(1.2);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
  }

  .range-slider-thumb.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .thumb-inner {
    width: 60%;
    height: 60%;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 50%;
  }

  .range-slider-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 0.25rem;
  }

  .range-label {
    font-size: 0.75rem;
    color: #6b7280;
    font-family: 'JetBrains Mono', monospace;
  }

  .range-slider-number-input {
    border: 1px solid #d1d5db;
    border-radius: 0.5rem;
    background: white;
    font-family: 'JetBrains Mono', monospace;
    transition: all 0.2s ease;
    text-align: center;
  }

  .range-slider-number-input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  .range-slider-number-input.disabled {
    background: #f9fafb;
    color: #9ca3af;
    cursor: not-allowed;
  }

  /* Custom scrollbar for webkit browsers */
  .range-slider-number-input::-webkit-outer-spin-button,
  .range-slider-number-input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  .range-slider-number-input[type=number] {
    -moz-appearance: textfield;
  }
</style>
