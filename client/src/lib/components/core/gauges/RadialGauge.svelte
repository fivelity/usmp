<script lang="ts">
  import type { WidgetConfig } from '$lib/types/widgets';
  import type { SensorData } from '$lib/types';

  const { widget, sensorData } = $props<{
    widget: WidgetConfig;
    sensorData: SensorData | undefined;
  }>();

  // Get display value and calculate percentage
  const value = $derived(typeof sensorData?.value === 'number' ? sensorData.value : 0);
  const minValue = $derived(widget.gauge_settings?.min_value ?? sensorData?.min_value ?? 0);
  const maxValue = $derived(widget.gauge_settings?.max_value ?? sensorData?.max_value ?? 100);
  const percentage = $derived((maxValue !== minValue) ? Math.min(100, Math.max(0, ((value - minValue) / (maxValue - minValue)) * 100)) : 0);
  
  // Gauge settings with defaults
  const startAngle = $derived(widget.gauge_settings?.start_angle ?? -90);
  const endAngle = $derived(widget.gauge_settings?.end_angle ?? 270);
  const strokeWidth = $derived(widget.gauge_settings?.stroke_width ?? 12);
  const primaryColor = $derived(widget.gauge_settings?.color_primary ?? '#3b82f6');
  const secondaryColor = $derived(widget.gauge_settings?.color_secondary ?? '#e5e7eb');
  const showGlow = $derived(widget.gauge_settings?.show_glow ?? true);
  const animationDuration = $derived(widget.gauge_settings?.animation_duration ?? 800);
  const showUnit = $derived(widget.gauge_settings?.show_unit ?? true);
  const showLabel = $derived(widget.gauge_settings?.show_value ?? true);

  // Calculate gauge dimensions
  const size = $derived(Math.min(widget.width - 32, widget.height - 32));
  const radius = $derived((size / 2) - (strokeWidth / 2) - 4);
  const center = $derived(size / 2);
  const circumference = $derived(2 * Math.PI * radius);

  // Calculate arc properties
  const arcLength = $derived(endAngle - startAngle);
  const strokeDasharray = $derived((arcLength / 360) * circumference);

  // Format display value
  const formattedValue = $derived(typeof value === 'number' ? 
    (Number.isInteger(value) ? value.toString() : value.toFixed(1)) : '--');
  const unit = $derived(widget.gauge_settings?.unit || sensorData?.unit || '');
  const fontSize = $derived(Math.max(12, Math.min(size / 8, 28)));

  // Animation state
  let mounted = $state(false);
  let animatedPercentage = $state(0);

  // Initialize component and animate to current value
  $effect(() => {
    if (!mounted) {
      mounted = true;
      // Animate to current value on mount
      const startTime = Date.now();
      const animate = () => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / animationDuration, 1);
        animatedPercentage = percentage * progress;
        
        if (progress < 1) {
          requestAnimationFrame(animate);
        }
      };
      animate();
    }
  });

  // Update animation when percentage changes
  $effect(() => {
    if (mounted && percentage !== animatedPercentage) {
      const startValue = animatedPercentage;
      const targetValue = percentage;
      const startTime = Date.now();
      
      const animate = () => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / (animationDuration / 2), 1);
        const easeOut = 1 - Math.pow(1 - progress, 3);
        animatedPercentage = startValue + (targetValue - startValue) * easeOut;
        
        if (progress < 1) {
          requestAnimationFrame(animate);
        }
      };
      animate();
    }
  });

  // Calculate animated stroke offset
  const animatedStrokeDashoffset = $derived(strokeDasharray - (strokeDasharray * animatedPercentage / 100));

  // Determine value color based on percentage
  const valueColor = $derived(percentage > 80 ? '#ef4444' : percentage > 60 ? '#f59e0b' : '#10b981');
</script>

<div class="gauge-container">
  <div class="relative flex items-center justify-center" style="width: {size}px; height: {size}px;">
    <!-- SVG Gauge -->
    <svg width={size} height={size} class="absolute transform -rotate-90">
      <!-- Glow effect -->
      {#if showGlow}
        <defs>
          <filter id="glow-{widget.id}">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge> 
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
      {/if}
      
      <!-- Background circle -->
      <circle
        cx={center}
        cy={center}
        r={radius}
        fill="none"
        stroke={secondaryColor}
        stroke-width={strokeWidth}
        opacity="0.2"
      />
      
      <!-- Progress circle -->
      <circle
        cx={center}
        cy={center}
        r={radius}
        fill="none"
        stroke={primaryColor}
        stroke-width={strokeWidth}
        stroke-linecap="round"
        stroke-dasharray={strokeDasharray}
        stroke-dashoffset={animatedStrokeDashoffset}
        filter={showGlow ? `url(#glow-${widget.id})` : 'none'}
        class="transition-all duration-300 ease-out"
        style="transform-origin: {center}px {center}px;"
      />
    </svg>

    <!-- Center content -->
    <div class="absolute inset-0 flex flex-col items-center justify-center text-center px-4">
      <!-- Value -->
      <div 
        class="font-bold transition-colors duration-300"
        style="font-size: {fontSize}px; line-height: 1; color: {valueColor};"
      >
        {formattedValue}
      </div>
      
      <!-- Unit -->
      {#if showUnit && unit}
        <div 
          class="text-gray-500 mt-1"
          style="font-size: {fontSize * 0.4}px; line-height: 1;"
        >
          {unit}
        </div>
      {/if}
      
      <!-- Percentage -->
      <div 
        class="text-gray-400 mt-1"
        style="font-size: {fontSize * 0.35}px; line-height: 1;"
      >
        {animatedPercentage.toFixed(0)}%
      </div>
    </div>

    <!-- Label -->
    {#if showLabel}
      <div class="absolute -bottom-6 left-0 right-0 text-center">
        <div class="text-xs text-gray-600 truncate px-2">
          {widget.title || sensorData?.name || 'Unknown Sensor'}
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  .gauge-container {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  }
</style>
