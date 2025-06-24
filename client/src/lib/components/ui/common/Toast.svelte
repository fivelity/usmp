<script lang="ts">
  import { onMount } from 'svelte';
  import { fly } from 'svelte/transition';
  import type { BaseComponentProps } from '$lib/types';

  interface Props extends BaseComponentProps {
    type?: 'success' | 'error' | 'warning' | 'info';
    title?: string;
    message: string;
    duration?: number;
    closable?: boolean;
    position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'top-center' | 'bottom-center';
    close?: () => void;
  }

  let {
    type = 'info',
    title,
    message,
    duration = 5000,
    closable = true,
    position = 'top-right',
    class: className = '',
    close = () => {}
  }: Props = $props();

  let visible = $state(true);
  let timeoutId: number;

  // Type configurations
  const typeConfig = {
    success: {
      icon: 'M5 13l4 4L19 7',
      bgColor: 'bg-green-50',
      borderColor: 'border-green-200',
      iconColor: 'text-green-600',
      titleColor: 'text-green-800',
      messageColor: 'text-green-700'
    },
    error: {
      icon: 'M6 18L18 6M6 6l12 12',
      bgColor: 'bg-red-50',
      borderColor: 'border-red-200',
      iconColor: 'text-red-600',
      titleColor: 'text-red-800',
      messageColor: 'text-red-700'
    },
    warning: {
      icon: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z',
      bgColor: 'bg-yellow-50',
      borderColor: 'border-yellow-200',
      iconColor: 'text-yellow-600',
      titleColor: 'text-yellow-800',
      messageColor: 'text-yellow-700'
    },
    info: {
      icon: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200',
      iconColor: 'text-blue-600',
      titleColor: 'text-blue-800',
      messageColor: 'text-blue-700'
    }
  };

  // Position configurations
  const positionConfig = {
    'top-right': { x: 100, y: -100 },
    'top-left': { x: -100, y: -100 },
    'bottom-right': { x: 100, y: 100 },
    'bottom-left': { x: -100, y: 100 },
    'top-center': { x: 0, y: -100 },
    'bottom-center': { x: 0, y: 100 }
  };

  const config = $derived(typeConfig[type]);
  const flyConfig = $derived(positionConfig[position]);

  function handleClose() {
    visible = false;
    setTimeout(() => close(), 200);
  }

  onMount(() => {
    visible = false;
    setTimeout(() => close(), 200);
  });

  onMount(() => {
    if (duration > 0) {
      timeoutId = setTimeout(() => {
        handleClose();
      }, duration) as unknown as number;
    }

    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  });
</script>

{#if visible}
  <div
    class="toast {config.bgColor} {config.borderColor} {className}"
    transition:fly={{ ...flyConfig, duration: 200 }}
    role="alert"
    aria-live="polite"

  >
    <!-- Icon -->
    <div class="toast-icon {config.iconColor}">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={config.icon} />
      </svg>
    </div>

    <!-- Content -->
    <div class="toast-content">
      {#if title}
        <h4 class="toast-title {config.titleColor}">
          {title}
        </h4>
      {/if}
      <p class="toast-message {config.messageColor}">
        {message}
      </p>
    </div>

    <!-- Close Button -->
    {#if closable}
      <button
        type="button"
        class="toast-close"
        onclick={handleClose}
        aria-label="Close notification"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    {/if}

    <!-- Progress Bar -->
    {#if duration > 0}
      <div class="toast-progress">
        <div 
          class="toast-progress-bar {config.iconColor}"
          style="animation: progress {duration}ms linear"
        ></div>
      </div>
    {/if}
  </div>
{/if}

<style>
  .toast {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 1rem;
    border: 1px solid;
    border-radius: 0.75rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    max-width: 400px;
    position: relative;
    overflow: hidden;
  }

  .toast-icon {
    flex-shrink: 0;
    margin-top: 0.125rem;
  }

  .toast-content {
    flex: 1;
    min-width: 0;
  }

  .toast-title {
    font-size: 0.875rem;
    font-weight: 600;
    margin: 0 0 0.25rem 0;
    line-height: 1.25;
  }

  .toast-message {
    font-size: 0.875rem;
    margin: 0;
    line-height: 1.4;
  }

  .toast-close {
    flex-shrink: 0;
    padding: 0.25rem;
    border: none;
    background: transparent;
    color: #6b7280;
    border-radius: 0.375rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .toast-close:hover {
    background: rgba(0, 0, 0, 0.05);
    color: #374151;
  }

  .toast-progress {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: rgba(0, 0, 0, 0.1);
  }

  .toast-progress-bar {
    height: 100%;
    width: 100%;
    transform-origin: left;
    opacity: 0.7;
  }

  @keyframes progress {
    from {
      transform: scaleX(1);
    }
    to {
      transform: scaleX(0);
    }
  }
</style>
