<script lang="ts">
  import { connectionStatus } from '$lib/stores';
  import { Badge } from '$lib/components/ui/common';
  import type { ConnectionStatus } from '$lib/types/sensors';

  const { size = 'md' } = $props<{ size?: 'sm' | 'md' | 'lg' }>();

  let currentStatus: ConnectionStatus = $state('disconnected');
  $effect(() => {
    const unsubscribe = connectionStatus.subscribe(status => {
      currentStatus = status;
    });
    return unsubscribe;
  });

  let variant = $state<'success' | 'error' | 'warning' | 'default'>('default');
  $effect(() => {
    switch (currentStatus) {
      case 'connected':
        variant = 'success';
        break;
      case 'disconnected':
      case 'error':
        variant = 'error';
        break;
      case 'connecting':
        variant = 'warning';
        break;
      default:
        variant = 'default';
    }
  });

  const statusText = $derived(() => {
    switch (currentStatus) {
      case 'connected':
        return 'Connected';
      case 'disconnected':
        return 'Disconnected';
      case 'connecting':
        return 'Connecting...';
      case 'error':
        return 'Error';
      default:
        return 'Unknown';
    }
  });
</script>

<Badge variant={variant} size={size}>
  {statusText}
</Badge>
