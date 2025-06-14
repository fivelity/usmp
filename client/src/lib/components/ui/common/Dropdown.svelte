<!-- Dropdown.svelte -->
<script lang="ts">
  import { fade, fly } from 'svelte/transition';
  import { createEventDispatcher, onMount } from 'svelte';

  export let trigger: 'click' | 'hover' = 'click';
  export let position: 'top' | 'right' | 'bottom' | 'left' = 'bottom';
  export let align: 'start' | 'center' | 'end' = 'start';
  export let className = '';

  const dispatch = createEventDispatcher<{
    open: void;
    close: void;
  }>();

  let dropdown: HTMLDivElement;
  let isOpen = false;
  let timer: number | undefined;

  $: positionClasses = {
    top: 'bottom-full mb-2',
    right: 'left-full ml-2',
    bottom: 'top-full mt-2',
    left: 'right-full mr-2'
  }[position];

  $: alignClasses = {
    start: position === 'top' || position === 'bottom' ? 'left-0' : 'top-0',
    center: position === 'top' || position === 'bottom' ? 'left-1/2 -translate-x-1/2' : 'top-1/2 -translate-y-1/2',
    end: position === 'top' || position === 'bottom' ? 'right-0' : 'bottom-0'
  }[align];

  function handleTrigger(event: MouseEvent) {
    if (trigger === 'click') {
      event.preventDefault();
      isOpen = !isOpen;
      dispatch(isOpen ? 'open' : 'close');
    }
  }

  function handleMouseEnter() {
    if (trigger === 'hover') {
      if (timer) clearTimeout(timer);
      isOpen = true;
      dispatch('open');
    }
  }

  function handleMouseLeave() {
    if (trigger === 'hover') {
      timer = setTimeout(() => {
        isOpen = false;
        dispatch('close');
      }, 100);
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      isOpen = false;
      dispatch('close');
    }
  }

  onMount(() => {
    window.addEventListener('keydown', handleKeydown);
    return () => {
      window.removeEventListener('keydown', handleKeydown);
      if (timer) clearTimeout(timer);
    };
  });
</script>

<div
  class="dropdown-wrapper"
  bind:this={dropdown}
  on:mouseenter={handleMouseEnter}
  on:mouseleave={handleMouseLeave}
>
  <div
    class="dropdown-trigger"
    on:click={handleTrigger}
    role="button"
    tabindex="0"
  >
    <slot name="trigger" />
  </div>

  {#if isOpen}
    <div
      class="dropdown-menu {positionClasses} {alignClasses} {className}"
      transition:fly={{ y: 5, duration: 200 }}
    >
      <slot />
    </div>
  {/if}
</div>

<style>
  .dropdown-wrapper {
    @apply relative inline-block;
  }

  .dropdown-trigger {
    @apply cursor-pointer;
  }

  .dropdown-menu {
    @apply absolute z-50 min-w-[8rem] bg-surface rounded-lg shadow-lg border border-border py-1;
  }

  /* Responsive adjustments */
  @media (max-width: 640px) {
    .dropdown-menu {
      @apply w-full;
    }
  }
</style> 