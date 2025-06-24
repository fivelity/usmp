<script lang="ts">
  interface Props {
    status: 'connected' | 'disconnected' | 'connecting' | 'error';
    isRetrying?: boolean;
    error?: string | null;
    lastUpdate?: string | null;
    sensorCount?: number;
  }

  let { status, isRetrying = false, error = null, lastUpdate = null, sensorCount = 0 }: Props = $props();

  function getStatusText() {
    switch (status) {
      case 'connected':
        return `Connected • ${sensorCount} sensors`;
      case 'connecting':
        return isRetrying ? 'Reconnecting...' : 'Connecting...';
      case 'error':
        return 'Connection Error';
      case 'disconnected':
        return 'Disconnected';
      default:
        return 'Unknown Status';
    }
  }

  function getStatusClass() {
    switch (status) {
      case 'connected':
        return 'bg-green-500 text-white';
      case 'connecting':
        return 'bg-yellow-500 text-white';
      case 'error':
        return 'bg-red-500 text-white';
      case 'disconnected':
        return 'bg-gray-500 text-white';
      default:
        return 'bg-gray-400 text-white';
    }
  }

  function getIndicatorClass() {
    switch (status) {
      case 'connected':
        return 'bg-green-400 animate-pulse';
      case 'connecting':
        return 'bg-yellow-400 animate-pulse';
      case 'error':
        return 'bg-red-400';
      case 'disconnected':
        return 'bg-gray-400';
      default:
        return 'bg-gray-300';
    }
  }
</script>

<div class="fixed top-4 right-4 z-50 max-w-sm">
  <div class="flex items-center gap-2 px-3 py-2 rounded-lg shadow-lg {getStatusClass()} text-sm font-medium">
    <div class="w-2 h-2 rounded-full {getIndicatorClass()}"></div>
    <span>{getStatusText()}</span>
    {#if lastUpdate}
      <span class="text-xs opacity-75">• {lastUpdate}</span>
    {/if}
  </div>
  
  {#if error}
    <div class="mt-2 px-3 py-2 bg-red-100 border border-red-300 rounded-lg text-red-800 text-xs">
      {error}
    </div>
  {/if}
</div>
