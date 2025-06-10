<script lang="ts">
  import '../app.css';
  import { onMount, onDestroy } from 'svelte';
  import type { SensorSourceFromAPI } from '$lib/types';
  import { initializeStores, connectionStatus, storeUtils, sensorSources, hardwareTree, availableSensors } from '$lib/stores';
  import { visualSettingsOriginal as visualSettings } from '$lib/stores/core/visual.svelte';
  import { sensorUtils } from '$lib/stores/sensorData.svelte';
  
  import { websocketService } from '$lib/services/websocket';
  import { apiService } from '$lib/services/api';

  
  let websocketUnsubscribe: () => void;

  onMount(async () => {
    // Initialize stores when the app starts
    initializeStores();
    
    // Fetch initial sensor sources and hardware tree
    await loadInitialSensorData();
    
    // Start WebSocket connection (only in browser)
    if (typeof window !== 'undefined') {
      try {
        websocketService.connect();
        
        // Subscribe to WebSocket messages
        websocketUnsubscribe = websocketService.subscribe((message: any) => {
          if (message.type === 'sensor_data' && message.data) {
            storeUtils.updateSensorData(message.data);
          }
        });

        // Update connection status
        websocketService.onConnectionChange((status: 'connecting' | 'connected' | 'disconnected' | 'error') => {
          connectionStatus.set(status);
        });
      } catch (error) {
        console.error('Failed to establish WebSocket connection:', error);
        connectionStatus.set('error');
      }
    }
    

  });

  // Effect for applying visual settings
  $effect(() => {
    if (typeof document !== 'undefined' && $visualSettings) {
      const settings = $visualSettings;
      const root = document.documentElement;
      root.style.setProperty('--materiality', settings.materiality.toString());
      root.style.setProperty('--information-density', settings.information_density.toString());
      root.style.setProperty('--animation-level', settings.animation_level.toString());
      root.style.setProperty('--grid-size', `${settings.grid_size}px`);
      
      // Apply theme class
      document.body.className = document.body.className.replace(/theme-\w+/, '');
      document.body.classList.add(`theme-${settings.color_scheme}`);
      
      // Apply font family
      root.style.setProperty('--font-family', settings.font_family);
      
      // Apply reduced motion preference
      if (settings.reduce_motion) {
        document.body.classList.add('reduce-motion');
      } else {
        document.body.classList.remove('reduce-motion');
      }
    }
  });

  onDestroy(() => {
    
    if (websocketUnsubscribe) {
      websocketUnsubscribe();
    }
    
    websocketService.disconnect();
  });

  async function loadInitialSensorData() {
    const sourcesResponse = await apiService.getSensors();
    console.log('[Layout] Sensor Sources Response:', sourcesResponse);
    if (sourcesResponse.success && sourcesResponse.data) {
      sensorUtils.updateSensorSources(sourcesResponse.data.sources as unknown as Record<string, SensorSourceFromAPI>);
      console.log('[Layout] Updated sensorSources store:', sensorSources);
      
      const lhmUpdatedSource = sourcesResponse.data.sources['librehardware_updated'];
      if (lhmUpdatedSource && lhmUpdatedSource.active) {
        const treeResponse = await apiService.getHardwareTree();
        console.log('[Layout] Hardware Tree Response:', treeResponse);
        if (treeResponse.success && treeResponse.data) {
          sensorUtils.updateHardwareTree(treeResponse.data.hardware);
          console.log('[Layout] Updated hardwareTree store:', hardwareTree);
        }
      }
    }
    // Trigger a log of available sensors after initial load
    console.log('[Layout] Initial availableSensors:', availableSensors);
  }
</script>

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
