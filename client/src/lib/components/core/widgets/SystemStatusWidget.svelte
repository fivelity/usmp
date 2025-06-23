<script lang="ts">
  import type { WidgetConfig, SensorData } from '$lib/types';
  import type { SystemStatusConfig, SystemMetric, StatusLevel } from '$lib/types/widgets';
  import { sensorStore as sensorDataStore } from '$lib/stores/data/sensors.svelte';
  import { get } from 'svelte/store';
  
  const {
    widget,
    isSelected = false,
    onfoo = undefined
  } = $props<{
    widget: WidgetConfig;
    isSelected?: boolean;
    onfoo?: () => void;
  }>();

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

  // Reactive derived state
  let config = $derived(widget.gauge_settings as SystemStatusConfig);
  let finalConfig = $derived({ ...defaultConfig, ...config });
  let currentSensorData = $derived(get(sensorDataStore) as Record<string, any>);

  interface ProcessedMetric extends SystemMetric {
    current_value: number;
    formatted_value: string;
    status: StatusLevel;
    sensor_data?: SensorData;
  }

  let processedMetrics = $state<ProcessedMetric[]>([]);

  // Icon mapping for common metrics
  const iconMap: Record<string, string> = {
    cpu: '🔥',
    gpu: '🎮',
    memory: '💾',
    temperature: '🌡️',
    fan: '🌀',
    power: '⚡',
    network: '🌐',
    disk: '💿',
    voltage: '🔋',
    frequency: '📡'
  };

  function formatValue(value: number, format: string, unit?: string): string {
    if (isNaN(value)) return 'N/A';
    let displayUnit = unit || '';

    switch (format) {
      case 'percentage':
        return `${value.toFixed(1)}%`;
      case 'temperature':
        return `${value.toFixed(1)}${displayUnit || '°C'}`; // Default to °C if unit not provided
      case 'frequency':
        return `${value.toFixed(0)} ${displayUnit || 'MHz'}`;
      case 'bytes':
        return formatBytes(value);
      default:
        return `${value.toFixed(1)}${displayUnit ? ' ' + displayUnit : ''}`;
    }
  }

  function formatBytes(bytes: number): string {
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return '0 B';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    if (i < 0 || i >= sizes.length) return `${bytes.toFixed(1)} B`; // Fallback for very small/large numbers
    return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`;
  }

  function getStatusLevel(value: number, metric: SystemMetric, currentFinalConfig: SystemStatusConfig): StatusLevel {
    if (!currentFinalConfig.use_status_colors) return 'normal';
    if (isNaN(value)) return 'normal'; // Treat NaN as normal to avoid errors

    const warningThreshold = metric.warning_threshold ?? currentFinalConfig.warning_threshold;
    const criticalThreshold = metric.critical_threshold ?? currentFinalConfig.critical_threshold;

    if (value >= criticalThreshold) return 'critical';
    if (value >= warningThreshold) return 'warning';
    return 'normal';
  }

  function getStatusColor(status: StatusLevel): string {
    switch (status) {
      case 'critical': return '#ef4444'; // red-500
      case 'warning': return '#f59e0b'; // amber-500
      case 'normal': return '#10b981'; // emerald-500
      default: return '#6b7280'; // gray-500
    }
  }

  function getMetricIcon(metric: SystemMetric): string {
    if (metric.icon) return metric.icon;

    const searchText = (metric.label + metric.sensor_id).toLowerCase();
    for (const [key, icon] of Object.entries(iconMap)) {
      if (searchText.includes(key)) return icon;
    }

    return '📊'; // Default icon
  }

  let animationClass: string = $derived(finalConfig.animate_changes ? `animate-${finalConfig.update_animation}` : '');

  $effect(() => {
    processedMetrics = (finalConfig.metrics || []).map(metric => {
      const sensor = currentSensorData[metric.sensor_id];
      const value = sensor?.value ?? 0;
      const numValue = typeof value === 'string' ? parseFloat(value) : Number(value);

      return {
        ...metric,
        current_value: numValue,
        formatted_value: formatValue(numValue, metric.format || 'number', metric.unit),
        status: getStatusLevel(numValue, metric, finalConfig),
        sensor_data: sensor
      };
    });
  });

  $effect(() => {
    if (processedMetrics && processedMetrics.length > 0) {
      // console.log('Processed metrics updated:', processedMetrics);
    }
  });
</script>

<div
  class="system-status-widget"
  class:selected={isSelected}
  class:compact={finalConfig.layout === 'compact'}
  class:detailed={finalConfig.layout === 'detailed'}
  class:minimal={finalConfig.layout === 'minimal'}
  style="--columns: {finalConfig.columns};"
>
  {#if !processedMetrics || processedMetrics.length === 0}
    <div class="empty-state">
      <div class="empty-icon">📊</div>
      <div class="empty-text">No metrics configured</div>
      <div class="empty-hint">Add metrics in the widget inspector</div>
    </div>
  {:else}
    <div class="metrics-grid">
      {#each processedMetrics as metric (metric.id)}
        <div
          class="metric-item {animationClass}"
          style="--status-color: {getStatusColor(metric.status)}"
          onclick={() => { if (onfoo) onfoo(); }}
          role="button"
          tabindex="0"
          onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') { if (onfoo) onfoo(); } }}
        >
          {#if finalConfig.show_icons}
            <div class="metric-icon" aria-hidden="true">
              {getMetricIcon(metric)}
            </div>
          {/if}

          <div class="metric-content">
            {#if finalConfig.show_labels}
              <div class="metric-label" title={metric.label}>{metric.label}</div>
            {/if}

            {#if finalConfig.show_values}
              <div class="metric-value">
                {metric.formatted_value}
                {#if finalConfig.show_units && metric.unit && !metric.formatted_value.includes(metric.unit)}
                  <span class="metric-unit">{metric.unit}</span>
                {/if}
              </div>
            {/if}
          </div>

          {#if finalConfig.use_status_colors}
            <div class="status-indicator" style="background-color: {getStatusColor(metric.status)}" aria-hidden="true"></div>
          {/if}
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .system-status-widget {
    width: 100%;
    height: 100%;
    padding: 12px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 8px;
    border: 1px solid #e5e7eb; /* gray-200 */
    overflow: hidden;
    position: relative;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  }

  .system-status-widget.selected {
    border-color: #3b82f6; /* blue-500 */
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #6b7280; /* gray-500 */
    text-align: center;
  }

  .empty-icon {
    font-size: 2rem;
    margin-bottom: 8px;
    opacity: 0.5;
  }

  .empty-text {
    font-weight: 500;
    margin-bottom: 4px;
  }

  .empty-hint {
    font-size: 0.75rem;
    opacity: 0.7;
  }

  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(var(--columns, 2), 1fr); /* Default to 2 columns if --columns is not set */
    gap: 8px;
    height: 100%;
  }

  .metric-item {
    display: flex;
    align-items: center;
    padding: 8px;
    background: rgba(248, 250, 252, 0.8); /* slate-50 with opacity */
    border-radius: 6px;
    border: 1px solid #f1f5f9; /* slate-100 */
    position: relative;
    transition: all 0.2s ease;
    cursor: default; /* Default cursor, can be changed if items are interactive */
  }
  .metric-item[role="button"]:hover,
  .metric-item[role="button"]:focus {
    background: rgba(241, 245, 249, 0.9); /* slate-100 with opacity */
    transform: translateY(-1px);
    outline: 1px solid #3b82f6; /* blue-500 for focus */
  }


  .metric-icon {
    font-size: 1.2rem;
    margin-right: 8px;
    flex-shrink: 0;
  }

  .metric-content {
    flex: 1;
    min-width: 0; /* Prevents overflow issues with text-ellipsis */
  }

  .metric-label {
    font-size: 0.75rem;
    color: #6b7280; /* gray-500 */
    font-weight: 500;
    margin-bottom: 2px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .metric-value {
    font-size: 0.875rem;
    font-weight: 600;
    color: #1f2937; /* gray-800 */
    display: flex;
    align-items: baseline;
    gap: 2px;
  }

  .metric-unit {
    font-size: 0.75rem;
    color: #6b7280; /* gray-500 */
    font-weight: 400;
  }

  .status-indicator {
    position: absolute;
    top: 4px;
    right: 4px;
    width: 6px;
    height: 6px;
    border-radius: 50%;
  }

  /* Layout variations */
  .compact .metrics-grid {
    gap: 6px;
  }

  .compact .metric-item {
    padding: 6px;
  }

  .compact .metric-icon {
    font-size: 1rem;
    margin-right: 6px;
  }

  .compact .metric-label {
    font-size: 0.7rem;
  }

  .compact .metric-value {
    font-size: 0.8rem;
  }

  .detailed .metric-item {
    flex-direction: column;
    align-items: flex-start;
    padding: 12px;
  }

  .detailed .metric-icon {
    margin-right: 0;
    margin-bottom: 6px;
    font-size: 1.5rem;
  }

  .detailed .metric-content {
    width: 100%;
  }

  .detailed .metric-label {
    font-size: 0.8rem;
    margin-bottom: 4px;
  }

  .detailed .metric-value {
    font-size: 1rem;
  }

  .minimal .metric-item {
    padding: 4px 6px;
    background: transparent;
    border: none;
  }

  .minimal .metric-icon {
    display: none;
  }

  .minimal .metric-label {
    display: none;
  }

  .minimal .metric-value {
    font-size: 0.8rem;
    justify-content: center;
  }

  /* Animations */
  .animate-fade {
    animation: fadeIn 0.3s ease;
  }

  .animate-slide {
    animation: slideIn 0.3s ease;
  }

  .animate-pulse {
    animation: pulse 0.5s ease;
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  @keyframes slideIn {
    from { transform: translateY(-10px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }

  @keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
  }

  /* Responsive adjustments */
  @media (max-width: 300px) {
    .metrics-grid {
      grid-template-columns: 1fr; /* Single column on very small screens */
    }
  }
</style>
