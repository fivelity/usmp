<script lang="ts">
  import type { SensorData } from '$lib/types';
  
  export let sensor: SensorData;
  export let icon: string | undefined = undefined;
  export let showLabel: boolean = true;
  export let showUnit: boolean = true;
  export let format: 'number' | 'percentage' | 'bytes' | 'temperature' = 'number';
  export let warningThreshold: number | undefined = undefined;
  export let criticalThreshold: number | undefined = undefined;
  export let animateChanges: boolean = true;
  
  let previousValue = $state(sensor.value);
  let isAnimating = $state(false);
  
  const formatValue = (value: number): string => {
    switch (format) {
      case 'percentage':
        return `${Math.round(value)}%`;
      case 'bytes':
        return formatBytes(value);
      case 'temperature':
        return `${Math.round(value)}°C`;
      default:
        return value.toLocaleString();
    }
  };
  
  const formatBytes = (bytes: number): string => {
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    let value = bytes;
    let unitIndex = 0;
    
    while (value >= 1024 && unitIndex < units.length - 1) {
      value /= 1024;
      unitIndex++;
    }
    
    return `${value.toFixed(1)} ${units[unitIndex]}`;
  };
  
  const getStatusClass = (value: number): string => {
    if (criticalThreshold && value >= criticalThreshold) {
      return 'status-error';
    }
    if (warningThreshold && value >= warningThreshold) {
      return 'status-warning';
    }
    return 'status-success';
  };
  
  $effect(() => {
    if (animateChanges && sensor.value !== previousValue) {
      isAnimating = true;
      setTimeout(() => {
        isAnimating = false;
      }, 500);
      previousValue = sensor.value;
    }
  });
</script>

<div class="metric-card card {animateChanges && isAnimating ? 'fade-in' : ''}">
  <div class="flex-between">
    {#if showLabel}
      <div class="flex items-center gap-2">
        {#if icon}
          <span class="text-xl" aria-hidden="true">{icon}</span>
        {/if}
        <span class="text-small">{sensor.name}</span>
      </div>
    {/if}
    
    {#if showUnit && sensor.unit}
      <span class="text-small text-text-muted">{sensor.unit}</span>
    {/if}
  </div>
  
  <div class="metric-value {getStatusClass(sensor.value)}">
    {formatValue(sensor.value)}
  </div>
  
  {#if sensor.min_value !== undefined && sensor.max_value !== undefined}
    <div class="metric-range">
      <div class="range-bar">
        <div 
          class="range-fill" 
          style="width: {((sensor.value - sensor.min_value) / (sensor.max_value - sensor.min_value)) * 100}%"
        />
      </div>
      <div class="flex-between text-small text-text-muted">
        <span>{formatValue(sensor.min_value)}</span>
        <span>{formatValue(sensor.max_value)}</span>
      </div>
    </div>
  {/if}
</div>

<style>
  .metric-card {
    @apply p-4;
  }
  
  .metric-value {
    @apply text-2xl font-bold mt-2;
  }
  
  .metric-range {
    @apply mt-3;
  }
  
  .range-bar {
    @apply h-1 bg-surface-elevated rounded-full overflow-hidden;
  }
  
  .range-fill {
    @apply h-full bg-primary transition-all duration-300;
  }
</style> 