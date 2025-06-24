<script lang="ts">
  import { selectedWidgets, availableSensors, widgets } from '$lib/stores';
  import { widgetUtils } from '$lib/stores/data/widgets.svelte';
  import type { GaugeType, WidgetConfig } from '$lib/types';
  import { ToggleSwitch, Button } from '$lib/components/ui';

  const gaugeTypes: { value: GaugeType; label: string; description: string }[] = [
    { value: 'text', label: 'Text Value', description: 'Simple text display' },
    { value: 'radial', label: 'Radial Gauge', description: 'Circular progress gauge' },
    { value: 'linear', label: 'Linear Bar', description: 'Horizontal or vertical bar' },
    { value: 'graph', label: 'Time Graph', description: 'Historical data chart' },
    { value: 'image', label: 'Image Sequence', description: 'Custom image animation' },
    { value: 'glassmorphic', label: 'Glassmorphic', description: 'Modern glass effect gauge' }
  ];

  // Create derived values from selected widgets
  let selectedWidgetConfigs = $derived(
    Array.from(selectedWidgets).map(id => widgets[id]).filter(Boolean)
  );
  let selectedWidget = $derived(selectedWidgetConfigs[0] as WidgetConfig);
  let isMultipleSelection = $derived(selectedWidgetConfigs.length > 1);

  function updateWidget(updates: Partial<WidgetConfig>) {
    if (selectedWidget) {
      widgetUtils.updateWidget(selectedWidget.id, updates);
    }
  }

  function updateGaugeType(value: string) {
    updateWidget({ gauge_type: value as GaugeType });
  }

  // Commented out unused functions - can be removed if not needed
  // function updateGaugeSettings(key: string, value: any) {
  //   if (selectedWidget) {
  //     const newSettings = { ...selectedWidget.gauge_settings, [key]: value };
  //     updateWidget({ gauge_settings: newSettings });
  //   }
  // }

  // // Helper function to get current gauge setting value
  // function getGaugeSetting(key: string, defaultValue: any = undefined) {
  //   return selectedWidget?.gauge_settings?.[key] ?? defaultValue;
  // }
</script>

