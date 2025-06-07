<script lang="ts">
  import { onMount } from 'svelte';
  import type { WidgetConfig } from '$lib/types/widgets';
  import type { SensorData } from '$lib/types';

  const { widget, sensorData } = $props<{
    widget: WidgetConfig;
    sensorData: SensorData | undefined;
  }>();

  let currentImageIndex = $state(0);
  let images = $state<HTMLImageElement[]>([]);
  let imagesLoaded = $state(false);
  let animationFrame: number | null = null;

  // Image sequence settings with defaults
  const imageSequence = $derived(widget.gauge_settings?.image_sequence || []);
  const minValue = $derived(widget.gauge_settings?.min_value ?? sensorData?.min_value ?? 0);
  const maxValue = $derived(widget.gauge_settings?.max_value ?? sensorData?.max_value ?? 100);
  const animationSpeed = $derived(widget.gauge_settings?.animation_speed ?? 300);
  const smoothTransitions = $derived(widget.gauge_settings?.smooth_transitions ?? true);

  const sensorName = $derived(widget.title || sensorData?.name || 'Unknown Sensor');
  const unit = $derived(widget.gauge_settings?.unit || sensorData?.unit || '');
  const displayValue = $derived(sensorData?.value ?? '--');

  // Load images when image sequence changes
  $effect(() => {
    if (imageSequence.length > 0) {
      loadImages();
    }
  });

  // Calculate current image based on sensor value with smooth transitions
  $effect(() => {
    if (imagesLoaded && imageSequence.length > 0 && typeof displayValue === 'number') {
      const normalizedValue = Math.max(0, Math.min(1, (displayValue - minValue) / (maxValue - minValue)));
      const targetIndex = Math.floor(normalizedValue * (imageSequence.length - 1));
      
      if (smoothTransitions) {
        // Cancel any existing animation
        if (animationFrame) {
          cancelAnimationFrame(animationFrame);
        }

        // Start smooth transition animation
        const startIndex = currentImageIndex;
        const startTime = performance.now();
        
        const animate = (currentTime: number) => {
          const elapsed = currentTime - startTime;
          const progress = Math.min(elapsed / animationSpeed, 1);
          
          // Ease in-out function for smooth animation
          const easedProgress = progress < 0.5
            ? 2 * progress * progress
            : 1 - Math.pow(-2 * progress + 2, 2) / 2;
          
          currentImageIndex = Math.round(startIndex + (targetIndex - startIndex) * easedProgress);
          
          if (progress < 1) {
            animationFrame = requestAnimationFrame(animate);
          } else {
            currentImageIndex = targetIndex;
            animationFrame = null;
          }
        };
        
        animationFrame = requestAnimationFrame(animate);
      } else {
        currentImageIndex = targetIndex;
      }
    }
  });

  // Load images with caching
  async function loadImages() {
    imagesLoaded = false;
    images = [];

    try {
      const loadPromises = imageSequence.map((imageSrc: string) => {
        return new Promise<HTMLImageElement>((resolve, reject) => {
          const img = new Image();
          
          // Add loading optimization attributes
          img.loading = 'eager';
          img.decoding = 'async';
          
          img.onload = () => {
            // Preload next image in sequence
            const nextIndex = imageSequence.indexOf(imageSrc) + 1;
            if (nextIndex < imageSequence.length) {
              const nextImg = new Image();
              nextImg.src = imageSequence[nextIndex];
            }
            resolve(img);
          };
          img.onerror = reject;
          img.src = imageSrc;
        });
      });

      images = await Promise.all(loadPromises);
      imagesLoaded = true;
    } catch (error) {
      console.error('Failed to load image sequence:', error);
      imagesLoaded = false;
    }
  }

  // Optimize image upload handling
  function handleImageUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files) {
      const files = Array.from(input.files);
      
      // Process images in chunks to avoid blocking the UI
      const chunkSize = 5;
      const chunks: File[][] = [];
      
      for (let i = 0; i < files.length; i += chunkSize) {
        chunks.push(files.slice(i, i + chunkSize));
      }
      
      let processedUrls: string[] = [];
      
      const processChunk = async (chunk: File[], index: number) => {
        const chunkUrls = await Promise.all(
          chunk.map(async (file) => {
            // Create a worker for image processing if available
            if (window.Worker) {
              return new Promise<string>((resolve) => {
                const worker = new Worker('/src/lib/workers/imageProcessor.js');
                worker.postMessage({ file });
                worker.onmessage = (e) => resolve(e.data.url);
              });
            } else {
              // Fallback to direct processing
              return URL.createObjectURL(file);
            }
          })
        );
        
        processedUrls = [...processedUrls, ...chunkUrls];
        
        // Update widget settings after each chunk
        widget.gauge_settings = {
          ...widget.gauge_settings,
          image_sequence: processedUrls
        };
        
        // Process next chunk if available
        if (index + 1 < chunks.length) {
          setTimeout(() => processChunk(chunks[index + 1], index + 1), 0);
        }
      };
      
      // Start processing first chunk
      if (chunks.length > 0) {
        processChunk(chunks[0], 0);
      }
    }
  }

  onMount(() => {
    // Cleanup function
    return () => {
      // Cancel any ongoing animation
      if (animationFrame) {
        cancelAnimationFrame(animationFrame);
      }
      
      // Revoke object URLs
      imageSequence.forEach((url: string) => {
        if (url.startsWith('blob:')) {
          URL.revokeObjectURL(url);
        }
      });
    };
  });
