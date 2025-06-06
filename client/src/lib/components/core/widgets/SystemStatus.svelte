<script lang="ts">
  import type { SystemEvent } from '$lib/types';
  
  export let status: SystemEvent['type'] = 'info';
  export let message: string = '';
  export let details: any = undefined;
  export let timestamp: string = new Date().toISOString();
  export let showTimestamp: boolean = true;
  export let dismissible: boolean = false;
  export let onDismiss: (() => void) | undefined = undefined;
  
  let isVisible = $state(true);
  
  const statusIcons = {
    success: '✓',
    warning: '⚠',
    error: '✕',
    info: 'ℹ'
  };
  
  const statusColors = {
    success: 'status-success',
    warning: 'status-warning',
    error: 'status-error',
    info: 'status-info'
  };
  
  function formatTimestamp(isoString: string): string {
    return new Date(isoString).toLocaleTimeString();
  }
  
  function handleDismiss() {
    if (dismissible && onDismiss) {
      isVisible = false;
      onDismiss();
    }
  }
</script>

{#if isVisible}
  <div class="system-status {statusColors[status]} theme-transition">
    <div class="flex-between">
      <div class="flex items-center gap-2">
        <span class="status-icon" aria-hidden="true">{statusIcons[status]}</span>
        <div>
          <p class="message">{message}</p>
          {#if details}
            <p class="details text-small">{details}</p>
          {/if}
        </div>
      </div>
      
      <div class="flex items-center gap-2">
        {#if showTimestamp}
          <span class="timestamp text-small">{formatTimestamp(timestamp)}</span>
        {/if}
        
        {#if dismissible}
          <button 
            class="dismiss-btn focus-ring" 
            onclick={handleDismiss}
            aria-label="Dismiss status message"
          >
            ×
          </button>
        {/if}
      </div>
    </div>
  </div>
{/if}

<style>
  .system-status {
    @apply p-3 rounded-lg mb-2;
  }
  
  .status-icon {
    @apply text-lg font-bold;
  }
  
  .message {
    @apply font-medium;
  }
  
  .details {
    @apply mt-1;
  }
  
  .timestamp {
    @apply opacity-75;
  }
  
  .dismiss-btn {
    @apply text-lg font-bold opacity-75 hover:opacity-100 transition-opacity;
    padding: 0.25rem 0.5rem;
  }
</style> 