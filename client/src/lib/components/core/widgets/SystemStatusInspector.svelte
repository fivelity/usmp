<script lang="ts">
  import type { WidgetConfig } from '$lib/types';
  import type { SystemStatusConfig, SystemMetric } from '$lib/types/widgets';
  import { availableSensors } from '$lib/stores';
  import { Button, ToggleSwitch, RangeSlider } from '$lib/components/ui';

  interface Props {
    widget: WidgetConfig;
    updateWidget: (updates: Partial<WidgetConfig>) => void;
  }

  let { widget, updateWidget }: Props = $props();

  // Widget-specific config is now stored in widget.gauge_settings
  // const config = widget.config as SystemStatusConfig; // Old line, using widget.gauge_settings directly in finalConfig

  // Default configuration
  const defaultConfig: SystemStatusConfig = {
    layout: 'compact',
    columns: 2,
    metrics: [],
    show_icons: true,
    show_labels: true,
    show_values: true,
    show_units: true,
    use_status_colors: true,
    warning_threshold: 75,
    critical_threshold: 90,
    animate_changes: true,
    update_animation: 'fade'
  };

  let finalConfig = $derived({ ...defaultConfig, ...(widget.gauge_settings || {}) });

  function updateConfig(updates: Partial<SystemStatusConfig>) {
    const newSettings = { ...finalConfig, ...updates };
    updateWidget({ gauge_settings: newSettings });
  }

  function addMetric() {
    const newMetric: SystemMetric = {
      id: `metric_${Date.now()}`,
      sensor_id: '',
      label: 'New Metric',
      format: 'number'
    };
    
    updateConfig({
      metrics: [...finalConfig.metrics, newMetric]
    });
  }

  function updateMetric(index: number, updates: Partial<SystemMetric>) {
    const newMetrics = [...finalConfig.metrics];
    const existingMetric = newMetrics[index];

    if (existingMetric === undefined) {
      console.warn(`SystemStatusInspector: updateMetric called with invalid index ${index} for metrics array of length ${newMetrics.length}`);
      return;
    }

    newMetrics[index] = {
      // Immutable field
      id: existingMetric.id,

      // Required fields: use update if defined, otherwise keep existing
      sensor_id: updates.sensor_id !== undefined ? updates.sensor_id : existingMetric.sensor_id,
      label: updates.label !== undefined ? updates.label : existingMetric.label,

      // Optional fields: if key exists in updates, use its value (even if undefined, to allow unsetting)
      // otherwise, keep existing value.
      icon: 'icon' in updates ? updates.icon : existingMetric.icon,
      unit: 'unit' in updates ? updates.unit : existingMetric.unit,
      min_value: 'min_value' in updates ? updates.min_value : existingMetric.min_value,
      max_value: 'max_value' in updates ? updates.max_value : existingMetric.max_value,
      warning_threshold: 'warning_threshold' in updates ? updates.warning_threshold : existingMetric.warning_threshold,
      critical_threshold: 'critical_threshold' in updates ? updates.critical_threshold : existingMetric.critical_threshold,
      format: 'format' in updates ? updates.format : existingMetric.format,
    };

    updateWidget({ gauge_settings: { ...finalConfig, metrics: newMetrics } });
  }

  function removeMetric(index: number) {
    const newMetrics = finalConfig.metrics.filter((_, i) => i !== index);
    updateWidget({ gauge_settings: { ...finalConfig, metrics: newMetrics } });
  }

  function moveMetric(index: number, direction: 'up' | 'down') {
    const newMetrics = [...finalConfig.metrics];
    const targetIndex = direction === 'up' ? index - 1 : index + 1;

    // Ensure both current index and target index are within bounds
    if (index >= 0 && index < newMetrics.length && 
        targetIndex >= 0 && targetIndex < newMetrics.length) {
      
      const itemAtIndex = newMetrics[index];
      const itemAtTargetIndex = newMetrics[targetIndex];

      // Perform the swap only if both items are defined (type guard)
      if (itemAtIndex !== undefined && itemAtTargetIndex !== undefined) {
        [newMetrics[index], newMetrics[targetIndex]] = [itemAtTargetIndex, itemAtIndex];
        updateWidget({ gauge_settings: { ...finalConfig, metrics: newMetrics } });
      } else {
        // This case should ideally not be reached if indices are correct and array has no undefined holes.
        console.error('SystemStatusInspector: Attempted to move an undefined metric item.');
      }
    }
  }

  function handleLayoutChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    updateConfig({ layout: target.value as SystemStatusConfig['layout'] });
  }

  function handleAnimationChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    updateConfig({ update_animation: target.value as SystemStatusConfig['update_animation'] });
  }