</script>

<div class="gauge-container">
  <!-- Title -->
  {#if widget.gauge_settings?.show_label}
    <div class="text-center text-xs font-medium text-[var(--theme-text-muted)] mb-1 truncate">
      {sensorName}
    </div>
  {/if}

  <!-- Image Display Area -->
  <div class="image-display flex-1 flex items-center justify-center relative">
    {#if imageSequence.length === 0}
      <!-- Upload prompt -->
      <div class="upload-prompt text-center p-4">
        <div class="text-[var(--theme-text-muted)] mb-2">
          <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          No image sequence
        </div>
        <label class="btn-upload cursor-pointer inline-block px-3 py-1 bg-[var(--theme-primary)] text-white rounded text-xs hover:opacity-80">
          Upload Images
          <input 
            type="file" 
            multiple 
            accept="image/*" 
            class="hidden" 
            onchange={handleImageUpload}
          />
        </label>
      </div>
    {:else if !imagesLoaded}
      <!-- Loading indicator -->
      <div class="text-center text-[var(--theme-text-muted)]">
        <svg class="w-6 h-6 mx-auto mb-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <div class="text-xs">Loading images...</div>
      </div>
    {:else}
      {#if images.length > 0 && currentImageIndex >= 0 && currentImageIndex < images.length}
        <!-- Current image -->
        <img 
          src={images[currentImageIndex]!.src}
          alt="Sensor visualization"
          class="max-w-full max-h-full object-contain"
        />
        
        <!-- Progress indicator -->
        <div class="absolute bottom-1 left-1 right-1">
          <div class="bg-black bg-opacity-30 rounded-full h-1 overflow-hidden">
            <div 
              class="h-full bg-[var(--theme-primary)] transition-all duration-300"
              style="width: {((currentImageIndex + 1) / imageSequence.length) * 100}%"
            ></div>
          </div>
        </div>
      {/if}
    {/if}
  </div>

  <!-- Value Display -->
  <div class="text-center mt-2">
    <div class="text-sm font-semibold text-[var(--theme-text)]">
      {displayValue}
      {#if widget.gauge_settings?.show_unit && unit}
        <span class="text-xs text-[var(--theme-text-muted)] ml-1">{unit}</span>
      {/if}
    </div>
    
    {#if imageSequence.length > 0}
      <div class="text-xs text-[var(--theme-text-muted)] mt-1">
        Frame {currentImageIndex + 1} of {imageSequence.length}
      </div>
    {/if}
  </div>

  <!-- Settings overlay in edit mode -->
  {#if imageSequence.length > 0}
    <div class="absolute top-1 right-1">
      <label class="btn-settings cursor-pointer p-1 bg-black bg-opacity-30 rounded text-white hover:bg-opacity-50 transition-all">
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
        </svg>
        <input 
          type="file" 
          multiple 
          accept="image/*" 
          class="hidden" 
          onchange={handleImageUpload}
        />
      </label>
    </div>
  {/if}
</div>

<style>
  .gauge-container {
    width: 100%;
    height: 100%;
    padding: 8px;
    display: flex;
    flex-direction: column;
    position: relative;
  }

  .image-display {
    min-height: 0; /* Allow flex item to shrink */
    border: 1px dashed var(--theme-border);
    border-radius: 4px;
    overflow: hidden;
  }

  .upload-prompt {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
</style>
