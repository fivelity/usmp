<!-- Tooltip.svelte -->
<script lang="ts">
  import { fade, fly } from 'svelte/transition';
  import { onMount } from 'svelte';

  export let text: string;
  export let position: 'top' | 'right' | 'bottom' | 'left' = 'top';
  export let delay = 200;
  export let className = '';

  let tooltip: HTMLDivElement;
  let visible = false;
  let timer: number | undefined;

  function show() {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      visible = true;
    }, delay);
  }

  function hide() {
    if (timer) clearTimeout(timer);
    visible = false;
  }

  $: positionClasses = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2'
  }[position];

  $: arrowClasses = {
    top: 'bottom-0 left-1/2 -translate-x-1/2 translate-y-1/2 rotate-45',
    right: 'left-0 top-1/2 -translate-y-1/2 -translate-x-1/2 -rotate-45',
    bottom: 'top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 rotate-45',
    left: 'right-0 top-1/2 -translate-y-1/2 translate-x-1/2 -rotate-45'
  }[position];

  onMount(() => {
    return () => {
      if (timer) clearTimeout(timer);
    };
  });
</script>

<div
  class="tooltip-wrapper"
  on:mouseenter={show}
  on:mouseleave={hide}
  on:focus={show}
  on:blur={hide}
>
  <slot />
  {#if visible}
    <div
      class="tooltip {positionClasses} {className}"
      bind:this={tooltip}
      role="tooltip"
      transition:fly={{ y: 5, duration: 200 }}
    >
      <div class="tooltip-content">
        {text}
      </div>
      <div class="tooltip-arrow {arrowClasses}" />
    </div>
  {/if}
</div>

<style>
  .tooltip-wrapper {
    @apply inline-block;
  }

  .tooltip {
    @apply absolute z-50;
  }

  .tooltip-content {
    @apply bg-surface-elevated text-text px-3 py-2 rounded-md shadow-lg text-sm whitespace-nowrap;
  }

  .tooltip-arrow {
    @apply absolute w-2 h-2 bg-surface-elevated;
  }
</style> 