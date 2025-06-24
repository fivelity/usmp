<script lang="ts">
  import type { SystemEvent } from '$lib/types';
  import type { WidgetConfig } from '$lib/types/widgets';
  
  type StatusType = SystemEvent['type'];
  
  // Accept both SystemStatus-specific props and general widget props
  const {
    // Widget-specific props
    widget = undefined,
    label = '',
    
    // SystemStatus-specific props
    status = 'info' as StatusType,
    message = '',
    details = undefined,
    timestamp = new Date().toISOString(),
    showTimestamp = true,
    dismissible = false,
    onDismiss = undefined
  } = $props<{
    // Widget props (optional, for compatibility with WidgetContent)
    widget?: WidgetConfig;
    sensorData?: any;
    config?: any;
    value?: number;
    unit?: string;
    min?: number;
    max?: number;
    label?: string;
    
    // SystemStatus-specific props
    status?: StatusType;
    message?: string;
    details?: unknown;
    timestamp?: string;
    showTimestamp?: boolean;
    dismissible?: boolean;
    onDismiss?: () => void;
  }>();
  
  // Derive actual status from widget data if available
  let actualStatus = $derived(widget?.gauge_settings?.status || status);
  let actualMessage = $derived(widget?.gauge_settings?.message || message || label || 'System Status');
  let actualDetails = $derived(widget?.gauge_settings?.details || details);
  
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
  <div class="system-status {statusColors[actualStatus as StatusType]} theme-transition">
    <div class="flex-between">
      <div class="flex items-center gap-2">
        <span class="status-icon" aria-hidden="true">{statusIcons[actualStatus as StatusType]}</span>
        <div>
          <p class="message">{actualMessage}</p>
          {#if actualDetails}
            <p class="details text-small">{actualDetails}</p>
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
    padding: 0.75rem;
    border-radius: 0.5rem;
    margin-bottom: 0.5rem;
  }
  
  .status-icon {
    font-size: 1.125rem;
    font-weight: 700;
  }
  
  .message {
    font-weight: 500;
  }
  
  .details {
    margin-top: 0.25rem;
  }
  
  .timestamp {
    opacity: 0.75;
  }
  
  .dismiss-btn {
    font-size: 1.125rem;
    font-weight: 700;
    opacity: 0.75;
    transition: opacity 0.2s;
    padding: 0.25rem 0.5rem;
  }

  .dismiss-btn:hover {
    opacity: 1;
  }
</style> 