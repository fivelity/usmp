<script lang="ts">
  import { onMount } from 'svelte';
  import { 
    editMode, 
    widgetArray, 
    selectedWidgets, 
    storeUtils, 
    availableSensors,
    uiUtils, // Added uiUtils
  } from '$lib/stores';
  import { sensorUtils } from '$lib/stores/sensorData.svelte';
  import { configService, type AppConfig } from '$lib/services/configService';
  import { apiService } from '$lib/services/api';
  import { initializationService, type InitializationResult } from '$lib/services/initializationService';
  import TopBar from '$lib/components/core/layout/TopBar.svelte';
  import LeftSidebar from '$lib/components/core/layout/LeftSidebar.svelte';
  import RightSidebar from '$lib/components/core/layout/RightSidebar.svelte';
  import DashboardCanvas from '$lib/components/core/dashboard/DashboardCanvas.svelte';

  import SnapGuides from '$lib/components/core/dashboard/SnapGuides.svelte';
  import type { WidgetConfig, SensorSourceFromAPI } from '$lib/types';
  // import { uiUtils } from '$lib/services/uiService'; // Path needs to be verified


  let initializationResult = $state<InitializationResult | null>(null);
  let isLoading = $state(true);
  let showInitializationDetails = $state(false);
  let leftSidebarVisible = $state(true);
  let rightSidebarVisible = $state(false);
  let hasInitialized = $state(false);
  let config = $state<AppConfig>();

  onMount(async () => {
    console.log('🚀 Ultimate Sensor Monitor starting...');
    
    try {
      // Load configuration first
      config = await configService.loadConfig();
      console.log('[App] Configuration loaded:', config);
      
      // Set UI defaults from config
      leftSidebarVisible = config.ui.autoOpenLeftSidebar;
      rightSidebarVisible = config.ui.autoOpenRightSidebar;
      uiUtils.setEditMode(config.ui.defaultEditMode);
      
      // Initialize visual settings from config
      storeUtils.updateVisualSettings({
        grid_size: config.canvas.defaultGridSize,
        snap_to_grid: config.canvas.defaultSnapToGrid,
        show_grid: config.canvas.defaultShowGrid
      });

      // Attempt proper initialization with timeout and fallback
      console.log('[App] Attempting full initialization...');
      try {
        // Set a reasonable timeout for initialization
        const initTimeout = new Promise((_, reject) => 
          setTimeout(() => reject(new Error('Initialization timeout')), 5000)
        );
        
        initializationResult = await Promise.race([
          initializationService.initialize(),
          initTimeout
        ]) as InitializationResult;
        
        console.log('[App] Full initialization completed:', initializationResult);
      } catch (error) {
        console.warn('[App] Full initialization failed, using fallback:', error);
        // Fallback to working offline mode
        initializationResult = {
          success: true,
          mode: 'offline' as const,
          errors: [],
          warnings: [`Full initialization failed: ${error}. Running in offline mode.`]
        };
      }
      
      if (initializationResult.success) {
        console.log(`✓ Application initialized in ${initializationResult.mode} mode`);
        if (initializationResult.warnings.length > 0) {
          console.warn('Initialization warnings:', initializationResult.warnings);
        }

        // Skip complex data loading for now to avoid hanging
        console.log('[App] Skipping complex data loading - app should now be ready');
        
        // Simple fallback to show empty dashboard
        console.log('[App] Dashboard ready for use');
      } else {
        console.error('❌ Application initialization failed:', initializationResult.errors);
      }
    } catch (error) {
      console.error('💥 Critical initialization error:', error);
      initializationResult = {
        success: false,
        mode: 'offline',
        errors: [`Critical error: ${error}`],
        warnings: []
      };
    } finally {
      isLoading = false;
      hasInitialized = true;
    }

    // Set up keyboard shortcuts
    setupKeyboardShortcuts();
  });

  async function loadSensorData() {
    console.log('[App] Attempting to load real sensor data...');
    try {
      const sensorsResult = await apiService.getSensors();
      
      if (sensorsResult.success && sensorsResult.data?.sources) {
        console.log('[App] Real sensor data loaded successfully');
        sensorUtils.updateSensorSources(sensorsResult.data.sources as unknown as Record<string, SensorSourceFromAPI>);
      } else {
        console.warn('[App] Failed to load sensor data:', sensorsResult.error);
        showEmptyState();
      }
    } catch (error) {
      console.error('[App] Error loading sensor data:', error);
      showEmptyState();
    }
  }

  async function loadDemoData() {
    console.log('[App] Loading demo data...');
    const { demoSensorSources, demoSensorData, demoWidgets } = await import('$lib/demoData');
    
    storeUtils.updateSensorSources(demoSensorSources as unknown as Record<string, SensorSourceFromAPI>);
    storeUtils.updateSensorData(demoSensorData);
    
    // Load demo widgets
    demoWidgets.forEach(widget => {
      (storeUtils as any).addWidget(widget);
    });
    
    console.log(`[App] Demo data loaded: ${demoWidgets.length} widgets`);
  }

  function showEmptyState() {
    console.log('[App] Showing empty state - no sensor data available');
    storeUtils.updateSensorSources({});
    storeUtils.updateSensorData({});
    (storeUtils as any).clearAllWidgets();
  }

  function createInitialWidgetsFromSensors() {
    const sensors = availableSensors;
    
    if (!sensors || sensors.length === 0) {
      console.log('[App] No sensors available for widget creation');
      return;
    }

    console.log(`[App] Creating initial widgets from ${sensors.length} available sensors`);
    
    // Group sensors by category
    const sensorsByCategory = sensors.reduce((acc: Record<string, typeof sensors>, sensor: typeof sensors[number]) => {
      if (!acc[sensor.category]) {
        acc[sensor.category] = [];
      }
      acc[sensor.category]!.push(sensor);
      return acc;
    }, {} as Record<string, typeof sensors>);

    // Widget creation configuration from config file
    const widgetConfig = config.widgets;
    let currentX = 50;
    let currentY = 50;
    
    const advancePosition = () => {
      currentX += widgetConfig.widgetSpacing;
      if (currentX > window.innerWidth - widgetConfig.defaultWidgetWidth) {
        currentX = 50;
        currentY += widgetConfig.widgetRowHeight;
      }
    };

    // Create widgets for each category (limited by config)
    Object.entries(sensorsByCategory).forEach(([category, categorySensors]) => {
      const maxWidgets = config.data.maxWidgetsPerCategory;
      const sensorsToUse = (categorySensors as typeof sensors).slice(0, maxWidgets);
      
      sensorsToUse.forEach((sensor: typeof sensors[number]) => {
        const widget: WidgetConfig = {
          id: `${category}_widget_${sensor.id}`,
          type: 'gauge',
          name: sensor.name,
          x: currentX,
          y: currentY,
          width: widgetConfig.defaultWidgetWidth,
          height: widgetConfig.defaultWidgetHeight,
          config: { sensorId: sensor.id },
        };
        
        console.log(`[App] Created ${category} widget:`, widget.id);
        (storeUtils as any).addWidget(widget);
        advancePosition();
      });
    });

    console.log(`[App] Created ${$widgetArray.length} initial widgets`);
  }

  function setupKeyboardShortcuts() {
    const handleKeydown = (event: KeyboardEvent) => {
      // Escape key - clear selection and hide context menu
      if (event.key === 'Escape') {
        storeUtils.clearSelection();
        storeUtils.hideContextMenu();
      }
      
      // Toggle edit mode with 'E' key
      if (event.key === 'e' || event.key === 'E') {
        if (event.ctrlKey || event.metaKey) {
          event.preventDefault();
          uiUtils.toggleEditMode();
        }
      }
      
      // Delete selected widgets with Delete key
      if (event.key === 'Delete' && editMode === 'edit') {
        if (selectedWidgets.size > 0) {
          selectedWidgets.forEach((id: string) => storeUtils.removeWidget(id));
          storeUtils.clearSelection(); // Clear selection after deleting
        }
      }
    };

    document.addEventListener('keydown', handleKeydown);
    return () => document.removeEventListener('keydown', handleKeydown);
  }

  function toggleLeftSidebar() {
    leftSidebarVisible = !leftSidebarVisible;
  }

  function toggleRightSidebar() {
    rightSidebarVisible = !rightSidebarVisible;
  }

