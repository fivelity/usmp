\`\`\`typescriptreact file="client/src/lib/components/WidgetInspector.svelte"
[v0-no-op-code-block-prefix]<script lang="ts">
  import { selectedWidgetConfigs } from '$lib/stores';
  import { selectedWidgets } from '$lib/stores/data/widgets';
  import { widgetUtils } from '$lib/stores/data/widgets';
  import { availableSensors } from '$lib/stores';
  import type { ExtendedGaugeType } from '$lib/types/widgets';
  import type { GaugeSettings, Widget } from '$lib/types';
  import { ColorPicker, RangeSlider, ToggleSwitch, Button } from '$lib/components/ui/common';
  import SystemStatusInspector from '../SystemStatusInspector.svelte';

  const gaugeTypes: { value: ExtendedGaugeType; label: string; description: string }[] = [
    { value: 'text', label: 'Text Value', description: 'Simple text display' },
    { value: 'radial', label: 'Radial Gauge', description: 'Circular progress gauge' },
    { value: 'linear', label: 'Linear Bar', description: 'Horizontal or vertical bar' },
    { value: 'graph', label: 'Time Graph', description: 'Historical data chart' },
    { value: 'image', label: 'Image Sequence', description: 'Custom image animation' },
    { value: 'glassmorphic', label: 'Glassmorphic', description: 'Modern glass effect gauge' }
  ];

  const selectedWidget = $derived(() => Object.values($selectedWidgetConfigs)[0] as Widget | undefined);
  const isMultipleSelection = $derived(() => Object.keys($selectedWidgetConfigs).length > 1);

  function handleGaugeTypeChange(type: ExtendedGaugeType) {
    const widget = selectedWidget();
    if (widget && typeof widget.id === 'string') {
      widgetUtils.updateWidget(widget.id, { config: { ...(widget.config || {}), gauge_type: type } });
    }
  }

  function handleGaugeSettingsChange(settings: Partial<GaugeSettings>) {
    const widget = selectedWidget();
    if (widget && typeof widget.id === 'string') {
      widgetUtils.updateWidget(widget.id, { config: { ...(widget.config || {}), gauge_settings: { ...((widget.config && widget.config.gauge_settings) || {}), ...settings } } });
    }
  }

  // Helper function to get current gauge setting value
  function getGaugeSetting(key: keyof GaugeSettings, defaultValue: any = undefined) {
    const widget = selectedWidget();
    const settings = widget?.config?.gauge_settings as Partial<GaugeSettings> | undefined;
    if (settings && typeof settings === 'object' && settings !== null) {
      return settings[key] ?? defaultValue;
    }
    return defaultValue;
  }

  // Helper function to get config property
  function getConfigProp<T = unknown>(key: string, defaultValue: T = undefined as T) {
    const widget = selectedWidget();
    return (widget?.config?.[key] ?? defaultValue) as T;
  }
</script>

<div class="inspector-container">
  {#if !selectedWidget()}
    <div class="empty-state">
      <div class="empty-icon">
        <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <h3>No Widget Selected</h3>
      <p>Select a widget to configure its properties</p>
    </div>
  {:else if isMultipleSelection()}
    <div class="empty-state">
      <div class="empty-icon">
        <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
      </div>
      <h3>Multiple Widgets Selected</h3>
      <p>Select a single widget to edit its properties</p>
      <div class="multi-actions">
        <Button variant="outline" onClick={() => widgetUtils.lockWidgets($selectedWidgets.filter((w: Widget) => typeof w.id === 'string').map((w: Widget) => w.id as string))}>
          Lock All
        </Button>
        <Button variant="outline" onClick={() => widgetUtils.unlockWidgets($selectedWidgets.filter((w: Widget) => typeof w.id === 'string').map((w: Widget) => w.id as string))}>
          Unlock All
        </Button>
      </div>
    </div>
  {:else}
    <div class="inspector-content">
      <!-- Header -->
      <div class="inspector-header">
        <h2>Widget Properties</h2>
        <div class="widget-id">ID: {selectedWidget()?.id}</div>
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
            value={getConfigProp('sensor_id', '')}
            onchange={(e) => { const id = selectedWidget()?.id; if (typeof id === 'string') widgetUtils.updateWidget(id, { config: { ...(selectedWidget()?.config || {}), sensor_id: e.currentTarget.value } }); }}
          >
            <option value="">Select a sensor...</option>
            {#each $availableSensors as sensor}
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
            value={selectedWidget()?.config?.gauge_type ?? ''}
            onchange={(e) => { const id = selectedWidget()?.id; if (typeof id === 'string') handleGaugeTypeChange(e.currentTarget.value as ExtendedGaugeType); }}
          >
            {#each gaugeTypes as gaugeType}
              <option value={gaugeType.value}>{gaugeType.label}</option>
            {/each}
          </select>
          <div class="form-help">
            {gaugeTypes.find(g => g.value === (selectedWidget()?.config?.gauge_type ?? ''))?.description}
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
            checked={getConfigProp('show_label', false)}
            onchange={(e) => { const id = selectedWidget()?.id; if (typeof id === 'string') widgetUtils.updateWidget(id, { config: { ...(selectedWidget()?.config || {}), show_label: e } }); }}
          />
        </div>

        <!-- Custom Label -->
        {#if getConfigProp('show_label', false)}
          <div class="form-group">
            <label for="custom-label">Custom Label</label>
            <input
              id="custom-label"
              type="text"
              class="form-input"
              placeholder="Leave empty to use sensor name"
              value={getConfigProp('custom_label', '')}
              oninput={(e) => { const id = selectedWidget()?.id; if (typeof id === 'string') widgetUtils.updateWidget(id, { config: { ...(selectedWidget()?.config || {}), custom_label: e.currentTarget.value || undefined } }); }}
            />
          </div>
        {/if}

        <!-- Show Unit Toggle -->
        <div class="form-group">
          <ToggleSwitch
            label="Show Unit"
            checked={getConfigProp('show_unit', false)}
            onchange={(e) => { const id = selectedWidget()?.id; if (typeof id === 'string') widgetUtils.updateWidget(id, { config: { ...(selectedWidget()?.config || {}), show_unit: e } }); }}
          />
        </div>

        <!-- Custom Unit -->
        {#if getConfigProp('show_unit', false)}
          <div class="form-group">
            <label for="custom-unit">Custom Unit</label>
            <input
              id="custom-unit"
              type="text"
              class="form-input"
              placeholder="Leave empty to use sensor unit"
              value={getConfigProp('custom_unit', '')}
              oninput={(e) => { const id = selectedWidget()?.id; if (typeof id === 'string') widgetUtils.updateWidget(id, { config: { ...(selectedWidget()?.config || {}), custom_unit: e.currentTarget.value || undefined } }); }}
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
            <label for="pos-x">X Position</label>
            <input
              id="pos-x"
              type="number"
              class="form-input"
              value={selectedWidget()?.config?.pos_x ?? 0}
              oninput={(e) => { const id = selectedWidget()?.id; if (typeof id === 'string') widgetUtils.updateWidget(id, { config: { ...(selectedWidget()?.config || {}), pos_x: parseInt(e.currentTarget.value) || 0 } }); }}
            />
          </div>
          <div class="form-group">
            <label for="pos-y">Y Position</label>
            <input
              id="pos-y"
              type="number"
              class="form-input"
              value={selectedWidget()?.config?.pos_y ?? 0}
              oninput={(e) => { const id = selectedWidget()?.id; if (typeof id === 'string') widgetUtils.updateWidget(id, { config: { ...(selectedWidget()?.config || {}), pos_y: parseInt(e.currentTarget.value) || 0 } }); }}
            />
          </div>
          <div class="form-group">
            <label for="width">Width</label>
            <input
              id="width"
              type="number"
              class="form-input"
              min="50"
              value={selectedWidget()?.width}
              oninput={(e) => widgetUtils.updateWidget(selectedWidget()?.id, { width: parseInt(e.currentTarget.value) || 100 })}
            />
          </div>
          <div class="form-group">
            <label for="height">Height</label>
            <input
              id="height"
              type="number"
              class="form-input"
              min="50"
              value={selectedWidget()?.height}
              oninput={(e) => widgetUtils.updateWidget(selectedWidget()?.id, { height: parseInt(e.currentTarget.value) || 100 })}
            />
          </div>
        </div>
        <div class="form-group">
          <label for="z-index">Z-Index</label>
          <input
            id="z-index"
            type="number"
            class="form-input"
            value={selectedWidget()?.config?.z_index ?? 0}
            oninput={(e) => { const id = selectedWidget()?.id; if (typeof id === 'string') widgetUtils.updateWidget(id, { config: { ...(selectedWidget()?.config || {}), z_index: parseInt(e.currentTarget.value) || 0 } }); }}
          />
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
            description="Locked widgets cannot be moved or resized in edit mode"
            checked={getConfigProp('is_locked', false)}
            onchange={(e) => { const id = selectedWidget()?.id; if (typeof id === 'string') widgetUtils.updateWidget(id, { config: { ...(selectedWidget()?.config || {}), is_locked: e } }); }}
          />
        </div>

        <div class="form-group">
          <label for="z-index">Z-Index (Layer)</label>
          <input
            id="z-index"
            type="number"
            class="form-input"
            value={selectedWidget()?.z_index}
            oninput={(e) => widgetUtils.updateWidget(selectedWidget()?.id, { z_index: parseInt(e.currentTarget.value) || 0 })}
          />
          <div class="form-help">Higher values appear on top</div>
        </div>
      </div>

      <!-- Gauge-Specific Settings -->
      {#if selectedWidget()?.gauge_type === 'radial'}
        <div class="section">
          <h3 class="section-title">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" />
              <path d="M12 6v6l4 2" />
            </svg>
            Radial Gauge Settings
          </h3>
          
          <div class="form-group">
            <RangeSlider
              label="Stroke Width"
              min={2}
              max={30}
              step={1}
              value={getGaugeSetting('stroke_width', 12)}
              unit="px"
              onchange={(e) => handleGaugeSettingsChange({ stroke_width: e.detail })}
            />
          </div>

          <div class="form-group">
            <ColorPicker
              label="Primary Color"
              value={getGaugeSetting('color_primary', '#3b82f6')}
              onchange={(e) => handleGaugeSettingsChange({ color_primary: e.detail })}
            />
          </div>

          <div class="form-group">
            <ColorPicker
              label="Secondary Color"
              value={getGaugeSetting('color_secondary', '#e5e7eb')}
              onchange={(e) => handleGaugeSettingsChange({ color_secondary: e.detail })}
            />
          </div>

          <div class="form-group">
            <ToggleSwitch
              label="Show Glow Effect"
              checked={getGaugeSetting('show_glow', true)}
              onchange={(e) => handleGaugeSettingsChange({ show_glow: e.detail })}
            />
          </div>

          <div class="form-group">
            <RangeSlider
              label="Animation Duration"
              min={200}
              max={2000}
              step={100}
              value={getGaugeSetting('animation_duration', 800)}
              unit="ms"
              onchange={(e) => handleGaugeSettingsChange({ animation_duration: e.detail })}
            />
          </div>
        </div>

      {:else if selectedWidget()?.gauge_type === 'linear'}
        <div class="section">
          <h3 class="section-title">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Linear Gauge Settings
          </h3>
          
          <div class="form-group">
            <label for="orientation-select">Orientation</label>
            <select
              id="orientation-select"
              class="form-select"
              value={getGaugeSetting('orientation', 'horizontal')}
              onchange={(e) => handleGaugeSettingsChange({ orientation: e.currentTarget.value })}
            >
              <option value="horizontal">Horizontal</option>
              <option value="vertical">Vertical</option>
            </select>
          </div>

          <div class="form-group">
            <ToggleSwitch
              label="Show Scale"
              checked={getGaugeSetting('show_scale', true)}
              onchange={(e) => handleGaugeSettingsChange({ show_scale: e.detail })}
            />
          </div>

          <div class="form-group">
            <ToggleSwitch
              label="Show Gradient"
              checked={getGaugeSetting('show_gradient', true)}
              onchange={(e) => handleGaugeSettingsChange({ show_gradient: e.detail })}
            />
          </div>

          <div class="form-group">
            <RangeSlider
              label="Bar Height"
              min={8}
              max={40}
              step={2}
              value={getGaugeSetting('bar_height', 20)}
              unit="px"
              onchange={(e) => handleGaugeSettingsChange({ bar_height: e.detail })}
            />
          </div>

          <div class="form-group">
            <ColorPicker
              label="Primary Color"
              value={getGaugeSetting('color_primary', '#3b82f6')}
              onchange={(e) => handleGaugeSettingsChange({ color_primary: e.detail })}
            />
          </div>

          <div class="form-group">
            <ColorPicker
              label="Secondary Color"
              value={getGaugeSetting('color_secondary', '#e5e7eb')}
              onchange={(e) => handleGaugeSettingsChange({ color_secondary: e.detail })}
            />
          </div>
        </div>

      {:else if selectedWidget()?.gauge_type === 'graph'}
        <div class="section">
          <h3 class="section-title">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Graph Settings
          </h3>
          
          <div class="form-group">
            <RangeSlider
              label="Time Range"
              min={10}
              max={300}
              step={10}
              value={getGaugeSetting('time_range', 60)}
              unit="s"
              onchange={(e) => handleGaugeSettingsChange({ time_range: e.detail })}
            />
          </div>

          <div class="form-group">
            <ColorPicker
              label="Line Color"
              value={getGaugeSetting('line_color', '#3b82f6')}
              onchange={(e) => handleGaugeSettingsChange({ line_color: e.detail })}
            />
          </div>

          <div class="form-group">
            <ToggleSwitch
              label="Fill Area"
              checked={getGaugeSetting('fill_area', false)}
              onchange={(e) => handleGaugeSettingsChange({ fill_area: e.detail })}
            />
          </div>

          <div class="form-group">
            <ToggleSwitch
              label="Show Points"
              checked={getGaugeSetting('show_points', false)}
              onchange={(e) => handleGaugeSettingsChange({ show_points: e.detail })}
            />
          </div>

          <div class="form-group">
            <ToggleSwitch
              label="Show Grid"
              checked={getGaugeSetting('show_grid', true)}
              onchange={(e) => handleGaugeSettingsChange({ show_grid: e.detail })}
            />
          </div>

          <div class="form-group">
            <ToggleSwitch
              label="Animate Entry"
              checked={getGaugeSetting('animate_entry', true)}
              onchange={(e) => handleGaugeSettingsChange({ animate_entry: e.detail })}
            />
          </div>
        </div>

      {:else if selectedWidget()?.gauge_type === 'glassmorphic'}
        <div class="section">
          <h3 class="section-title">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4h4a2 2 0 002-2V5z" />
            </svg>
            Glassmorphic Settings
          </h3>
          
          <div class="form-group">
            <label for="glassmorphic-style-select">Gauge Style</label>
            <select
              id="glassmorphic-style-select"
              class="form-select"
              value={getGaugeSetting('style', 'radial')}
              onchange={(e) => handleGaugeSettingsChange({ style: e.currentTarget.value })}
            >
              <option value="radial">Radial</option>
              <option value="linear">Linear</option>
              <option value="ring">Ring</option>
            </select>
          </div>

          <div class="form-group">
            <RangeSlider
              label="Glow Intensity"
              min={0}
              max={1}
              step={0.1}
              value={getGaugeSetting('glow_intensity', 0.5)}
              onchange={(e) => handleGaugeSettingsChange({ glow_intensity: e.detail })}
            />
          </div>

          <div class="form-group">
            <RangeSlider
              label="Blur Level"
              min={0}
              max={1}
              step={0.1}
              value={getGaugeSetting('blur_level', 0.3)}
              onchange={(e) => handleGaugeSettingsChange({ blur_level: e.detail })}
            />
          </div>

          <div class="form-group">
            <RangeSlider
              label="Transparency"
              min={0.1}
              max={1}
              step={0.1}
              value={getGaugeSetting('transparency', 0.8)}
              onchange={(e) => handleGaugeSettingsChange({ transparency: e.detail })}
            />
          </div>

          <div class="form-group">
            <ColorPicker
              label="Primary Color"
              value={getGaugeSetting('color_primary', '#3b82f6')}
              onchange={(e) => handleGaugeSettingsChange({ color_primary: e.detail })}
            />
          </div>

          <div class="form-group">
            <ColorPicker
              label="Secondary Color"
              value={getGaugeSetting('color_secondary', '#8b5cf6')}
              onchange={(e) => handleGaugeSettingsChange({ color_secondary: e.detail })}
            />
          </div>
        </div>
      {:else if selectedWidget()?.gauge_type === 'system_status'}
        <SystemStatusInspector 
          widget={selectedWidget()}
          on:update-widget={(e) => widgetUtils.updateWidget(selectedWidget()?.id, e.detail.updates)}
        />
      {/if}

      <!-- Actions Section -->
      <div class="section">
        <h3 class="section-title">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
          </svg>
          Actions
        </h3>
        
        <div class="action-buttons">
          <Button variant="outline" onclick={() => widgetUtils.duplicateWidget(selectedWidget()?.id)}>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            Duplicate
          </Button>
          
          <Button variant="outline" onclick={() => widgetUtils.bringToFront(selectedWidget()?.id)}>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
            </svg>
            Bring to Front
          </Button>
          
          <Button variant="outline" onclick={() => widgetUtils.sendToBack(selectedWidget()?.id)}>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8V20m0 0l4-4m-4 4l-4-4M7 4v12m0 0l-4-4m4 4l4-4" />
            </svg>
            Send to Back
          </Button>
          
          <Button variant="danger" onclick={() => widgetUtils.removeWidget(selectedWidget()?.id)}>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Delete
          </Button>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .inspector-container {
    height: 100%;
    background: #f8fafc;
    border-left: 1px solid #e2e8f0;
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
    color: #64748b;
  }

  .empty-icon {
    margin-bottom: 1rem;
    opacity: 0.5;
  }

  .empty-state h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.125rem;
    font-weight: 600;
    color: #334155;
  }

  .empty-state p {
    margin: 0;
    font-size: 0.875rem;
  }

  .multi-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
  }

  .inspector-content {
    padding: 1.5rem;
  }

  .inspector-header {
    margin-bottom: 2rem;
  }

  .inspector-header h2 {
    margin: 0 0 0.25rem 0;
    font-size: 1.25rem;
    font-weight: 700;
    color: #1e293b;
  }

  .widget-id {
    font-size: 0.75rem;
    color: #64748b;
    font-family: monospace;
  }

  .section {
    margin-bottom: 2rem;
    background: white;
    border-radius: 0.75rem;
    padding: 1.5rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  }

  .section-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0 0 1.5rem 0;
    font-size: 1rem;
    font-weight: 600;
    color: #334155;
  }

  .form-group {
    margin-bottom: 1.5rem;
  }

  .form-group:last-child {
    margin-bottom: 0;
  }

  .form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-size: 0.875rem;
    font-weight: 500;
    color: #374151;
  }

  .form-input,
  .form-select {
    width: 100%;
    padding: 0.5rem 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    background: white;
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  .form-input:focus,
  .form-select:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  .form-help {
    margin-top: 0.25rem;
    font-size: 0.75rem;
    color: #6b7280;
  }

  .action-buttons {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
  }
</style>
