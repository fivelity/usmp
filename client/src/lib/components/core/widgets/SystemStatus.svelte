<script lang="ts">
  import type { SystemEvent } from '$lib/types';
  
  type StatusType = SystemEvent['type'];
  
  const {
    status = 'info' as StatusType,
    message = '',
    details = undefined,
    timestamp = new Date().toISOString(),
    showTimestamp = true,
    dismissible = false,
    onDismiss = undefined
  } = $props<{
    status?: StatusType;
    message?: string;
    details?: unknown;
    timestamp?: string;
    showTimestamp?: boolean;
    dismissible?: boolean;
    onDismiss?: () => void;
  }>();
  
  let isVisible = $state(true);
  
  const statusIcons: Record<StatusType, string> = {
    success: '✓',
    warning: '⚠',
    error: '✕',
    info: 'ℹ'
  };
  
  const statusColors: Record<StatusType, string> = {
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

  $effect(() => {
    // Ensure status is a valid key
    if (!(status in statusIcons)) {
      console.error(`Invalid status type: ${status}`);
    }
  });
</script>

{#if isVisible}
  <div class="system-status {statusColors[status as StatusType]} theme-transition">
    <div class="flex-between">
      <div class="flex items-center gap-2">
        <span class="status-icon" aria-hidden="true">{statusIcons[status as StatusType]}</span>
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