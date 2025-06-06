<script lang="ts">
  import { onMount } from 'svelte';
  import type { WidgetConfig } from '$lib/types/widgets';
  import type { SensorData } from '$lib/types';

  const { widget, sensorData } = $props<{
    widget: WidgetConfig;
    sensorData: SensorData | undefined;
  }>();

  // Gauge settings with defaults
  const glow_intensity = $derived(widget.gauge_settings?.glow_intensity ?? 0.5);
  const blur_level = $derived(widget.gauge_settings?.blur_level ?? 0.3);
  const transparency = $derived(widget.gauge_settings?.transparency ?? 0.8);
  const gauge_style = $derived(widget.gauge_settings?.style ?? 'radial'); // 'radial' | 'linear' | 'ring'
  
  // Data processing
  const sensorName = $derived(widget.title || sensorData?.name || 'Unknown Sensor');
  const unit = $derived(widget.gauge_settings?.unit || sensorData?.unit || '');
  const displayValue = $derived(sensorData?.value ?? '--');
  const minValue = $derived(widget.gauge_settings?.min_value ?? sensorData?.min_value ?? 0);
  const maxValue = $derived(widget.gauge_settings?.max_value ?? sensorData?.max_value ?? 100);
  
  // Calculate normalized value (0-1)
  const normalizedValue = $derived(typeof displayValue === 'number' 
    ? Math.max(0, Math.min(1, (displayValue - minValue) / (maxValue - minValue)))
    : 0);
  
  // Calculate percentage for display
  const percentageValue = $derived(Math.round(normalizedValue * 100));
  
  // Dynamic styling based on value
  const valueColor = $derived(getValueColor(normalizedValue));
  const glowColor = $derived(getGlowColor(normalizedValue));
  
  function getValueColor(value: number): string {
    if (value < 0.3) return '#10b981'; // Green
    if (value < 0.7) return '#f59e0b'; // Yellow  
    return '#ef4444'; // Red
  }
  
  function getGlowColor(value: number): string {
    if (value < 0.3) return '16, 185, 129'; // Green RGB
    if (value < 0.7) return '245, 158, 11'; // Yellow RGB
    return '239, 68, 68'; // Red RGB
  }
  
  // Animation values
  let mountedValue = 0;
  let animationProgress = 0;
  
  onMount(() => {
    // Animate to current value on mount
    const animate = () => {
      if (mountedValue < normalizedValue) {
        mountedValue = Math.min(mountedValue + 0.02, normalizedValue);
        animationProgress = mountedValue;
        requestAnimationFrame(animate);
      } else {
        animationProgress = normalizedValue;
      }
    };
    animate();
  });
  
  // Update animation when value changes
  $effect(() => {
    if (typeof normalizedValue === 'number') {
      const targetValue = normalizedValue;
      const currentValue = animationProgress;
      const diff = targetValue - currentValue;
      
      if (Math.abs(diff) > 0.01) {
        const animate = () => {
          const step = diff * 0.1;
          animationProgress += step;
          
          if (Math.abs(targetValue - animationProgress) > 0.01) {
            requestAnimationFrame(animate);
          } else {
            animationProgress = targetValue;
          }
        };
        animate();
      }
    }
  });
</script>

