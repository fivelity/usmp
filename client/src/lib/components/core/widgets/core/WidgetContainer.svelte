<script lang="ts">
  import { createEventDispatcher, onMount } from 'svelte';
  import { getEditMode, getSelectedWidgets } from '$lib/stores/core/ui.svelte';
  import { configService } from '$lib/services/configService';
  import type { WidgetConfig } from '$lib/types/widgets';
  
  import WidgetContent from './WidgetContent.svelte';
  import WidgetControls from './WidgetControls.svelte';
  import ResizeHandles from '../../../ui/common/ResizeHandles.svelte';
  import WidgetBorder from './WidgetBorder.svelte';
  
  let { widget } = $props<{ widget: WidgetConfig }>();
  
  const dispatch = createEventDispatcher<{
    'widget-updated': { id: string; updates: Partial<WidgetConfig> };
    'widget-selected': { id: string; multiSelect: boolean };
    'widget-context-menu': { id: string; x: number; y: number };
    'widget-delete': { id: string };
  }>();
  
  let isDragging = $state(false);
  let dragStart = { x: 0, y: 0 };
  let initialPos = { x: 0, y: 0 };
  let config = configService.getConfig();
  
  // Performance optimization
  let updateThrottle = 0;
  const throttleDelay = config.performance.widgetUpdateThrottle;
  let lastRenderTime = 0;
  let frameRequestId: number | null = null;
  
  // Reactive state with performance optimizations
  let isSelected = $derived(getSelectedWidgets().has(widget.id));
  let isLocked = $derived(widget.is_locked);
  let showControls = $derived(getEditMode() === 'edit' && isSelected && !isLocked);
  let canEdit = $derived(getEditMode() === 'edit');
  
  // Performance monitoring
  let performanceMetrics = {
    renderCount: 0,
    lastRenderDuration: 0,
    averageRenderDuration: 0,
    updateCount: 0
  };
  
  // Throttled update function
  function throttledUpdate(updates: Partial<WidgetConfig>) {
    if (updateThrottle) {
      window.clearTimeout(updateThrottle);
    }
    
    updateThrottle = window.setTimeout(() => {
      const startTime = performance.now();
      
      dispatch('widget-updated', {
        id: widget.id,
        updates
      });
      
      performanceMetrics.updateCount++;
      const updateDuration = performance.now() - startTime;
      
      if (config.debug.showPerformanceMetrics) {
        console.debug(`[Widget ${widget.id}] Update duration: ${updateDuration.toFixed(2)}ms`);
      }
      
      updateThrottle = 0;
    }, throttleDelay);
  }
  
  // Optimized drag handling
  function handleDragStart(event: MouseEvent) {
    if (!canEdit || isLocked) return;
    
    isDragging = true;
    dragStart = { x: event.clientX, y: event.clientY };
    initialPos = { x: widget.pos_x, y: widget.pos_y };
    
    document.addEventListener('mousemove', handleDragMove);
    document.addEventListener('mouseup', handleDragEnd);
  }
  
  function handleDragMove(event: MouseEvent) {
    if (!isDragging) return;
    
    // Use requestAnimationFrame for smooth dragging
    if (frameRequestId) {
      cancelAnimationFrame(frameRequestId);
    }
    
    frameRequestId = requestAnimationFrame(() => {
      const deltaX = event.clientX - dragStart.x;
      const deltaY = event.clientY - dragStart.y;
      
      let newX = initialPos.x + deltaX;
      let newY = initialPos.y + deltaY;
      
      // Apply constraints
      newX = Math.max(0, newX);
      newY = Math.max(0, newY);
      
      // Emit update
      throttledUpdate({ pos_x: newX, pos_y: newY });
      
      frameRequestId = null;
    });
  }
  
  function handleDragEnd() {
    isDragging = false;
    if (frameRequestId) {
      cancelAnimationFrame(frameRequestId);
      frameRequestId = null;
    }
    document.removeEventListener('mousemove', handleDragMove);
    document.removeEventListener('mouseup', handleDragEnd);
  }
  
  function handleResize(event: CustomEvent<{ width: number; height: number }>) {
    const { width, height } = event.detail;
    
    // Apply size constraints
    const minWidth = config.widgets.minWidgetWidth;
    const minHeight = config.widgets.minWidgetHeight;
    const maxWidth = config.widgets.maxWidgetWidth;
    const maxHeight = config.widgets.maxWidgetHeight;
    
    const constrainedWidth = Math.max(minWidth, Math.min(maxWidth, width));
    const constrainedHeight = Math.max(minHeight, Math.min(maxHeight, height));
    
    throttledUpdate({ width: constrainedWidth, height: constrainedHeight });
  }
  
  function handleLockToggle() {
    throttledUpdate({ is_locked: !widget.is_locked });
  }
  
  function handleContainerMouseDown(event: MouseEvent) {
    if (!canEdit) return;
    
    // Handle widget selection
    if (!event.ctrlKey && !event.shiftKey) {
      dispatch('widget-selected', { id: widget.id, multiSelect: false });
    } else if (event.ctrlKey || event.shiftKey) {
      dispatch('widget-selected', { id: widget.id, multiSelect: true });
    }
    
    // Start drag if not locked
    if (!isLocked) {
      handleDragStart(event);
    }
  }
  
  function handleContainerClick(event: MouseEvent) {
    if (!canEdit) return;
    
    event.stopPropagation();
    const multiSelect = event.shiftKey || event.ctrlKey;
    dispatch('widget-selected', { id: widget.id, multiSelect });
  }
  
  function handleContextMenu(event: MouseEvent) {
    event.preventDefault();
    dispatch('widget-context-menu', {
      id: widget.id,
      x: event.clientX,
      y: event.clientY
    });
  }
  
  function handleDelete() {
    dispatch('widget-delete', { id: widget.id });
  }
  
  function handleKeyPress(event: KeyboardEvent) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      dispatch('widget-selected', { id: widget.id, multiSelect: event.ctrlKey || event.shiftKey });
    } else if (event.key === 'Delete' || event.key === 'Backspace') {
      event.preventDefault();
      handleDelete();
    }
  }
  
  onMount(() => {
    // Load configuration
    configService.loadConfig().then(loadedConfig => {
      config = loadedConfig;
    });
    
    return () => {
      // Cleanup
      if (updateThrottle) {
        window.clearTimeout(updateThrottle);
      }
      if (frameRequestId) {
        cancelAnimationFrame(frameRequestId);
      }
    };
  });
  
  // Performance monitoring
  $effect(() => {
    const now = performance.now();
    const renderDuration = now - lastRenderTime;
    
    performanceMetrics.renderCount++;
    performanceMetrics.lastRenderDuration = renderDuration;
    performanceMetrics.averageRenderDuration = 
      (performanceMetrics.averageRenderDuration * (performanceMetrics.renderCount - 1) + renderDuration) / 
      performanceMetrics.renderCount;
    
    lastRenderTime = now;
    
    if (config.debug.showPerformanceMetrics && performanceMetrics.renderCount % 100 === 0) {
      console.debug(`[Widget ${widget.id}] Performance metrics:`, {
        renderCount: performanceMetrics.renderCount,
        lastRenderDuration: performanceMetrics.lastRenderDuration.toFixed(2) + 'ms',
        averageRenderDuration: performanceMetrics.averageRenderDuration.toFixed(2) + 'ms',
        updateCount: performanceMetrics.updateCount
      });
    }
  });
