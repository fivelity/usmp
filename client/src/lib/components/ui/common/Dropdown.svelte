<!-- Dropdown.svelte -->
<script lang="ts">
  import { fly } from 'svelte/transition';
  import { createEventDispatcher, onMount } from 'svelte';

  const {
    trigger = 'click',
    position = 'bottom',
    align = 'start',
    className = '',
    children,
    triggerSnippet
  } = $props<{
    trigger?: 'click' | 'hover';
    position?: 'top' | 'right' | 'bottom' | 'left';
    align?: 'start' | 'center' | 'end';
    className?: string;
    children: any;
    triggerSnippet: any;
  }>();

  const dispatch = createEventDispatcher<{
    open: void;
    close: void;
  }>();

  let isOpen = $state(false);
  let timer: ReturnType<typeof setTimeout> | undefined;

  const positionClasses = $derived((() => {
    const classes = {
      top: 'bottom-full mb-2',
      right: 'left-full ml-2',
      bottom: 'top-full mt-2',
      left: 'right-full mr-2'
    } as const;
    return classes[position as keyof typeof classes];
  })());

  const alignClasses = $derived((() => {
    const classes = {
      start: position === 'top' || position === 'bottom' ? 'left-0' : 'top-0',
      center: position === 'top' || position === 'bottom' ? 'left-1/2 -translate-x-1/2' : 'top-1/2 -translate-y-1/2',
      end: position === 'top' || position === 'bottom' ? 'right-0' : 'bottom-0'
    } as const;
    return classes[align as keyof typeof classes];
  })());

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
  class="relative inline-block"
  role="menu"
  tabindex="0"
  onmouseenter={handleMouseEnter}
  onmouseleave={handleMouseLeave}
  onkeydown={handleKeydown}
>
  <div
    class="cursor-pointer"
    onclick={handleTrigger}
    onkeydown={handleKeydown}
    role="button"
    tabindex="0"
  >
    {@render triggerSnippet()}
  </div>

  {#if isOpen}
    <div
      class="absolute z-50 min-w-32 sm:min-w-32 w-full sm:w-auto bg-surface rounded-lg shadow-lg border border-border py-1 {positionClasses} {alignClasses} {className}"
      transition:fly={{ y: 5, duration: 200 }}
    >
      {@render children()}
    </div>
  {/if}
</div>