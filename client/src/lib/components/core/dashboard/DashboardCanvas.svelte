<script lang="ts">
  import { onMount } from 'svelte';
  import { getEditMode, uiUtils } from '$lib/stores/core/ui.svelte';
  import { widgetArray } from '$lib/stores/data/widgets'; // Assuming widgetArray is Widget[]
  
  import { widgetUtils } from '$lib/stores/data/widgets';
  import { notifications } from '$lib/stores/notifications';
  import WidgetContainer from '../widgets/core/WidgetContainer.svelte';
  import GridSystem from './GridSystem.svelte';
  import NotificationCenter from '../../ui/common/NotificationCenter.svelte';
  import type { Point } from '$lib/types';
  import type { Widget } from '$lib/types';
  import type { WidgetConfig, GaugeSettings } from '$lib/types/widgets';
  import type { ContextMenuItem } from '$lib/stores/core/ui.svelte'; // Import ContextMenuItem
  import { get } from 'svelte/store';

  let canvasElement: HTMLDivElement | null = $state(null);
  let isSelecting = $state(false);
  let selectionStart: Point = $state({ x: 0, y: 0 });
  let selectionEnd: Point = $state({ x: 0, y: 0 });
  
  // Virtual scrolling state
  let viewport = $state({
    top: 0,
    bottom: 0,
    left: 0,
    right: 0,
    width: 0,
    height: 0
  });
  
  let visibleWidgets = $derived(calculateVisibleWidgets());
  
  // Performance monitoring
  let performanceMetrics = {
    renderCount: 0,
    lastRenderDuration: 0,
    averageRenderDuration: 0,
    visibleWidgetCount: 0
  };
  
  // Widget update batching
  let pendingUpdates = new Map<string, Partial<WidgetConfig>>();
  let updateTimeout: number | null = null;
  const BATCH_UPDATE_INTERVAL = 16; // ~60fps

  // Sensor data cache
  let sensorDataCache = new Map<string, {
    value: number;
    timestamp: number;
    ttl: number;
  }>();
  const CACHE_TTL = 1000; // 1 second cache TTL

  function calculateVisibleWidgets() {
    const widgets = get(widgetArray);
    return widgets.map(widget => mapWidgetToWidgetConfig(widget)).filter((widget: WidgetConfig) => {
      const widgetRect = {
        top: widget.pos_y,
        bottom: widget.pos_y + widget.height,
        left: widget.pos_x,
        right: widget.pos_x + widget.width
      };
      
      return !(
        widgetRect.bottom < viewport.top ||
        widgetRect.top > viewport.bottom ||
        widgetRect.right < viewport.left ||
        widgetRect.left > viewport.right
      );
    });
  }
  
  function updateViewport() {
    if (!canvasElement) return;
    
    const rect = canvasElement.getBoundingClientRect();
    viewport = {
      top: canvasElement.scrollTop,
      bottom: canvasElement.scrollTop + rect.height,
      left: canvasElement.scrollLeft,
      right: canvasElement.scrollLeft + rect.width,
      width: rect.width,
      height: rect.height
    };
    
    performanceMetrics.visibleWidgetCount = visibleWidgets.length;
  }
  
  // Throttled scroll handler
  let scrollThrottle: number | null = null;
  function handleScroll() {
    if (scrollThrottle) {
      cancelAnimationFrame(scrollThrottle);
    }
    
    scrollThrottle = requestAnimationFrame(() => {
      updateViewport();
      scrollThrottle = null;
    });
  }
  
  // Resize observer for viewport updates
  let resizeObserver: ResizeObserver | null = null;
  
  function mapWidgetToWidgetConfig(baseWidget: Widget): WidgetConfig {
    const config = baseWidget.config || {};
    const gaugeType = baseWidget.type;

    return {
      id: baseWidget.id,
      type: gaugeType,
      pos_x: baseWidget.x,
      pos_y: baseWidget.y,
      width: baseWidget.width,
      height: baseWidget.height,
      is_locked: baseWidget.is_locked ?? false,
      gauge_type: gaugeType,
      gauge_settings: config as GaugeSettings,
      group_id: baseWidget.groupId,
      z_index: 1,
      title: baseWidget.name,
      description: undefined,
      is_visible: true,
      is_draggable: true,
      is_resizable: true,
      is_selectable: true,
      is_grouped: !!baseWidget.groupId
    };
  }

  onMount(() => {
    if (canvasElement) {
      // Initial viewport calculation
      updateViewport();
      
      // Setup scroll listener
      canvasElement.addEventListener('scroll', handleScroll);
      
      // Setup resize observer
      resizeObserver = new ResizeObserver(() => {
        updateViewport();
      });
      resizeObserver.observe(canvasElement);
    }
    
    // Handle canvas interactions
    const handleMouseDown = (event: MouseEvent) => {
      if (getEditMode() !== 'edit') return;
      
      const target = event.target as Element;
      
      // Only start selection if clicking on the canvas itself
      if (target === canvasElement || target.closest('[data-canvas-background]')) {
        startSelection(event);
      }
    };

    const handleMouseMove = (event: MouseEvent) => {
      if (isSelecting) {
        updateSelection(event);
      }
    };

    const handleMouseUp = (event: MouseEvent) => {
      if (isSelecting) {
        finishSelection(event);
      }
    };

    const handleResize = () => {
      // Handle canvas resize if needed
      if (canvasElement) {
        // Trigger any necessary updates
        if (canvasElement) canvasElement.dispatchEvent(new CustomEvent('canvas-resize'));
      }
    };

    if (canvasElement) canvasElement.addEventListener('mousedown', handleMouseDown);
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
    window.addEventListener('resize', handleResize);

    return () => {
      if (canvasElement) {
        canvasElement.removeEventListener('scroll', handleScroll);
        canvasElement.removeEventListener('mousedown', handleMouseDown);
      }
      if (resizeObserver) {
        resizeObserver.disconnect();
      }
      if (scrollThrottle) {
        cancelAnimationFrame(scrollThrottle);
      }
      if (canvasElement) canvasElement.removeEventListener('mousemove', handleMouseMove);
      if (canvasElement) canvasElement.removeEventListener('mouseup', handleMouseUp);
      if (canvasElement) canvasElement.removeEventListener('resize', handleResize);
      if (updateTimeout) {
        clearTimeout(updateTimeout);
      }
      pendingUpdates.clear();
      sensorDataCache.clear();
    };
  });

  function startSelection(event: MouseEvent) {
    isSelecting = true;
    if (!canvasElement) return;
    const rect = canvasElement.getBoundingClientRect();
    selectionStart = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
    };
    selectionEnd = { ...selectionStart };
    
    // Clear current selection unless holding Shift
    if (!event.shiftKey) {
      uiUtils.clearSelection();
    }
  }

  function updateSelection(event: MouseEvent) {
    if (!isSelecting) return;
    
    if (!canvasElement) return;
    const rect = canvasElement.getBoundingClientRect();
    selectionEnd = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
    };
  }

  function finishSelection(event: MouseEvent) {
    isSelecting = false;
    const newlySelectedIds = new Set<string>();
    const currentSelectionBox = {
      x: Math.min(selectionStart.x, selectionEnd.x),
      y: Math.min(selectionStart.y, selectionEnd.y),
      width: Math.abs(selectionEnd.x - selectionStart.x),
      height: Math.abs(selectionEnd.y - selectionStart.y)
    };

    if (currentSelectionBox.width > 0 || currentSelectionBox.height > 0) {
      $widgetArray.forEach((widget: Widget) => {
        // Check if widget overlaps with selection box using widget.x and widget.y
        if (
          widget.x < currentSelectionBox.x + currentSelectionBox.width &&
          widget.x + widget.width > currentSelectionBox.x &&
          widget.y < currentSelectionBox.y + currentSelectionBox.height &&
          widget.y + widget.height > currentSelectionBox.y
        ) {
          newlySelectedIds.add(widget.id);
        }
      });
    }

    if (newlySelectedIds.size > 0) {
      if (event.shiftKey) {
        // Add to existing selection
        newlySelectedIds.forEach(id => uiUtils.addToSelection(id));
      } else {
        // Replace selection
        uiUtils.replaceSelection(Array.from(newlySelectedIds));
      }
    } else if (!event.shiftKey) {
      // If no new widgets selected and shift is not pressed, clear selection
      uiUtils.clearSelection();
    }

    // Reset selection box visual state
    selectionStart = { x: 0, y: 0 };
  }

  function handleCanvasRightClick(event: MouseEvent) {
    event.preventDefault();
    if (getEditMode() === 'view') return;
    const canvasMenuItems: ContextMenuItem[] = [
      { type: 'item', label: 'Paste Widget', action: 'paste-widget', disabled: true }, 
      { type: 'item', label: 'Select All Widgets', action: 'select-all-widgets' }, 
      { type: 'separator' },
      { type: 'item', label: 'Dashboard Settings...', action: 'dashboard-settings' } 
    ];
    uiUtils.showContextMenu(event.clientX, event.clientY, canvasMenuItems, undefined, 'canvas'); 
  }

  function handleCanvasKeyDown(event: KeyboardEvent) {
    if (getEditMode() !== 'edit') return;
    
    // Handle keyboard events for canvas
    if (event.key === 'Tab') {
      event.preventDefault();
      // Implement tab focus logic here
    }
  }

  function handleDrop(event: DragEvent) {
    event.preventDefault();
    const data = event.dataTransfer?.getData('application/json');
    if (data) {
      try {
        const widgetData = JSON.parse(data);
        // Handle widget drop
        notifications.add({
          type: 'info',
          category: 'user',
          title: 'Widget Added',
          message: `Added ${widgetData.type} widget to dashboard`,
          priority: 'low'
        });
      } catch (error) {
        console.error('Error handling widget drop:', error);
      }
    }
  }

  function handleDragOver(event: DragEvent) {
    event.preventDefault();
    event.dataTransfer!.dropEffect = 'copy';
  }

  function batchUpdateWidget(id: string, updates: Partial<WidgetConfig>) {
    const existingUpdates = pendingUpdates.get(id) || {};
    pendingUpdates.set(id, { ...existingUpdates, ...updates });

    if (!updateTimeout) {
      updateTimeout = window.setTimeout(() => {
        flushPendingUpdates();
      }, BATCH_UPDATE_INTERVAL);
    }
  }

  function flushPendingUpdates() {
    if (pendingUpdates.size === 0) return;

    const startTime = performance.now();
    pendingUpdates.forEach((updates, id) => {
      widgetUtils.updateWidget(id, updates);
    });

    const endTime = performance.now();
    if (endTime - startTime > 16) {
      console.warn(`[DashboardCanvas] Batch update took ${(endTime - startTime).toFixed(2)}ms`);
    }

    pendingUpdates.clear();
    updateTimeout = null;
  }

  function getCachedSensorData(sensorId: string): number | null {
    const cached = sensorDataCache.get(sensorId);
    if (!cached) return null;

    const now = Date.now();
    if (now - cached.timestamp > cached.ttl) {
      sensorDataCache.delete(sensorId);
      return null;
    }

    return cached.value;
  }

  function cacheSensorData(sensorId: string, value: number, ttl: number = CACHE_TTL) {
    sensorDataCache.set(sensorId, {
      value,
      timestamp: Date.now(),
      ttl
    });
  }

  // Handle widget events with batching
  function handleWidgetUpdated(event: CustomEvent<{ id: string; updates: Partial<any> }>) {
    const { id, updates } = event.detail;
    batchUpdateWidget(id, updates);
  }

  function handleWidgetSelected(event: CustomEvent<{ id: string; multiSelect: boolean }>) {
    const { id, multiSelect } = event.detail;
    uiUtils.selectWidget(id, multiSelect);
  }

  function handleWidgetContextMenu(event: CustomEvent<{ id: string; x: number; y: number }>) {
    const { id, x, y } = event.detail;
    const menuItems: ContextMenuItem[] = [
      { type: 'item', label: 'Edit Widget', action: 'edit-widget', id: id },
      { type: 'item', label: 'Duplicate Widget', action: 'duplicate-widget', id: id },
      { type: 'separator' },
      { type: 'item', label: 'Bring to Front', action: 'bring-to-front', id: id },
      { type: 'item', label: 'Send to Back', action: 'send-to-back', id: id },
      { type: 'separator' },
      { type: 'item', label: 'Delete Widget', action: 'delete-widget', id: id, icon: 'delete-icon-class' } // Example icon
    ];
    uiUtils.showContextMenu(x, y, menuItems, id, 'widget');
  }

  function handleWidgetDelete(event: CustomEvent<{ id: string }>) {
    const { id } = event.detail;
    widgetUtils.removeWidget(id);
  }

  // Get selection rectangle for display
  let selectionRect = $derived(isSelecting ? {
    left: Math.min(selectionStart.x, selectionEnd.x),
    top: Math.min(selectionStart.y, selectionEnd.y),
    width: Math.abs(selectionEnd.x - selectionStart.x),
    height: Math.abs(selectionEnd.y - selectionStart.y)
  } : null);

  // Performance monitoring effect
  $effect(() => {
    const now = performance.now();
    const renderDuration = now - performanceMetrics.lastRenderDuration;
    
    performanceMetrics.renderCount++;
    performanceMetrics.lastRenderDuration = renderDuration;
    performanceMetrics.averageRenderDuration = 
      (performanceMetrics.averageRenderDuration * (performanceMetrics.renderCount - 1) + renderDuration) / 
      performanceMetrics.renderCount;
    
    if (performanceMetrics.renderCount % 100 === 0) {
      console.debug('[DashboardCanvas] Performance metrics:', {
        renderCount: performanceMetrics.renderCount,
        lastRenderDuration: performanceMetrics.lastRenderDuration.toFixed(2) + 'ms',
        averageRenderDuration: performanceMetrics.averageRenderDuration.toFixed(2) + 'ms',
        visibleWidgetCount: performanceMetrics.visibleWidgetCount
      });
    }
  });
