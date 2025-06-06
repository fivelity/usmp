<script lang="ts">
  import { fade, scale } from 'svelte/transition';
  import { createEventDispatcher, onMount } from 'svelte';

  export let isOpen = false;
  export let title: string;
  export let size: 'sm' | 'md' | 'lg' | 'xl' = 'md';
  export let closeOnClickOutside = true;
  export let closeOnEsc = true;
  export let className = '';

  const dispatch = createEventDispatcher<{
    close: void;
  }>();

  let modal: HTMLDivElement;

  $: sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl'
  }[size];

  function handleClose() {
    dispatch('close');
  }

  function handleKeydown(event: KeyboardEvent) {
    if (closeOnEsc && event.key === 'Escape') {
      handleClose();
    }
  }

  function handleClickOutside(event: MouseEvent) {
    if (closeOnClickOutside && event.target === modal) {
      handleClose();
    }
  }

  onMount(() => {
    if (closeOnEsc) {
      window.addEventListener('keydown', handleKeydown);
    }
    return () => {
      if (closeOnEsc) {
        window.removeEventListener('keydown', handleKeydown);
      }
    };
  });
</script>

{#if isOpen}
  <div
    class="modal-backdrop"
    bind:this={modal}
    on:click={handleClickOutside}
    transition:fade={{ duration: 200 }}
  >
    <div
      class="modal {sizeClasses} {className}"
      transition:scale={{ duration: 200, start: 0.95 }}
    >
      <div class="modal-header">
        <h3 class="modal-title">{title}</h3>
        <button
          class="modal-close"
          on:click={handleClose}
          aria-label="Close modal"
        >
          <i class="fas fa-times" />
        </button>
      </div>
      <div class="modal-content">
        <slot />
      </div>
      <div class="modal-footer">
        <slot name="footer" />
      </div>
    </div>
  </div>
{/if}

<style>
  .modal-backdrop {
    @apply fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm;
  }

  .modal {
    @apply bg-surface rounded-lg shadow-xl w-full mx-4;
    max-height: calc(100vh - 2rem);
  }

  .modal-header {
    @apply flex items-center justify-between p-4 border-b border-border;
  }

  .modal-title {
    @apply text-lg font-medium;
  }

  .modal-close {
    @apply p-1 hover:bg-surface-hover rounded-full transition-colors;
  }

  .modal-content {
    @apply p-4 overflow-y-auto;
    max-height: calc(100vh - 12rem);
  }

  .modal-footer {
    @apply p-4 border-t border-border flex justify-end gap-2;
  }

  /* Responsive adjustments */
  @media (max-width: 640px) {
    .modal {
      @apply mx-2;
    }

    .modal-content {
      max-height: calc(100vh - 8rem);
    }
  }
</style>
