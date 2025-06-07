<!-- Alert.svelte -->
<script lang="ts">
  import { fly } from 'svelte/transition';
  import { onMount } from 'svelte';

  type AlertType = 'info' | 'success' | 'warning' | 'error';

  const {
    type = 'info' as AlertType,
    message,
    title = undefined,
    dismissible = true,
    autoDismiss = false,
    dismissTimeout = 5000,
    className = ''
  } = $props<{
    type?: AlertType;
    message: string;
    title?: string;
    dismissible?: boolean;
    autoDismiss?: boolean;
    dismissTimeout?: number;
    className?: string;
  }>();

  let visible = $state(true);
  let timer: NodeJS.Timeout | undefined;

  $effect(() => {
    if (autoDismiss && visible) {
      if (timer) clearTimeout(timer);
      timer = setTimeout(() => {
        visible = false;
      }, dismissTimeout);
    }
  });

  function handleDismiss() {
    visible = false;
  }

  onMount(() => {
    return () => {
      if (timer) clearTimeout(timer);
    };
  });

  const iconMap: Record<AlertType, string> = {
    info: 'fa-info-circle',
    success: 'fa-check-circle',
    warning: 'fa-exclamation-triangle',
    error: 'fa-times-circle'
  };

  const variantMap: Record<AlertType, string> = {
    info: 'bg-info-100 text-info-700 border-info-200',
    success: 'bg-success-100 text-success-700 border-success-200',
    warning: 'bg-warning-100 text-warning-700 border-warning-200',
    error: 'bg-error-100 text-error-700 border-error-200'
  };

  let icon = $derived(iconMap[type as AlertType]);
  let variantClasses = $derived(variantMap[type as AlertType]);
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
    @apply p-1 hover:bg-gray-100 hover:bg-opacity-50 rounded-full transition-colors;
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