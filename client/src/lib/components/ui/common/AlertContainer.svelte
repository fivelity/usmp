<!-- AlertContainer.svelte -->
<script lang="ts">
  import { alerts } from '$lib/stores/alerts';
  import Alert from './Alert.svelte';
  import type { Alert as AlertType } from '$lib/stores/alerts';

  const {
    position = 'top-right',
    maxAlerts = 5,
    className = ''
  } = $props<{
    position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left';
    maxAlerts?: number;
    className?: string;
  }>();

  const positionClasses = $derived((() => {
    const classes = {
      'top-right': 'top-4 right-4',
      'top-left': 'top-4 left-4',
      'bottom-right': 'bottom-4 right-4',
      'bottom-left': 'bottom-4 left-4'
    } as const;
    return classes[position as keyof typeof classes];
  })());

  function handleDismiss(alert: AlertType) {
    alerts.remove(alert.id);
  }
</script>

<div
  class="fixed z-50 flex flex-col gap-2 max-w-sm sm:max-w-sm w-full sm:w-auto px-4 sm:px-0 {positionClasses} {className}"
  role="alert"
  aria-live="polite"
>
  {#each $alerts.slice(0, maxAlerts) as alert (alert.id)}
    <Alert
      {...alert}
      on:dismiss={() => handleDismiss(alert)}
    />
  {/each}
</div>