</script>

<div 
  bind:this={canvasElement}
  class="dashboard-canvas w-full h-full relative overflow-auto bg-[var(--theme-background)] cursor-default"
  class:cursor-crosshair={getEditMode() === 'edit'}
  role="button"
  tabindex="0"
  oncontextmenu={handleCanvasRightClick}
  onkeydown={handleCanvasKeyDown}
  ondrop={handleDrop}
  ondragover={handleDragOver}
  data-canvas-background
>
  <!-- Canvas content area -->
  <div class="canvas-content relative min-w-full min-h-full" style="width: max(100%, 1920px); height: max(100%, 1080px);">
    
    <!-- Widgets -->
    {#each $widgetArray as baseWidget (baseWidget.id)}
    {@const widget = mapWidgetToWidgetConfig(baseWidget)}
      <WidgetContainer 
        {widget}
        on:widgetupdated={handleWidgetUpdated}
        on:widgetselected={handleWidgetSelected}
        on:widgetcontextmenu={handleWidgetContextMenu}
        on:widgetdelete={handleWidgetDelete}
      />
    {/each}

    <!-- Selection rectangle -->
    {#if selectionRect && getEditMode() === 'edit'}
      <div 
        class="selection-rectangle absolute border-2 border-blue-500 bg-blue-200 bg-opacity-20 pointer-events-none rounded"
        style="left: {selectionRect.left}px; top: {selectionRect.top}px; width: {selectionRect.width}px; height: {selectionRect.height}px;"
      ></div>
    {/if}

    <!-- Grid System -->
    <GridSystem />
  </div>

  <!-- Notification Center -->
  <NotificationCenter position="top-right" />
</div>

<style>
  .dashboard-canvas {
    position: relative;
    contain: layout style;
  }

  .canvas-content {
    position: relative;
  }

  .selection-rectangle {
    backdrop-filter: blur(1px);
    animation: selection-pulse 1s ease-in-out infinite alternate;
  }

  /* Smooth selection animation */
  @keyframes selection-pulse {
    0% {
      border-color: #3b82f6;
      background-color: rgba(59, 130, 246, 0.1);
    }
    100% {
      border-color: #60a5fa;
      background-color: rgba(96, 165, 250, 0.15);
    }
  }

  /* Optimize rendering during selection */
  .dashboard-canvas:has(:global(.selection-rectangle)) .canvas-content {
    will-change: scroll-position;
  }
</style> 