<div class="glassmorphic-gauge" class:show-blur={blur_level > 0}>
  <!-- Background Glass Effect -->
  <div 
    class="glass-background"
    style="
      backdrop-filter: blur({blur_level * 20}px);
      background: rgba(255, 255, 255, {transparency * 0.1});
      border: 1px solid rgba(255, 255, 255, {transparency * 0.2});
    "
  ></div>
  
  <!-- Title -->
  {#if widget.gauge_settings?.show_label}
    <div class="gauge-title">
      {sensorName}
    </div>
  {/if}
  
  <!-- Main Gauge Content -->
  <div class="gauge-content">
    {#if gauge_style === 'radial'}
      <!-- Radial Gauge -->
      <div class="radial-gauge">
        <svg viewBox="0 0 120 120" class="gauge-svg">
          <!-- Background Arc -->
          <circle
            cx="60"
            cy="60"
            r="45"
            fill="none"
            stroke="rgba(255, 255, 255, 0.1)"
            stroke-width="8"
            stroke-linecap="round"
          />
          
          <!-- Progress Arc -->
          <circle
            cx="60"
            cy="60"
            r="45"
            fill="none"
            stroke={valueColor}
            stroke-width="8"
            stroke-linecap="round"
            stroke-dasharray="283"
            stroke-dashoffset={283 - (283 * animationProgress)}
            transform="rotate(-90 60 60)"
            style="
              filter: drop-shadow(0 0 {glow_intensity * 10}px rgba({glowColor}, {glow_intensity}));
              transition: stroke-dashoffset 0.3s ease;
            "
          />
          
          <!-- Center Glow -->
          <circle
            cx="60"
            cy="60"
            r="25"
            fill="rgba({glowColor}, {glow_intensity * 0.1})"
            style="filter: blur({blur_level * 5}px);"
          />
        </svg>
        
        <!-- Center Value -->
        <div class="center-value">
          <div class="value-text" style="color: {valueColor};">
            {displayValue}
          </div>
          {#if widget.gauge_settings?.show_unit && unit}
            <div class="unit-text">
              {unit}
            </div>
          {/if}
        </div>
      </div>
      
    {:else if gauge_style === 'linear'}
      <!-- Linear Gauge -->
      <div class="linear-gauge">
        <div class="linear-track">
          <div 
            class="linear-progress"
            style="
              width: {animationProgress * 100}%;
              background: linear-gradient(90deg, {valueColor} 0%, rgba({glowColor}, 0.8) 100%);
              box-shadow: 0 0 {glow_intensity * 15}px rgba({glowColor}, {glow_intensity});
            "
          ></div>
        </div>
        
        <div class="linear-value">
          <span class="value-text" style="color: {valueColor};">
            {displayValue}
          </span>
          {#if widget.gauge_settings?.show_unit && unit}
            <span class="unit-text">{unit}</span>
          {/if}
        </div>
      </div>
      
    {:else if gauge_style === 'ring'}
      <!-- Ring Gauge -->
      <div class="ring-gauge">
        <div class="ring-container">
          <!-- Outer Ring -->
          <div 
            class="ring-outer"
            style="
              background: conic-gradient(
                from 0deg,
                {valueColor} 0deg,
                {valueColor} {animationProgress * 360}deg,
                rgba(255, 255, 255, 0.1) {animationProgress * 360}deg,
                rgba(255, 255, 255, 0.1) 360deg
              );
              filter: blur({blur_level * 2}px) drop-shadow(0 0 {glow_intensity * 8}px rgba({glowColor}, {glow_intensity}));
            "
          ></div>
          
          <!-- Inner Content -->
          <div class="ring-inner">
            <div class="ring-value">
              <div class="value-text" style="color: {valueColor};">
                {percentageValue}%
              </div>
              <div class="sensor-name">
                {sensorName}
              </div>
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>
  
  <!-- Bottom Info -->
  <div class="gauge-info">
    <div class="info-item">
      <span class="info-label">Min</span>
      <span class="info-value">{minValue}</span>
    </div>
    <div class="info-item">
      <span class="info-label">Max</span>
      <span class="info-value">{maxValue}</span>
    </div>
  </div>
  
  <!-- Floating Particles Effect -->
  {#if glow_intensity > 0.7}
    <div class="particles">
      {#each Array(6) as _, i}
        <div 
          class="particle"
          style="
            animation-delay: {i * 0.3}s;
            background: radial-gradient(circle, rgba({glowColor}, 0.8) 0%, transparent 70%);
          "
        ></div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .glassmorphic-gauge {
    width: 100%;
    height: 100%;
    position: relative;
    overflow: hidden;
    border-radius: 1rem;
    padding: 1rem;
    display: flex;
    flex-direction: column;
  }

  .glass-background {
    position: absolute;
    inset: 0;
    z-index: 0;
  }

  .gauge-title {
    position: relative;
    z-index: 1;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--theme-text-muted);
    margin-bottom: 0.5rem;
    text-align: center;
  }

  .gauge-content {
    position: relative;
    z-index: 1;
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .gauge-info {
    position: relative;
    z-index: 1;
    display: flex;
    justify-content: space-between;
    margin-top: 0.5rem;
    font-size: 0.75rem;
  }

  .info-item {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .info-label {
    color: var(--theme-text-muted);
    font-size: 0.625rem;
  }

  .info-value {
    color: var(--theme-text);
    font-weight: 500;
  }

  /* Radial Gauge Styles */
  .radial-gauge {
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .gauge-svg {
    width: 100%;
    height: 100%;
    max-width: 200px;
    max-height: 200px;
  }

  .center-value {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
  }

  .value-text {
    font-size: 1.5rem;
    font-weight: 600;
    line-height: 1;
  }

  .unit-text {
    font-size: 0.75rem;
    color: var(--theme-text-muted);
    margin-top: 0.25rem;
  }

  /* Linear Gauge Styles */
  .linear-gauge {
    width: 100%;
    padding: 1rem;
  }

  .linear-track {
    height: 0.5rem;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 0.25rem;
    overflow: hidden;
  }

  .linear-progress {
    height: 100%;
    border-radius: 0.25rem;
    transition: width 0.3s ease;
  }

  .linear-value {
    margin-top: 0.5rem;
    text-align: center;
  }

  /* Ring Gauge Styles */
  .ring-gauge {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .ring-container {
    position: relative;
    width: 150px;
    height: 150px;
  }

  .ring-outer {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    transition: background 0.3s ease;
  }

  .ring-inner {
    position: absolute;
    inset: 10px;
    background: var(--theme-surface);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .ring-value {
    text-align: center;
  }

  .sensor-name {
    font-size: 0.75rem;
    color: var(--theme-text-muted);
    margin-top: 0.25rem;
  }

  /* Particles Effect */
  .particles {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }

  .particle {
    position: absolute;
    width: 100px;
    height: 100px;
    opacity: 0;
    animation: float 3s ease-in-out infinite;
  }

  @keyframes float {
    0%, 100% {
      transform: translate(0, 0);
      opacity: 0;
    }
    50% {
      transform: translate(20px, -20px);
      opacity: 0.5;
    }
  }

  /* Show blur class */
  .show-blur {
    backdrop-filter: blur(10px);
  }
</style>
