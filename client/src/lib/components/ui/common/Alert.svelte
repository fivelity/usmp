<!-- Alert.svelte -->
<script lang="ts">
  import { fade, fly } from 'svelte/transition';
  import { onMount } from 'svelte';

  export let type: 'info' | 'success' | 'warning' | 'error' = 'info';
  export let message: string;
  export let title: string | undefined = undefined;
  export let dismissible = true;
  export let autoDismiss = false;
  export let dismissTimeout = 5000;
  export let className = '';

  let visible = true;
  let timer: NodeJS.Timeout | undefined;

  $: if (autoDismiss && visible) {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      visible = false;
    }, dismissTimeout);
  }

  function handleDismiss() {
    visible = false;
  }

  onMount(() => {
    return () => {
      if (timer) clearTimeout(timer);
    };
  });

  $: icon = {
    info: 'fa-info-circle',
    success: 'fa-check-circle',
    warning: 'fa-exclamation-triangle',
    error: 'fa-times-circle'
  }[type];

  $: variantClasses = {
    info: 'bg-info/20 text-info border-info/30',
    success: 'bg-success/20 text-success border-success/30',
    warning: 'bg-warning/20 text-warning border-warning/30',
    error: 'bg-error/20 text-error border-error/30'
  }[type];
</script>

{#if visible}
  <div
    class="alert {variantClasses} {className}"
    transition:fly={{ y: -20, duration: 300 }}
  >
    <div class="alert-content">
      <i class="fas {icon}" />
      <div class="alert-text">
        {#if title}
          <h4 class="alert-title">{title}</h4>
        {/if}
        <p class="alert-message">{message}</p>
      </div>
    </div>
    {#if dismissible}
      <button
        class="alert-dismiss"
        on:click={handleDismiss}
        aria-label="Dismiss alert"
      >
        <i class="fas fa-times" />
      </button>
    {/if}
  </div>
{/if}

<style>
  .alert {
    @apply flex items-start justify-between gap-4 p-4 rounded-lg border;
  }

  .alert-content {
    @apply flex items-start gap-3 flex-1;
  }

  .alert-text {
    @apply flex-1;
  }

  .alert-title {
    @apply font-medium mb-1;
  }

  .alert-message {
    @apply text-sm;
  }

  .alert-dismiss {
    @apply p-1 hover:bg-surface/50 rounded-full transition-colors;
  }

  /* Animation for auto-dismiss */
  .alert:global(.fade-out) {
    animation: fadeOut 0.3s ease-out forwards;
  }

  @keyframes fadeOut {
    from {
      opacity: 1;
      transform: translateY(0);
    }
    to {
      opacity: 0;
      transform: translateY(-10px);
    }
  }
</style> 