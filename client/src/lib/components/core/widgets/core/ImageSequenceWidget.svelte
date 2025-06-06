<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import type { WidgetConfig } from '$lib/types/widgets';
  import { createEventDispatcher } from 'svelte';

  const { widget } = $props<{ widget: WidgetConfig }>();
  const dispatch = createEventDispatcher();

  // Image sequence state
  let currentFrame = $state(0);
  let isPlaying = $state(false);
  let frameRate = $state(30);
  let preloadQueue: string[] = [];
  let imageCache = new Map<string, HTMLImageElement>();
  let frameTimeout: number | null = null;

  // Performance monitoring
  let loadTimes = new Map<string, number>();
  let averageLoadTime = $state(0);
  let cacheHitRate = $state(0);
  let totalRequests = $state(0);
  let cacheHits = $state(0);

  // Image sequence settings
  let settings = $derived({
    ...widget.gauge_settings,
    frameRate: widget.gauge_settings.frameRate || 30,
    loop: widget.gauge_settings.loop ?? true,
    preloadFrames: widget.gauge_settings.preloadFrames || 5,
    quality: widget.gauge_settings.quality || 'high',
    interpolation: widget.gauge_settings.interpolation || 'linear'
  });

  // Smart preloading
  function preloadNextFrames() {
    const framesToPreload = Math.min(settings.preloadFrames, widget.gauge_settings.frames?.length || 0);
    const startFrame = (currentFrame + 1) % (widget.gauge_settings.frames?.length || 1);
    
    for (let i = 0; i < framesToPreload; i++) {
      const frameIndex = (startFrame + i) % (widget.gauge_settings.frames?.length || 1);
      const frameUrl = widget.gauge_settings.frames?.[frameIndex];
      if (frameUrl && !imageCache.has(frameUrl)) {
        preloadQueue.push(frameUrl);
      }
    }
    
    processPreloadQueue();
  }

  // Process preload queue with rate limiting
  let isProcessingQueue = false;
  async function processPreloadQueue() {
    if (isProcessingQueue || preloadQueue.length === 0) return;
    
    isProcessingQueue = true;
    const startTime = performance.now();
    
    while (preloadQueue.length > 0) {
      const frameUrl = preloadQueue.shift();
      if (!frameUrl) continue;
      
      try {
        const img = new Image();
        const loadPromise = new Promise<void>((resolve, reject) => {
          img.onload = () => resolve();
          img.onerror = reject;
        });
        
        img.src = frameUrl;
        await loadPromise;
        
        imageCache.set(frameUrl, img);
        const loadTime = performance.now() - startTime;
        loadTimes.set(frameUrl, loadTime);
        
        // Update average load time
        const times = Array.from(loadTimes.values());
        averageLoadTime = times.reduce((a, b) => a + b, 0) / times.length;
        
      } catch (error) {
        console.error(`Failed to preload image: ${frameUrl}`, error);
      }
      
      // Rate limit preloading
      await new Promise(resolve => setTimeout(resolve, 16));
    }
    
    isProcessingQueue = false;
  }

  // Frame update with interpolation
  function updateFrame() {
    if (!isPlaying || !widget.gauge_settings.frames?.length) return;
    
    const nextFrame = (currentFrame + 1) % widget.gauge_settings.frames.length;
    const frameUrl = widget.gauge_settings.frames[nextFrame];
    
    totalRequests++;
    if (imageCache.has(frameUrl)) {
      cacheHits++;
      cacheHitRate = (cacheHits / totalRequests) * 100;
    }
    
    currentFrame = nextFrame;
    preloadNextFrames();
    
    frameTimeout = window.setTimeout(updateFrame, 1000 / frameRate);
  }

  // Playback controls
  function togglePlayback() {
    isPlaying = !isPlaying;
    if (isPlaying) {
      updateFrame();
    } else if (frameTimeout) {
      clearTimeout(frameTimeout);
      frameTimeout = null;
    }
  }

  function setFrameRate(newRate: number) {
    frameRate = Math.max(1, Math.min(60, newRate));
    if (isPlaying && frameTimeout) {
      clearTimeout(frameTimeout);
      updateFrame();
    }
  }

  // Cleanup
  onDestroy(() => {
    if (frameTimeout) {
      clearTimeout(frameTimeout);
    }
    imageCache.clear();
    preloadQueue = [];
  });

  // Initial preload
  onMount(() => {
    preloadNextFrames();
  });
</script>

<div class="image-sequence-widget relative w-full h-full">
  <!-- Current frame display -->
  {#if widget.gauge_settings.frames?.[currentFrame]}
    <img
      src={widget.gauge_settings.frames[currentFrame]}
      alt={`Frame ${currentFrame + 1}`}
      class="w-full h-full object-contain"
      style="image-rendering: {settings.quality === 'high' ? 'crisp-edges' : 'auto'};"
    />
  {/if}

  <!-- Playback controls -->
  <div class="absolute bottom-0 left-0 right-0 bg-black bg-opacity-50 p-2 flex items-center justify-between">
    <button
      class="text-white hover:text-blue-400 transition-colors"
      on:click={togglePlayback}
    >
      {isPlaying ? '⏸' : '▶'}
    </button>
    
    <div class="text-white text-sm">
      Frame: {currentFrame + 1}/{widget.gauge_settings.frames?.length || 0}
    </div>
    
    <div class="text-white text-sm">
      FPS: {frameRate}
    </div>
  </div>

  <!-- Performance metrics (debug) -->
  {#if settings.showDebug}
    <div class="absolute top-0 left-0 right-0 bg-black bg-opacity-50 p-2 text-white text-xs">
      <div>Avg Load Time: {averageLoadTime.toFixed(2)}ms</div>
      <div>Cache Hit Rate: {cacheHitRate.toFixed(1)}%</div>
      <div>Cache Size: {imageCache.size}</div>
      <div>Queue Size: {preloadQueue.length}</div>
    </div>
  {/if}
</div>

<style>
  .image-sequence-widget {
    contain: layout style paint;
  }

  img {
    will-change: transform;
    backface-visibility: hidden;
  }
</style> 