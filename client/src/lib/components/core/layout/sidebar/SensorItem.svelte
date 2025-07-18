<script lang="ts">
  import type { SensorReading } from '$lib/types/sensors';
  import { sensorDataManager } from '$lib/stores/sensorData.svelte';
  import { addWidget } from '$lib/stores/data/widgets.svelte';
  import type { WidgetConfig, ExtendedGaugeType } from '$lib/types';
  import { get } from 'svelte/store';
  import Dropdown from '$lib/components/ui/common/Dropdown.svelte';
  import Button from '$lib/components/ui/common/Button.svelte';

  let { sensor }: { sensor: SensorReading } = $props();

  const _allSensorDataMap = $derived(get(sensorDataManager.sensorDataStore));
  const currentData = $derived(_allSensorDataMap ? _allSensorDataMap[sensor.id] : undefined);

  function createWidget(sensor: SensorReading, gaugeType: ExtendedGaugeType) {
    const newWidgetConfig: WidgetConfig = {
      id: `widget_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      type: gaugeType,
      title: sensor.name || 'Sensor Widget',
      pos_x: Math.floor(Math.random() * 800),
      pos_y: Math.floor(Math.random() * 600),
      width: 200,
      height: 150,
      is_locked: false,
      gauge_type: gaugeType,
      gauge_settings: {}, // Default empty gauge settings
      sensor_id: sensor.id,
      custom_label: sensor.name, // Use sensor name as label
      custom_unit: sensor.unit,   // Use sensor unit
      style: {}, // Default empty style object
      // Add other required WidgetConfig properties with defaults:
      z_index: 0,
      is_visible: true,
      is_draggable: true,
      is_resizable: true,
      is_selectable: true,
      is_grouped: false,
      // title: sensor.name, // Optional: if title is distinct from custom_label
    };
    addWidget(newWidgetConfig);
  }

  function formatValue(value: any): string {
    if (typeof value === 'number') {
      return Number.isInteger(value) ? value.toString() : value.toFixed(1);
    }
    return value?.toString() || '--';
  }
</script>

<div
  class="sensor-item p-3 rounded-lg bg-(--theme-background) border border-(--theme-border) hover:border-(--theme-primary) transition-colors group"
  data-sensor-id={sensor.id}
>
  <div class="flex items-center justify-between">
    <div class="flex-1 overflow-hidden">
      <div class="font-medium text-sm text-(--theme-text) truncate" title={sensor.name}>
        {sensor.name}
      </div>
      <div class="text-xs text-(--theme-text-muted) truncate" title={sensor.id}>
        {sensor.id}
      </div>
    </div>
    <div class="text-right pl-2">
      <div class="font-mono text-sm font-semibold text-(--theme-text)">
        {formatValue(currentData?.value)} {sensor.unit}
      </div>
    </div>
    <div class="pl-2">
    <Dropdown position="bottom" align="end">
        {#snippet triggerSnippet()}
          <div class="p-1 cursor-pointer rounded-md hover:bg-(--theme-border)">
            +
          </div>
        {/snippet}
        {#snippet children()}
          <div class="p-2 bg-(--theme-surface-overlay) rounded-lg shadow-lg border border-(--theme-border) flex flex-col gap-1">
            <Button onClick={() => createWidget(sensor, 'text')}>Add Text</Button>
            <Button onClick={() => createWidget(sensor, 'radial')}>Add Radial</Button>
            <Button onClick={() => createWidget(sensor, 'linear')}>Add Linear</Button>
            <Button onClick={() => createWidget(sensor, 'graph')}>Add Graph</Button>
          </div>
        {/snippet}
      </Dropdown>
    </div>
  </div>

  {#if sensor.min_value != null && sensor.max_value != null && typeof currentData?.value === 'number'}
    {@const percentage = Math.min(100, Math.max(0, ((currentData.value - sensor.min_value) / (sensor.max_value - sensor.min_value)) * 100))}
    <div class="mt-2">
      <div class="w-full bg-(--theme-border) rounded-full h-1.5">
        <div
          class="bg-(--theme-primary) h-1.5 rounded-full transition-all duration-300"
          style="width: {percentage}%"
        ></div>
      </div>
      <div class="flex justify-between text-xs text-(--theme-text-muted) mt-1">
        <span>{sensor.min_value}</span>
        <span>{sensor.max_value}</span>
      </div>
    </div>
  {/if}
</div> 