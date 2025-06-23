<script lang="ts">
  import { scale } from 'svelte/transition';
  
  interface Props {
    value?: string;
    label?: string;
    showHex?: boolean;
    disabled?: boolean;
    onfoo?: (value: string) => void;
  }

  let {
    value = $bindable('#3b82f6'),
    label = '',
    showHex = true,
    disabled = false,
    onfoo = () => {}
  }: Props = $props();

  let isOpen = $state(false);
  let colorInput: HTMLInputElement = $state();

  const presetColors = [
    '#3b82f6', // blue
    '#10b981', // green
    '#f59e0b', // yellow
    '#ef4444', // red
    '#8b5cf6', // purple
    '#ec4899', // pink
    '#6b7280', // gray
    '#000000', // black
    '#ffffff', // white
  ];

  function handleColorChange(event: Event) {
    const target = event.target as HTMLInputElement;
    value = target.value;
    onfoo(value);
  }

  function selectPreset(color: string) {
    value = color;
    onfoo(value);
    isOpen = false;
  }

  function togglePicker() {
    if (disabled) return;

    if (!isOpen) {
      isOpen = true;
      setTimeout(() => {
        colorInput?.click();
      }, 50);
    } else {
      isOpen = false;
    }
  }

  function handleClickOutside(event: MouseEvent) {
    const target = event.target as HTMLElement;
    if (isOpen && !target.closest('.color-picker-container')) {
      isOpen = false;
    }
  }
</script>

<svelte:window onclick={handleClickOutside} />

<div class="color-picker-container">
  {#if label}
    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1" for="color-input">
      {label}
    </label>
  {/if}

  <div class="relative">
    <!-- Color preview button -->
    <button
      type="button"
      class="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white dark:bg-gray-800 w-full text-left focus:outline-none focus:ring-2 focus:ring-blue-500"
      class:opacity-50={disabled}
      class:cursor-not-allowed={disabled}
      onclick={togglePicker}
      aria-haspopup="true"
      aria-expanded={isOpen}
    >
      <span 
        class="block w-5 h-5 rounded-full border border-gray-300 shadow-inner" 
        style="background-color: {value};"
        aria-hidden="true"
      ></span>

      {#if showHex}
        <span class="text-sm text-gray-700 dark:text-gray-300">{value}</span>
      {/if}

      <svg 
        class="w-4 h-4 ml-auto text-gray-400" 
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- Color picker dropdown -->
    {#if isOpen}
      <div 
        class="absolute z-10 mt-1 w-full bg-white dark:bg-gray-800 rounded-md shadow-lg border border-gray-200 dark:border-gray-700 p-3"
        transition:scale={{ duration: 100, start: 0.95 }}
        role="menu"
      >
        <!-- Color input -->
        <div class="mb-3">
          <input
            bind:this={colorInput}
            type="color"
            value={value}
            oninput={handleColorChange}
            class="w-full h-8 cursor-pointer rounded border border-gray-300 dark:border-gray-600"
            id="color-input"
          />
        </div>

        <!-- Preset colors -->
        <div class="grid grid-cols-3 gap-2">
          {#each presetColors as color}
            <button
              type="button"
              class="w-full aspect-square rounded-md border border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
              style="background-color: {color};"
              onclick={() => selectPreset(color)}
              aria-label={`Select color ${color}`}
            ></button>
          {/each}
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  /* Hide default color input appearance */
  input[type="color"] {
    -webkit-appearance: none;
    appearance: none;
    padding: 0;
    border: none;
  }

  input[type="color"]::-webkit-color-swatch-wrapper {
    padding: 0;
  }

  input[type="color"]::-webkit-color-swatch {
    border: none;
    border-radius: 4px;
  }
</style>