</script>

<div class="system-status-inspector">
  <!-- Layout Settings -->
  <div class="section">
    <h3 class="section-title">Layout Settings</h3>
    
    <div class="form-group">
      <label for="layout-select">Layout Style</label>
      <select
        id="layout-select"
        class="form-select"
        value={finalConfig.layout}
        onchange={handleLayoutChange}
      >
        <option value="compact">Compact</option>
        <option value="detailed">Detailed</option>
        <option value="minimal">Minimal</option>
      </select>
    </div>

    <div class="form-group">
      <RangeSlider
        label="Columns"
        min={1}
        max={4}
        step={1}
        value={finalConfig.columns}
        on:valuechange={(event) => updateConfig({ columns: event.detail as number })}
      />
    </div>
  </div>

  <!-- Display Options -->
  <div class="section">
    <h3 class="section-title">Display Options</h3>
    
    <div class="form-group">
      <ToggleSwitch
        label="Show Icons"
        checked={finalConfig.show_icons}
        on:change={(event) => updateConfig({ show_icons: event.detail as boolean })}
      />
    </div>

    <div class="form-group">
      <ToggleSwitch
        label="Show Labels"
        checked={finalConfig.show_labels}
        on:change={(event) => updateConfig({ show_labels: event.detail as boolean })}
      />
    </div>

    <div class="form-group">
      <ToggleSwitch
        label="Show Values"
        checked={finalConfig.show_values}
        on:change={(event) => updateConfig({ show_values: event.detail as boolean })}
      />
    </div>

    <div class="form-group">
      <ToggleSwitch
        label="Show Units"
        checked={finalConfig.show_units}
        on:change={(event) => updateConfig({ show_units: event.detail as boolean })}
      />
    </div>
  </div>

  <!-- Status Colors -->
  <div class="section">
    <h3 class="section-title">Status Colors</h3>
    
    <div class="form-group">
      <ToggleSwitch
        label="Use Status Colors"
        checked={finalConfig.use_status_colors}
        on:change={(event) => updateConfig({ use_status_colors: event.detail as boolean })}
      />
    </div>

    {#if finalConfig.use_status_colors}
      <div class="form-group">
        <RangeSlider
          label="Warning Threshold"
          min={0}
          max={100}
          step={5}
          value={finalConfig.warning_threshold}
          unit="%"
          onValueChange={(value) => updateConfig({ warning_threshold: value })}
        />
      </div>

      <div class="form-group">
        <RangeSlider
          label="Critical Threshold"
          min={0}
          max={100}
          step={5}
          value={finalConfig.critical_threshold}
          unit="%"
          onValueChange={(value) => updateConfig({ critical_threshold: value })}
        />
      </div>
    {/if}
  </div>

  <!-- Animation Settings -->
  <div class="section">
    <h3 class="section-title">Animation</h3>
    
    <div class="form-group">
      <ToggleSwitch
        label="Animate Changes"
        checked={finalConfig.animate_changes}
        on:change={(event) => updateConfig({ animate_changes: event.detail as boolean })}
      />
    </div>

    {#if finalConfig.animate_changes}
      <div class="form-group">
        <label for="animation-select">Animation Type</label>
        <select
          id="animation-select"
          class="form-select"
          value={finalConfig.update_animation}
          onchange={handleAnimationChange}
        >
          <option value="fade">Fade</option>
          <option value="slide">Slide</option>
          <option value="pulse">Pulse</option>
          <option value="none">None</option>
        </select>
      </div>
    {/if}
  </div>

  <!-- Metrics Configuration -->
  <div class="section">
    <h3 class="section-title">
      Metrics Configuration
      <Button variant="outline" size="sm" on:click={addMetric}>
        Add Metric
      </Button>
    </h3>

    {#if finalConfig.metrics.length === 0}
      <div class="empty-metrics">
        <p>No metrics configured. Click "Add Metric" to get started.</p>
      </div>
    {:else}
      <div class="metrics-list">
        {#each finalConfig.metrics as metric, index (metric.id)}
          <div class="metric-config">
            <div class="metric-header">
              <span class="metric-index">{index + 1}</span>
              <input
                type="text"
                class="metric-label-input"
                bind:value={metric.label}
                placeholder="Metric Label"
                oninput={(e) => updateMetric(index, { label: e.currentTarget.value })}
              />
              <div class="metric-actions">
                <button
                  class="action-btn"
                  onclick={() => moveMetric(index, 'up')}
                  disabled={index === 0}
                  title="Move Up"
                  aria-label="Move metric up"
                >
                  ↑
                </button>
                <button
                  class="action-btn"
                  onclick={() => moveMetric(index, 'down')}
                  disabled={index === finalConfig.metrics.length - 1}
                  title="Move Down"
                  aria-label="Move metric down"
                >
                  ↓
                </button>
                <button
                  class="action-btn danger"
                  onclick={() => removeMetric(index)}
                  title="Remove"
                  aria-label="Remove metric"
                >
                  ×
                </button>
              </div>
            </div>

            <div class="metric-fields">
              <div class="form-group">
                <label for="sensor-select-{index}">Sensor</label>
                <select
                  id="sensor-select-{index}"
                  class="form-select"
                  bind:value={metric.sensor_id}
                  onchange={(e) => updateMetric(index, { sensor_id: e.currentTarget.value })}
                >
                  <option value="">Select sensor...</option>
                  {#each availableSensors as sensor}
                    <option value={sensor.id}>{sensor.name} ({sensor.category})</option>
                  {/each}
                </select>
              </div>

              <div class="form-group">
                <label for="format-select-{index}">Format</label>
                <select
                  id="format-select-{index}"
                  class="form-select"
                  bind:value={metric.format}
                  onchange={(e) => updateMetric(index, { format: e.currentTarget.value as SystemMetric['format'] })}
                >
                  <option value="number">Number</option>
                  <option value="percentage">Percentage</option>
                  <option value="temperature">Temperature</option>
                  <option value="frequency">Frequency</option>
                  <option value="bytes">Bytes</option>
                </select>
              </div>

              <div class="form-group">
                <label for="icon-input-{index}">Icon (emoji)</label>
                <input
                  id="icon-input-{index}"
                  type="text"
                  class="form-input"
                  bind:value={metric.icon}
                  placeholder="📊"
                  maxlength="2"
                  oninput={(e) => updateMetric(index, { icon: e.currentTarget.value })}
                />
              </div>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>

<style>
  .system-status-inspector {
    padding: 1rem;
  }

  .section {
    margin-bottom: 2rem;
    background: white;
    border-radius: 0.5rem;
    padding: 1rem;
    border: 1px solid #e5e7eb;
  }

  .section-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 0 0 1rem 0;
    font-size: 1rem;
    font-weight: 600;
    color: #374151;
  }

  .form-group {
    margin-bottom: 1rem;
  }

  .form-group:last-child {
    margin-bottom: 0;
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
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    font-size: 0.875rem;
  }

  .form-input:focus,
  .form-select:focus {
    outline: 2px solid #3b82f6;
    outline-offset: 2px;
  }

  .empty-metrics {
    text-align: center;
    color: #6b7280;
    font-style: italic;
    padding: 2rem;
  }

  .metrics-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .metric-config {
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    padding: 1rem;
    background: #f9fafb;
  }

  .metric-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .metric-index {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    background: #3b82f6;
    color: white;
    border-radius: 50%;
    font-size: 0.75rem;
    font-weight: 600;
    flex-shrink: 0;
  }

  .metric-label-input {
    flex: 1;
    padding: 0.375rem 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    font-weight: 500;
  }

  .metric-actions {
    display: flex;
    gap: 0.25rem;
  }

  .action-btn {
    width: 24px;
    height: 24px;
    border: 1px solid #d1d5db;
    border-radius: 0.25rem;
    background: white;
    color: #6b7280;
    font-size: 0.75rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .action-btn:hover:not(:disabled) {
    background: #f3f4f6;
    color: #374151;
  }

  .action-btn:focus {
    outline: 2px solid #3b82f6;
    outline-offset: 2px;
  }

  .action-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .action-btn.danger {
    color: #ef4444;
  }

  .action-btn.danger:hover:not(:disabled) {
    background: #fef2f2;
    color: #dc2626;
  }

  .metric-fields {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0.75rem;
  }

  @media (max-width: 768px) {
    .metric-fields {
      grid-template-columns: 1fr;
    }
  }
</style>
