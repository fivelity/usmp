<!-- AlertContainer.svelte -->
<script lang="ts">
  import { alerts } from '$lib/stores/alerts';
  import Alert from './common/Alert.svelte';
  import type { Alert as AlertType } from '$lib/stores/alerts';

  export let position: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' = 'top-right';
  export let maxAlerts = 5;
  export let className = '';

  $: positionClasses = {
    'top-right': 'top-4 right-4',
    'top-left': 'top-4 left-4',
    'bottom-right': 'bottom-4 right-4',
    'bottom-left': 'bottom-4 left-4'
  }[position];

  function handleDismiss(alert: AlertType) {
    alerts.remove(alert.id);
  }
</script>

<div
  class="alert-container {positionClasses} {className}"
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

<style>
  .alert-container {
    @apply fixed z-50 flex flex-col gap-2;
    max-width: 400px;
  }

  /* Responsive adjustments */
  @media (max-width: 640px) {
    .alert-container {
      @apply w-full px-4;
      max-width: none;
    }
  }
</style> 