<div class="inspector-container">
  {#if !selectedWidget}
    <div class="empty-state">
      <div class="empty-icon">
        <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <h3>No Widget Selected</h3>
      <p>Select a widget to configure its properties</p>
    </div>
  {:else if isMultipleSelection}
    <div class="empty-state">
      <div class="empty-icon">
        <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
      </div>
      <h3>Multiple Widgets Selected</h3>
      <p>Select a single widget to edit its properties</p>
      <div class="multi-actions">
        <Button variant="outline" onclick={() => widgetUtils.lockWidgets(Array.from(selectedWidgets))}>
          Lock All
        </Button>
        <Button variant="outline" onclick={() => widgetUtils.unlockWidgets(Array.from(selectedWidgets))}>
          Unlock All
        </Button>
      </div>
    </div>
  {:else}
    <div class="inspector-content">
      <!-- Header -->
      <div class="inspector-header">
        <h2>Widget Properties</h2>
        <div class="widget-id">ID: {selectedWidget.id}</div>
      </div>

      <!-- Basic Properties Section -->
      <div class="section">
        <h3 class="section-title">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c-.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          Basic Properties
        </h3>
        
        <!-- Sensor Selection -->
        <div class="form-group">
          <label for="sensor-select">Sensor Data Source</label>
          <select
            id="sensor-select"
            class="form-select"
            value={selectedWidget.sensor_id}
            onchange={(e) => updateWidget({ sensor_id: e.currentTarget.value })}
          >
            <option value="">Select a sensor...</option>
            {#each availableSensors() as sensor}
              <option value={sensor.id}>{sensor.name} ({sensor.category})</option>
            {/each}
          </select>
        </div>

        <!-- Gauge Type -->
        <div class="form-group">
          <label for="gauge-type-select">Gauge Type</label>
          <select
            id="gauge-type-select"
            class="form-select"
            value={selectedWidget.gauge_type}
            onchange={(e) => updateGaugeType(e.currentTarget.value)}
          >
            {#each gaugeTypes as gaugeType}
              <option value={gaugeType.value}>{gaugeType.label}</option>
            {/each}
          </select>
          <div class="form-help">
            {gaugeTypes.find(g => g.value === selectedWidget.gauge_type)?.description}
          </div>
        </div>
      </div>

      <!-- Display Options Section -->
      <div class="section">
        <h3 class="section-title">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          Display Options
        </h3>
        
        <!-- Show Label Toggle -->
        <div class="form-group">
        <ToggleSwitch
          label="Show Label"
          checked={selectedWidget.show_label ?? false}
          onchange={(value) => updateWidget({ show_label: value })}
        />
        </div>

        <!-- Custom Label -->
        {#if selectedWidget.show_label}
          <div class="form-group">
            <label for="custom-label">Custom Label</label>
            <input
              id="custom-label"
              type="text"
              class="form-input"
              placeholder="Leave empty to use sensor name"
              value={selectedWidget.custom_label || ''}
              oninput={(e) => updateWidget({ custom_label: e.currentTarget.value || undefined })}
            />
          </div>
        {/if}

        <!-- Show Unit Toggle -->
        <div class="form-group">
          <ToggleSwitch
            label="Show Unit"
            checked={selectedWidget.show_unit ?? false}
            onchange={(value) => updateWidget({ show_unit: value })}
          />
        </div>

        <!-- Custom Unit -->
        {#if selectedWidget.show_unit}
          <div class="form-group">
            <label for="custom-unit">Custom Unit</label>
            <input
              id="custom-unit"
              type="text"
              class="form-input"
              placeholder="Leave empty to use sensor unit"
              value={selectedWidget.custom_unit || ''}
              oninput={(e) => updateWidget({ custom_unit: e.currentTarget.value || undefined })}
            />
          </div>
        {/if}
      </div>

      <!-- Position & Size Section -->
      <div class="section">
        <h3 class="section-title">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
          </svg>
          Position & Size
        </h3>
        
        <div class="form-grid">
          <div class="form-group">
            <label for="x-position">X Position</label>
            <input
              id="x-position"
              type="number"
              class="form-input"
              value={selectedWidget.pos_x}
              oninput={(e) => updateWidget({ pos_x: parseInt(e.currentTarget.value) || 0 })}
            />
          </div>
          <div class="form-group">
            <label for="y-position">Y Position</label>
            <input
              id="y-position"
              type="number"
              class="form-input"
              value={selectedWidget.pos_y}
              oninput={(e) => updateWidget({ pos_y: parseInt(e.currentTarget.value) || 0 })}
            />
          </div>
          <div class="form-group">
            <label for="width">Width</label>
            <input
              id="width"
              type="number"
              class="form-input"
              min="50"
              value={selectedWidget.width}
              oninput={(e) => updateWidget({ width: parseInt(e.currentTarget.value) || 100 })}
            />
          </div>
          <div class="form-group">
            <label for="height">Height</label>
            <input
              id="height"
              type="number"
              class="form-input"
              min="50"
              value={selectedWidget.height}
              oninput={(e) => updateWidget({ height: parseInt(e.currentTarget.value) || 100 })}
            />
          </div>
        </div>
      </div>

      <!-- Widget Behavior Section -->
      <div class="section">
        <h3 class="section-title">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          Widget Behavior
        </h3>
        
        <div class="form-group">
          <ToggleSwitch
            label="Lock Widget"
            checked={selectedWidget.locked ?? false}
            onchange={(value) => updateWidget({ locked: value })}
          />
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .inspector-container {
    height: 100%;
    overflow-y: auto;
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 2rem;
    text-align: center;
  }

  .empty-icon {
    color: var(--theme-text-muted);
    margin-bottom: 1rem;
  }

  .empty-state h3 {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--theme-text);
    margin-bottom: 0.5rem;
  }

  .empty-state p {
    font-size: 0.875rem;
    color: var(--theme-text-muted);
    margin-bottom: 1rem;
  }

  .multi-actions {
    display: flex;
    gap: 0.5rem;
  }

  .inspector-content {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .inspector-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
  }

  .inspector-header h2 {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--theme-text);
  }

  .widget-id {
    font-size: 0.75rem;
    color: var(--theme-text-muted);
  }

  .section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .section-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--theme-text);
    margin-bottom: 1rem;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .form-group label {
    display: block;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--theme-text);
  }

  .form-input,
  .form-select {
    width: 100%;
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
    border: 1px solid var(--theme-border);
    border-radius: 0.375rem;
    background-color: var(--theme-surface);
    color: var(--theme-text);
  }

  .form-input:focus,
  .form-select:focus {
    outline: none;
    box-shadow: 0 0 0 2px var(--theme-primary);
    border-color: transparent;
  }

  .form-help {
    font-size: 0.75rem;
    color: var(--theme-text-muted);
  }

  .form-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
</style>
