<script lang="ts">
  import type { WidgetConfig } from '$lib/types/widgets';
  import type { SensorData } from '$lib/types';

  const { widget, sensorData } = $props<{
    widget: WidgetConfig;
    sensorData: SensorData | undefined;
  }>();

  // Get display value
  const displayValue = $derived(sensorData?.value ?? '--');
  const unit = $derived(widget.gauge_settings?.unit || sensorData?.unit || '');
  const sensorName = $derived(widget.title || sensorData?.name || 'Unknown Sensor');

  // Format the value based on its type
  const formattedValue = $derived(formatValue(displayValue));
  const validValue = $derived(displayValue !== null && displayValue !== undefined && displayValue !== '--' && displayValue !== '' && !Number.isNaN(displayValue));

  function formatValue(value: any): string {
    if (value === null || value === undefined || value === '--') {
      return '--';
    }
    
    if (typeof value === 'number') {
      if (Number.isInteger(value)) {
        return value.toString();
      } else {
        return value.toFixed(1);
      }
    }
    
    return value.toString();
  }

  // Get text size based on widget size and information density
  const fontSize = $derived(Math.min(widget.width / 6, widget.height / 3));
  const titleSize = $derived(Math.max(fontSize * 0.4, 12));
</script>

<div class="gauge-container text-center">
  <div class="flex flex-col h-full justify-center">
    <!-- Sensor Name -->
    {#if widget.gauge_settings?.show_label}
      <div 
        class="font-medium text-(--theme-text-muted) mb-1 truncate"
        style="font-size: {titleSize}px; line-height: 1.2;"
      >
        {sensorName}
      </div>
    {/if}

    <!-- Main Value -->
    <div class="flex-1 flex items-center justify-center">
      {#if validValue}
        <div 
          class="font-bold text-(--theme-text)"
          style="font-size: {fontSize}px; line-height: 1;"
        >
          {formattedValue}
        </div>
      {:else}
        <div class="font-bold text-(--theme-text-muted) opacity-60" style="font-size: {fontSize}px; line-height: 1;">
          --
        </div>
      {/if}
    </div>

    <!-- Unit -->
    {#if widget.gauge_settings?.show_unit && unit}
      <div 
        class="text-(--theme-text-muted) opacity-75 truncate"
        style="font-size: {titleSize}px; line-height: 1.2;"
      >
        {unit}
      </div>
    {/if}
  </div>
</div>

<style>
  .gauge-container {
    width: 100%;
    height: 100%;
    padding: 8px;
    background: var(--theme-surface);
    border-radius: 0.75rem; /* 12px */
    font-family: var(--font-family, sans-serif);
  }
  /* Ensure child text elements inherit the font by default */
  .gauge-container :global(div),
  .gauge-container :global(span) {
    font-family: inherit;
  }
</style>
