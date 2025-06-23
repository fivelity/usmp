<script lang="ts">
  import { widgetUtils } from '$lib/stores/data/widgets.svelte';
  import type { WidgetConfig } from '$lib/types/widgets';
  import { RangeSlider, ToggleSwitch, Button } from '$lib/components/ui/common';
  import FileInput from '$lib/components/ui/common/FileInput.svelte';

  const { widget } = $props<{ widget: WidgetConfig }>();

  // Image sequence settings
  let settings = $derived({
    ...widget.gauge_settings,
    frameRate: widget.gauge_settings.frameRate || 30,
    loop: widget.gauge_settings.loop ?? true,
    preloadFrames: widget.gauge_settings.preloadFrames || 5,
    quality: widget.gauge_settings.quality || 'high',
    interpolation: widget.gauge_settings.interpolation || 'linear',
    showDebug: widget.gauge_settings.showDebug ?? false
  });

  // Handle file uploads
  async function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    const files = Array.from(input.files);
    const newFrames = [...(settings.frames || [])];

    for (const file of files) {
      try {
        const reader = new FileReader();
        const dataUrl = await new Promise<string>((resolve, reject) => {
          reader.onload = () => resolve(reader.result as string);
          reader.onerror = reject;
          reader.readAsDataURL(file);
        });
        newFrames.push(dataUrl);
      } catch (error) {
        console.error('Error reading file:', error);
      }
    }

    updateSettings({ frames: newFrames });
  }

  // Update settings
  function updateSettings(updates: Partial<typeof settings>) {
    widgetUtils.updateWidget(widget.id, {
      gauge_settings: {
        ...settings,
        ...updates
      }
    });
  }

  // Remove frame
  function removeFrame(index: number) {
    const newFrames = [...(settings.frames || [])];
    newFrames.splice(index, 1);
    updateSettings({ frames: newFrames });
  }

  // Reorder frames
  function moveFrame(fromIndex: number, toIndex: number) {
    const newFrames = [...(settings.frames || [])];
    const [movedFrame] = newFrames.splice(fromIndex, 1);
    newFrames.splice(toIndex, 0, movedFrame);
    updateSettings({ frames: newFrames });
  }
</script>

<div class="image-sequence-inspector space-y-4 p-4">
  <div class="space-y-2">
    <h3 class="text-lg font-semibold">Image Sequence Settings</h3>
    
    <!-- Frame Rate -->
    <div class="space-y-1">
      <label for="frame-rate" class="text-sm font-medium">Frame Rate</label>
      <RangeSlider
        id="frame-rate"
        value={settings.frameRate}
        min={1}
        max={60}
        step={1}
        onchange={(value) => updateSettings({ frameRate: value })}
      />
      <div class="text-xs text-gray-500">{settings.frameRate} FPS</div>
    </div>

    <!-- Preload Frames -->
    <div class="space-y-1">
      <label for="preload-frames" class="text-sm font-medium">Preload Frames</label>
      <RangeSlider
        id="preload-frames"
        value={settings.preloadFrames}
        min={1}
        max={20}
        step={1}
        onchange={(value) => updateSettings({ preloadFrames: value })}
      />
      <div class="text-xs text-gray-500">Preload {settings.preloadFrames} frames ahead</div>
    </div>

    <!-- Quality -->
    <div class="space-y-1">
      <label for="quality-select" class="text-sm font-medium">Quality</label>
      <select
        id="quality-select"
        class="w-full rounded border border-gray-300 p-2"
        value={settings.quality}
        onchange={(e) => updateSettings({ quality: e.currentTarget.value })}
      >
        <option value="high">High</option>
        <option value="low">Low</option>
      </select>
    </div>

    <!-- Interpolation -->
    <div class="space-y-1">
      <label for="interpolation-select" class="text-sm font-medium">Interpolation</label>
      <select
        id="interpolation-select"
        class="w-full rounded border border-gray-300 p-2"
        value={settings.interpolation}
        onchange={(e) => updateSettings({ interpolation: e.currentTarget.value })}
      >
        <option value="linear">Linear</option>
        <option value="nearest">Nearest</option>
      </select>
    </div>

    <!-- Loop -->
    <div class="flex items-center justify-between">
      <label for="loop-animation" class="text-sm font-medium">Loop Animation</label>
      <ToggleSwitch
        id="loop-animation"
        checked={settings.loop}
        onchange={(value) => updateSettings({ loop: value })}
      />
    </div>

    <!-- Debug Mode -->
    <div class="flex items-center justify-between">
      <label for="show-debug" class="text-sm font-medium">Show Debug Info</label>
      <ToggleSwitch
        id="show-debug"
        checked={settings.showDebug}
        onchange={(value) => updateSettings({ showDebug: value })}
      />
    </div>
  </div>

  <!-- Frame Management -->
  <div class="space-y-2">
    <h3 class="text-lg font-semibold">Frames</h3>
    
    <!-- Upload Frames -->
    <FileInput
      accept="image/*"
      multiple
      onchange={handleFileUpload}
      class="w-full"
    >
      Upload Frames
    </FileInput>

    <!-- Frame List -->
    <div class="space-y-2 max-h-48 overflow-y-auto">
      {#each settings.frames || [] as frame, i}
        <div class="flex items-center space-x-2 p-2 bg-gray-100 rounded">
          <img src={frame} alt={`Frame ${i + 1}`} class="w-8 h-8 object-cover rounded" />
          <span class="text-sm flex-1">Frame {i + 1}</span>
          <div class="flex space-x-1">
            {#if i > 0}
              <Button
                size="sm"
                variant="ghost"
                onClick={() => moveFrame(i, i - 1)}
              >
                ↑
              </Button>
            {/if}
            {#if i < (settings.frames?.length || 0) - 1}
              <Button
                size="sm"
                variant="ghost"
                onClick={() => moveFrame(i, i + 1)}
              >
                ↓
              </Button>
            {/if}
            <Button
              size="sm"
              variant="ghost"
              className="text-red-500"
              onClick={() => removeFrame(i)}
            >
              ×
            </Button>
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>

<style>
  .image-sequence-inspector {
    contain: layout style;
  }
</style> 