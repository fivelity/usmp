<script lang="ts">
  import SystemStatus from './SystemStatus.svelte';
  import { systemStatus } from '$lib/stores/systemStatus';
  
  const {
    maxHeight = '400px',
    showClearButton = true
  } = $props<{
    maxHeight?: string;
    showClearButton?: boolean;
  }>();
  
  // Access the events store from systemStatus
  let events = systemStatus.events;
  
  function handleDismiss(id: string) {
    systemStatus.removeEvent(id);
  }
  
  function handleClear() {
    systemStatus.clearEvents();
  }
</script>

<div class="system-status-history card">
  <div class="flex-between mb-4">
    <h2 class="text-heading">System Status</h2>
    {#if showClearButton}
      <button 
        class="btn btn-secondary text-small"
        onclick={handleClear}
        disabled={$events.length === 0}
      >
        Clear History
      </button>
    {/if}
  </div>
  
  <div class="status-list" style="max-height: {maxHeight};">
    {#if $events.length === 0}
      <p class="text-small text-center text-text-muted">No system events to display</p>
    {:else}
      {#each $events as event (event.id)}
        <SystemStatus
          status={event.type}
          message={event.message}
          timestamp={new Date(event.timestamp).toISOString()}
          dismissible={true}
          onDismiss={() => handleDismiss(event.id)}
        />
      {/each}
    {/if}
  </div>
</div>

<style>
  .system-status-history {
    width: 100%;
  }
  
  .status-list {
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    scrollbar-width: thin;
    scrollbar-color: var(--theme-border) transparent;
  }
  
  .status-list::-webkit-scrollbar {
    width: 6px;
  }
  
  .status-list::-webkit-scrollbar-track {
    background: transparent;
  }
  
  .status-list::-webkit-scrollbar-thumb {
    background-color: var(--theme-border);
    border-radius: 3px;
  }
</style>
