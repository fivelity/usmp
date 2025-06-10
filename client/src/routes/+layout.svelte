<script lang="ts">
  import '../app.css';
  import { browser } from '$app/environment';
  import { sensorUtils } from '$lib/stores/sensorData.svelte';
  import { websocketStore } from '$lib/services/websocket.svelte';
  import { storeUtils } from '$lib/stores';

  import ThemeManager from '$lib/components/core/layout/ThemeManager.svelte';
  import AlertContainer from '$lib/components/ui/common/AlertContainer.svelte';

  // Access the data from the load function
  let { data } = $props();

  // Initialize stores with data from the server
  if (data.initialSensors) {
    sensorUtils.updateSensorSources(data.initialSensors);
  }
  if (data.initialTree) {
    sensorUtils.updateHardwareTree(data.initialTree);
  }

  // Effect to manage WebSocket connection
  $effect(() => {
    if (browser) {
      websocketStore.connect();

      const unsubscribe = websocketStore.subscribe((message: any) => {
        if (message.type === 'sensor_data' && message.data) {
          storeUtils.updateSensorData(message.data);
        }
      });

      return () => {
        unsubscribe();
        websocketStore.disconnect();
      };
    }
    return () => {}; // No-op for server-side
  });
</script>

<ThemeManager />
<AlertContainer />

<main class="min-h-screen bg-[var(--theme-background)] text-[var(--theme-text)] font-[var(--font-family)]">
  <slot />
</main>

<style>
  :global(.reduce-motion *) {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
</style>
