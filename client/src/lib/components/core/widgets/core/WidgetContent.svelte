<script lang="ts">
  import type { WidgetConfig } from '$lib/types/widgets';
  import { sensorDataManager } from '$lib/stores/data/sensors.svelte';
  
  // Import widget components
  import TextGauge from '../../gauges/TextGauge.svelte';
  import RadialGauge from '../../gauges/RadialGauge.svelte';
  import LinearGauge from '../../gauges/LinearGauge.svelte';
  import GraphGauge from '../../gauges/GraphGauge.svelte';
  import ImageSequenceGauge from '../../gauges/ImageSequenceGauge.svelte';
  import GlassmorphicGauge from '../../gauges/GlassmorphicGauge.svelte';
  import SystemStatus from '../SystemStatus.svelte';
  
  let { widget }: { widget: WidgetConfig } = $props();
  
  // Get sensor data for this widget
  let sensorData = $derived(() => {
    if (!widget.sensor_id) return undefined;
    const allSensorData = sensorDataManager.getSensorData();
    return allSensorData[widget.sensor_id] || undefined;
  });
  
  // Performance optimization: only update when necessary
  let componentProps = $derived({
    widget,
    sensorData: sensorData(),
    config: widget.gauge_settings || {},
    // Additional props that gauge components might expect
    value: sensorData()?.value || 0,
    unit: sensorData()?.unit || '',
    min: sensorData()?.min_value || 0,
    max: sensorData()?.max_value || 100,
    label: widget.title || '',
    ...widget.gauge_settings
  });
</script>

<div class="widget-content" style="width: 100%; height: 100%;">
  {#if widget.gauge_type === 'text'}
    <TextGauge {...componentProps} />
  {:else if widget.gauge_type === 'radial'}
    <RadialGauge {...componentProps} />
  {:else if widget.gauge_type === 'linear'}
    <LinearGauge {...componentProps} />
  {:else if widget.gauge_type === 'graph'}
    <GraphGauge {...componentProps} />
  {:else if widget.gauge_type === 'image'}
    <ImageSequenceGauge {...componentProps} />
  {:else if widget.gauge_type === 'glassmorphic'}
    <GlassmorphicGauge {...componentProps} />
  {:else if widget.gauge_type === 'system_status'}
    <SystemStatus {...componentProps} />
  {:else}
    <div class="widget-fallback">
      <div class="fallback-icon">⚠️</div>
      <div class="fallback-text">
        Unknown widget type: {widget.gauge_type}
      </div>
    </div>
  {/if}
</div>

<style>
  .widget-content {
    position: relative;
    overflow: hidden;
    border-radius: inherit;
  }
  
  .widget-fallback {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: var(--theme-text-muted, #6b7280);
    text-align: center;
    padding: 1rem;
  }
  
  .fallback-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
  }
  
  .fallback-text {
    font-size: 0.875rem;
    line-height: 1.4;
  }
</style>
