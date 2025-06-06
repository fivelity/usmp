<script lang="ts">
  import { onMount } from 'svelte';
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
  const orientation = $derived(widget.gauge_settings?.orientation ?? 'horizontal');
  const showScale = $derived(widget.gauge_settings?.show_scale ?? true);
  const primaryColor = $derived(widget.gauge_settings?.color_primary ?? '#3b82f6');
  const showGradient = $derived(widget.gauge_settings?.show_gradient ?? true);
  const barHeight = $derived(widget.gauge_settings?.bar_height ?? 20);
  const animationDuration = $derived(widget.gauge_settings?.animation_duration ?? 600);
  const showUnit = $derived(widget.gauge_settings?.show_unit ?? true);
  const showLabel = $derived(widget.gauge_settings?.show_label ?? true);

  // Format display value
  const formattedValue = $derived(typeof value === 'number' ? 
    (Number.isInteger(value) ? value.toString() : value.toFixed(1)) : '--');
  const unit = $derived(widget.gauge_settings?.unit || sensorData?.unit || '');
  
  // Calculate dimensions based on orientation
  const isHorizontal = $derived(orientation === 'horizontal');
  const actualBarHeight = $derived(Math.min(barHeight, isHorizontal ? widget.height / 3 : widget.width / 3));

  // Animation state
  let mounted = false;
  let animatedPercentage = 0;

  onMount(() => {
    mounted = true;
    // Animate to current value
    const startTime = Date.now();
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / animationDuration, 1);
      const easeOut = 1 - Math.pow(1 - progress, 3);
      animatedPercentage = percentage * easeOut;
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };
    animate();
  });

  // Update animation when percentage changes
  $effect(() => {
    if (mounted && Math.abs(percentage - animatedPercentage) > 0.1) {
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

  // Determine value color based on percentage
  const valueColor = $derived(percentage > 80 ? '#ef4444' : percentage > 60 ? '#f59e0b' : '#10b981');
  
  // Create gradient
  const gradientColors = $derived(showGradient ? 
    `linear-gradient(${isHorizontal ? '90deg' : '0deg'}, ${primaryColor}, ${valueColor})` : 
    primaryColor);
</script>

<div class="gauge-container">
  <div class="flex {isHorizontal ? 'flex-col' : 'flex-row'} h-full justify-center items-center gap-3">
    
    <!-- Value Display -->
    <div class="text-center {isHorizontal ? 'mb-2' : 'mr-3'} flex-shrink-0">
      <div class="font-bold text-2xl transition-colors duration-300" style="color: {valueColor};">
        {formattedValue}
      </div>
      {#if showUnit && unit}
        <div class="text-sm text-gray-500 mt-1">
          {unit}
        </div>
      {/if}
    </div>

    <!-- Progress Bar Container -->
    <div class="flex-1 {isHorizontal ? 'w-full' : 'h-full'} relative">
      <!-- Background bar -->
      <div 
        class="
          {isHorizontal ? 'w-full' : 'h-full'} 
          bg-gray-200 
          rounded-full 
          overflow-hidden
          shadow-inner
        "
        style="
          {isHorizontal ? `height: ${actualBarHeight}px;` : `width: ${actualBarHeight}px;`}
        "
      >
        <!-- Progress fill -->
        <div 
          class="
            {isHorizontal ? 'h-full' : 'w-full'} 
            rounded-full 
            transition-all 
            duration-500 
            ease-out
            shadow-sm
          "
          style="
            background: {gradientColors};
            {isHorizontal 
              ? `width: ${animatedPercentage}%;` 
              : `height: ${animatedPercentage}%; margin-top: auto;`
            }
          "
        >
          <!-- Shine effect -->
          <div class="
            w-full h-full rounded-full
            bg-gradient-to-{isHorizontal ? 'r' : 'b'} 
            from-white/20 via-transparent to-transparent
          "></div>
        </div>
      </div>

      <!-- Scale markers -->
      {#if showScale}
        <div class="absolute {isHorizontal ? 'top-full mt-2 left-0 right-0' : 'left-full ml-2 top-0 bottom-0'}">
          <div class="
            {isHorizontal ? 'flex justify-between' : 'flex flex-col justify-between h-full'} 
            text-xs text-gray-500
          ">
            <span class="font-medium">{minValue}</span>
            <span class="font-medium">{maxValue}</span>
          </div>
        </div>
      {/if}

      <!-- Percentage indicator -->
      <div class="absolute {isHorizontal ? 'bottom-full mb-1' : 'right-full mr-1'} 
                  {isHorizontal ? 'left-1/2 transform -translate-x-1/2' : 'top-1/2 transform -translate-y-1/2'}">
        <div class="text-xs text-gray-600 font-semibold bg-white/80 px-2 py-1 rounded-full shadow-sm">
          {animatedPercentage.toFixed(0)}%
        </div>
      </div>
    </div>

    <!-- Label -->
    {#if showLabel}
      <div class="text-center {isHorizontal ? 'mt-2' : 'ml-3'} flex-shrink-0">
        <div class="text-xs text-gray-600 font-medium max-w-20 truncate">
          {widget.title || sensorData?.name || 'Sensor'}
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  .gauge-container {
    width: 100%;
    height: 100%;
    padding: 16px;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  }
</style>
