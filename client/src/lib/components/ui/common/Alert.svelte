<!-- Alert.svelte -->
<script lang="ts">
  import { fly } from 'svelte/transition';
  import { onMount, createEventDispatcher } from 'svelte';

  type AlertType = 'info' | 'success' | 'warning' | 'error';
  
  const dispatch = createEventDispatcher<{
    dismiss: void;
  }>();

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
    dispatch('dismiss');
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

  const icon = $derived(iconMap[type as AlertType]);
  const variantClasses = $derived(variantMap[type as AlertType]);
</script>

{#if visible}
  <div
    class="flex items-start justify-between gap-4 p-4 rounded-lg border {variantClasses} {className}"
    transition:fly={{ y: -20, duration: 300 }}
  >
    <div class="flex items-start gap-3 flex-1">
      <i class="fas {icon}"></i>
      <div class="flex-1">
        {#if title}
          <h4 class="font-medium mb-1">{title}</h4>
        {/if}
        <p class="text-sm">{message}</p>
      </div>
    </div>
    {#if dismissible}
      <button
        class="p-1 hover:bg-gray-100 hover:bg-opacity-50 rounded-full transition-colors"
        onclick={handleDismiss}
        aria-label="Dismiss alert"
      >
        <i class="fas fa-times"></i>
      </button>
    {/if}
  </div>
{/if}

<style>
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