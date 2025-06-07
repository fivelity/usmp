<script lang="ts">
  import { fade, scale } from 'svelte/transition';
  import { onMount, type Snippet } from 'svelte';

  interface Props {
    isOpen?: boolean;
    title: string;
    size?: 'sm' | 'md' | 'lg' | 'xl';
    closeOnClickOutside?: boolean;
    closeOnEsc?: boolean;
    className?: string;
    onClose?: () => void;
    children?: Snippet;
    footer?: Snippet;
  }

  let {
    isOpen = false,
    title,
    size = 'md',
    closeOnClickOutside = true,
    closeOnEsc = true,
    className = '',
    onClose,
    children,
    footer
  }: Props = $props();

  let modal = $state<HTMLDivElement>();

  const sizeClassMap = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl'
  } as const;

  const sizeClasses = $derived(sizeClassMap[size]);

  function handleClose() {
    onClose?.();
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
      const keydownHandler = (event: KeyboardEvent) => {
        if (event.key === 'Escape') {
          handleClose();
        }
      };
      
      document.addEventListener('keydown', keydownHandler);
      
      return () => {
        document.removeEventListener('keydown', keydownHandler);
      };
    }
    return undefined;
  });
</script>

{#if isOpen}
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm"
    bind:this={modal}
    onclick={handleClickOutside}
    onkeydown={handleKeydown}
    role="button"
    tabindex="0"
    transition:fade={{ duration: 200 }}
  >
    <div
      class="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full mx-4 {sizeClasses} {className}"
      style="max-height: calc(100vh - 2rem);"
      transition:scale={{ duration: 200, start: 0.95 }}
    >
      <div class="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white">{title}</h3>
        <button
          class="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition-colors"
          onclick={handleClose}
          aria-label="Close modal"
        >
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="p-4 overflow-y-auto" style="max-height: calc(100vh - 12rem);">
        {@render children?.()}
      </div>
      <div class="p-4 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-2">
        {@render footer?.()}
      </div>
    </div>
  </div>
{/if}