</script>

<svelte:head>
  <title>Ultimate Sensor Monitor</title>
</svelte:head>

{#if isLoading}
  <!-- Loading Screen -->
  <div class="flex items-center justify-center min-h-screen bg-gray-900 text-white">
    <div class="text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
      <h2 class="text-xl font-semibold mb-2">Initializing Ultimate Sensor Monitor</h2>
      <p class="text-gray-400">Loading configuration and connecting to sensors...</p>
    </div>
  </div>
{:else if !initializationResult?.success}
  <!-- Error Screen -->
  <div class="flex items-center justify-center min-h-screen bg-gray-900 text-white p-8">
    <div class="max-w-2xl text-center">
      <div class="text-red-500 text-6xl mb-4">⚠️</div>
      <h2 class="text-2xl font-bold mb-4 text-red-400">Initialization Failed</h2>
      <p class="text-gray-300 mb-6">
        The application could not start properly. Please check the configuration and try again.
      </p>
      
      <div class="bg-gray-800 rounded-lg p-4 mb-6 text-left">
        <h3 class="font-semibold text-red-400 mb-2">Errors:</h3>
        <ul class="space-y-1">
          {#each initializationResult?.errors || [] as error}
            <li class="text-red-300">• {error}</li>
          {/each}
        </ul>
      </div>

      <div class="space-x-4">
        <button 
          class="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg transition-colors"
          onclick={() => window.location.reload()}
        >
          Retry
        </button>
        <button 
          class="bg-gray-600 hover:bg-gray-700 px-6 py-2 rounded-lg transition-colors"
          onclick={() => showInitializationDetails = !showInitializationDetails}
        >
          {showInitializationDetails ? 'Hide' : 'Show'} Details
        </button>
      </div>

      {#if showInitializationDetails}
        <div class="mt-6 bg-gray-800 rounded-lg p-4 text-left text-sm">
          <h4 class="font-semibold mb-2">Troubleshooting:</h4>
          <ul class="space-y-1 text-gray-400">
            <li>• Ensure the backend server is running on port 8100</li>
            <li>• Check if LibreHardwareMonitor.dll is in the project root</li>
            <li>• Verify that demo mode is enabled in settings.cfg if needed</li>
            <li>• Try running the server with administrator privileges</li>
          </ul>
        </div>
      {/if}
    </div>
  </div>
{:else}
  <!-- Main Application -->
  <div class="h-screen flex flex-col bg-gray-900 text-white overflow-hidden">
    <!-- Top Bar -->
    <TopBar
      showLeftSidebar={leftSidebarVisible}
      showRightSidebar={rightSidebarVisible}
      ontoggleLeftSidebar={toggleLeftSidebar}
      ontoggleRightSidebar={toggleRightSidebar}
    />
    
    <!-- Status Bar -->
    {#if initializationResult.mode === 'demo'}
      <div class="bg-yellow-600 text-yellow-100 px-4 py-2 text-sm text-center">
        ⚠️ Running in Demo Mode - No real sensor data available
      </div>
    {:else if initializationResult.warnings.length > 0}
      <div class="bg-orange-600 text-orange-100 px-4 py-2 text-sm text-center">
        ⚠️ {initializationResult.warnings.join(', ')}
      </div>
    {/if}

    <!-- Main Content -->
    <div class="flex-1 flex overflow-hidden">
      <!-- Left Sidebar -->
      {#if leftSidebarVisible}
        <div class="w-64 border-r border-gray-800">
          <LeftSidebar onclose={toggleLeftSidebar} />
        </div>
      {/if}
      
      <!-- Dashboard Canvas -->
      <main class="flex-1 relative">
        <DashboardCanvas />
        <SnapGuides
          calculateSnap={() => ({ x: 0, y: 0 })}
          on:snap={() => {}}
        />
      </main>
      
      <!-- Right Sidebar -->
      {#if rightSidebarVisible}
        <div class="w-80 border-l border-gray-800">
          <RightSidebar on:close={toggleRightSidebar} />
        </div>
      {/if}
    </div>

    <!-- Connection Status -->
    <!-- <ConnectionStatus
      status={connectionStatus}
      onRetry={() => apiService.testConnection()}
    /> -->
    
    <!-- Context Menu -->
    <!-- <ContextMenu
      show={contextMenu.show}
      x={contextMenu.x}
      y={contextMenu.y}
      items={contextMenu.items}
      target={contextMenu.target} 
      on:close={() => { /* uiUtils.hideContextMenu(); TODO: Fix uiUtils import and usage */ contextMenu.show = false; }}
    /> -->
  </div>
{/if}

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    overflow: hidden;
  }
</style>