</script>

<div
  
  class="widget-container absolute cursor-pointer"
  class:widget-selected={isSelected}
  class:widget-locked={isLocked}
  class:widget-dragging={isDragging}
  class:widget-edit-mode={canEdit}
  style="
    left: {widget.pos_x}px;
    top: {widget.pos_y}px;
    width: {widget.width}px;
    height: {widget.height}px;
    z-index: {widget.z_index};
    transform: rotate({widget.rotation}deg);
  "
  onmousedown={handleContainerMouseDown}
  onclick={handleContainerClick}
  oncontextmenu={handleContextMenu}
  onkeydown={handleKeyPress}
  role="button"
  tabindex="0"
>
  <!-- Widget Border and Selection Indicator -->
  <WidgetBorder {isSelected} {isLocked} {canEdit} />
  
  <!-- Widget Content -->
  <WidgetContent {widget} />
  
  <!-- Widget Controls (Edit Mode Only) -->
  {#if showControls}
    <WidgetControls 
      {widget}
      on:lock-toggle={handleLockToggle}
      on:delete={handleDelete}
    />
  {/if}
  
  <!-- Resize Handles (Edit Mode Only) -->
  {#if canEdit && !isLocked}
    <ResizeHandles 
      on:resize={handleResize}
    />
  {/if}
</div>

<style>
  .widget-container {
    transition: box-shadow 0.2s ease;
    will-change: transform;
  }
  
  .widget-container:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .widget-selected {
    box-shadow: 0 0 0 2px var(--theme-primary);
  }
  
  .widget-locked {
    opacity: 0.8;
  }
  
  .widget-dragging {
    user-select: none;
    pointer-events: none;
    z-index: 9999;
  }
  
  .widget-edit-mode {
    cursor: move;
  }
  
  .widget-edit-mode.widget-locked {
    cursor: not-allowed;
  }
</style>
