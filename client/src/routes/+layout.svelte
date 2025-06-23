<script lang="ts">
  import '../app.css';
  import { browser } from '$app/environment';
  import { websocketStore } from '$lib/services/websocket.svelte';
  import { sensorDataManager } from '$lib/stores/sensorData';
  import { ui } from '$lib/stores/core/ui.svelte';

  import ThemeManager from '$lib/components/core/layout/ThemeManager.svelte';
  import AlertContainer from '$lib/components/ui/common/AlertContainer.svelte';
  import ContextMenu from '$lib/components/ui/common/ContextMenu.svelte';

  // Children prop for Svelte 5
  let { children }: { children: any } = $props();

  // Effect to establish WebSocket connection (runs once)
  $effect(() => {
    if (browser) {
      websocketStore.connect();
      
      return () => {
        // This cleanup runs when the component is destroyed
        websocketStore.disconnect();
      };
    }
    return () => {}; // No-op for server-side
  });
  
  // Separate effect to handle incoming messages (doesn't trigger reconnection)
  $effect(() => {
    if (browser) {
      const message = websocketStore.message;
      if (message && message.type === 'sensor_data' && message.data) {
        sensorDataManager.updateSensorData(message.data);
      }
    }
  });

  function handleContextMenuAction(_event: 'context-action', detail: { action: string }) {
    console.log('Context menu action dispatched:', detail.action);
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
  {@render children()}
</main>

<style>
  :global(.reduce-motion *) {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
</style>
