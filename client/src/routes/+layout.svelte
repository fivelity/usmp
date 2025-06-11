<script lang="ts">
  import '../app.css';
  import { browser } from '$app/environment';
  import { websocketStore } from '$lib/services/websocket.svelte';
  import { updateSensorData } from '$lib/stores/data/sensors.svelte';
  import { ui } from '$lib/stores/core/ui.svelte';

  import ThemeManager from '$lib/components/core/layout/ThemeManager.svelte';
  import AlertContainer from '$lib/components/ui/common/AlertContainer.svelte';
  import ContextMenu from '$lib/components/ui/common/ContextMenu.svelte';

  // Effect to manage WebSocket connection and data
  $effect(() => {
    if (browser) {
      websocketStore.connect();

      // This effect will re-run whenever a new message arrives
      const message = websocketStore.message;
      if (message && message.type === 'sensor_data' && message.data) {
        updateSensorData(message.data);
      }

      return () => {
        // This cleanup runs when the component is destroyed
        websocketStore.disconnect();
      };
    }
    return () => {}; // No-op for server-side
  });

  function handleContextMenuAction(event: CustomEvent<{ action: string }>) {
    console.log('Context menu action dispatched:', event.detail.action);
    // Future logic to handle specific actions at the layout level can go here
  }
</script>

<ThemeManager />
<AlertContainer />

{#if ui.contextMenu.show}
  <ContextMenu
    x={ui.contextMenu.x}
    y={ui.contextMenu.y}
    items={ui.contextMenu.items}
    dispatch={handleContextMenuAction}
  />
{/if}

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
