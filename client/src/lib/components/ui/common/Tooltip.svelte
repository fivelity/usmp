<!-- Tooltip.svelte -->
<script lang="ts">
  import { fly } from 'svelte/transition';
  import type { Snippet } from 'svelte';
  import { onMount } from 'svelte';

  type Props = {
    text: string;
    position?: 'top' | 'right' | 'bottom' | 'left';
    delay?: number;
    className?: string;
    children?: Snippet;
  };
  let {
    text,
    position = 'top',
    delay = 200,
    className = '',
    children
  }: Props = $props();

  let visible = $state(false);
  let timer = $state<NodeJS.Timeout | undefined>(undefined);

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

  const positionClasses = $derived(({
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2'
  })[position]);

  const arrowClasses = $derived(({
    top: 'bottom-0 left-1/2 -translate-x-1/2 translate-y-1/2 rotate-45',
    right: 'left-0 top-1/2 -translate-y-1/2 -translate-x-1/2 -rotate-45',
    bottom: 'top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 rotate-45',
    left: 'right-0 top-1/2 -translate-y-1/2 translate-x-1/2 -rotate-45'
  })[position]);

  onMount(() => {
    return () => {
      if (timer) clearTimeout(timer);
    };
  });
</script>

<div
  class="tooltip-wrapper"
  role="button"
  tabindex="0"
  onmouseenter={show}
  onmouseleave={hide}
  onfocus={show}
  onblur={hide}
>
  {#if children}{@render children()}{/if}
  {#if visible}
    <div
      class="tooltip {positionClasses} {className}"
      
      role="tooltip"
      transition:fly={{ y: 5, duration: 200 }}
    >
      <div class="tooltip-content">
        {text}
      </div>
      <div class="tooltip-arrow {arrowClasses}"></div>
    </div>
  {/if}
</div>

<style>
  .tooltip-wrapper {
    display: inline-block;
  }

  .tooltip {
    position: absolute;
    z-index: 50;
  }

  .tooltip-content {
    background-color: var(--color-surface-elevated);
    color: var(--color-text);
    padding: 0.5rem 0.75rem;
    border-radius: 0.375rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    font-size: 0.875rem;
    white-space: nowrap;
  }

  .tooltip-arrow {
    position: absolute;
    width: 0.5rem;
    height: 0.5rem;
    background-color: var(--color-surface-elevated);
  }
</style>