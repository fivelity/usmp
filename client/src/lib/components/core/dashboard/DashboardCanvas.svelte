<script lang="ts">
  import { onMount } from 'svelte';
  import { editMode, selectedWidgets } from '$lib/stores/core/ui';
  import { visualSettings } from '$lib/stores/core/visual';
  import { widgetArray } from '$lib/stores/data/widgets';
  import { uiUtils } from '$lib/stores/core/ui';
  import { widgetUtils } from '$lib/stores/data/widgets';
  import { notifications } from '$lib/stores/notifications';
  import WidgetContainer from '../widgets/core/WidgetContainer.svelte';
  import GridSystem from './GridSystem.svelte';
  import NotificationCenter from '../../ui/common/NotificationCenter.svelte';
  import type { Point } from '$lib/types';

  let canvasElement: HTMLDivElement = $state();
  let isSelecting = $state(false);
  let selectionStart: Point = $state({ x: 0, y: 0 });
  let selectionEnd: Point = $state({ x: 0, y: 0 });

  onMount(() => {
    // Handle canvas interactions
    const handleMouseDown = (event: MouseEvent) => {
      if ($editMode !== 'edit') return;
      
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
        canvasElement.dispatchEvent(new CustomEvent('canvas-resize'));
      }
    };

    canvasElement.addEventListener('mousedown', handleMouseDown);
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
    window.addEventListener('resize', handleResize);

    return () => {
      canvasElement.removeEventListener('mousedown', handleMouseDown);
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
      window.removeEventListener('resize', handleResize);
    };
  });

  function startSelection(event: MouseEvent) {
    isSelecting = true;
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
    
    const rect = canvasElement.getBoundingClientRect();
    selectionEnd = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
    };
  }

  function finishSelection(event: MouseEvent) {
    if (!isSelecting) return;
    
    isSelecting = false;
    
    // Calculate selection rectangle
    const selectionRect = {
      x: Math.min(selectionStart.x, selectionEnd.x),
      y: Math.min(selectionStart.y, selectionEnd.y),
      width: Math.abs(selectionEnd.x - selectionStart.x),
      height: Math.abs(selectionEnd.y - selectionStart.y)
    };

    // Only select if there's a meaningful selection area
    if (selectionRect.width > 5 && selectionRect.height > 5) {
      // Find widgets that intersect with selection rectangle
      const selectedIds: string[] = [];
      
      $widgetArray.forEach(widget => {
        const widgetRect = {
          x: widget.pos_x,
          y: widget.pos_y,
          width: widget.width,
          height: widget.height
        };
        
        // Check if rectangles intersect
        if (rectanglesIntersect(selectionRect, widgetRect)) {
          selectedIds.push(widget.id);
        }
      });
      
      if (selectedIds.length > 0) {
        if (event.shiftKey) {
          // Add to existing selection
          selectedIds.forEach(id => uiUtils.addToSelection(id));
        } else {
          // Replace selection
          selectedWidgets.set({ type: 'widget', ids: selectedIds });
        }
      }
    }
  }

  function rectanglesIntersect(rect1: any, rect2: any): boolean {
    return !(rect2.x > rect1.x + rect1.width || 
             rect2.x + rect2.width < rect1.x || 
             rect2.y > rect1.y + rect1.height ||
             rect2.y + rect2.height < rect1.y);
  }

  function handleCanvasRightClick(event: MouseEvent) {
    if ($editMode !== 'edit') return;
    
    event.preventDefault();
    uiUtils.showContextMenu(event.clientX, event.clientY, { type: 'canvas' });
  }

  function handleCanvasKeyDown(event: KeyboardEvent) {
    if ($editMode !== 'edit') return;
    
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

  // Handle widget events
  function handleWidgetUpdated(event: CustomEvent<{ id: string; updates: Partial<any> }>) {
    const { id, updates } = event.detail;
    widgetUtils.updateWidget(id, updates);
  }

  function handleWidgetSelected(event: CustomEvent<{ id: string; multiSelect: boolean }>) {
    const { id, multiSelect } = event.detail;
    uiUtils.selectWidget(id, multiSelect);
  }

  function handleWidgetContextMenu(event: CustomEvent<{ id: string; x: number; y: number }>) {
    const { id, x, y } = event.detail;
    uiUtils.showContextMenu(x, y, { type: 'widget', id });
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
</script>

<div 
  bind:this={canvasElement}
  class="dashboard-canvas w-full h-full relative overflow-auto bg-[var(--theme-background)] cursor-default"
  class:cursor-crosshair={$editMode === 'edit'}
  role="button"
  tabindex="0"
  on:contextmenu={handleCanvasRightClick}
  on:keydown={handleCanvasKeyDown}
  on:drop={handleDrop}
  on:dragover={handleDragOver}
  data-canvas-background
>
  <!-- Canvas content area -->
  <div class="canvas-content relative min-w-full min-h-full" style="width: max(100%, 1920px); height: max(100%, 1080px);">
    
    <!-- Widgets -->
    {#each $widgetArray as widget (widget.id)}
      <WidgetContainer 
        {widget}
        onwidgetupdated={handleWidgetUpdated}
        onwidgetselected={handleWidgetSelected}
        onwidgetcontextmenu={handleWidgetContextMenu}
        onwidgetdelete={handleWidgetDelete}
      />
    {/each}

    <!-- Selection rectangle -->
    {#if selectionRect && $editMode === 'edit'}
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