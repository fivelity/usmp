<script lang="ts">
  import { ui } from '$lib/stores/core/ui.svelte';
  import { getWidgetArray, updateWidget } from '$lib/stores/data/widgets.svelte';
  import WidgetContainer from '../widgets/core/WidgetContainer.svelte';
  import GridSystem from './GridSystem.svelte';
  import NotificationCenter from '../../ui/common/NotificationCenter.svelte';
  import type { WidgetConfig, ContextMenuItem } from '$lib/types';
  import type { Point } from '$lib/types/common';

  // --- State ---
  let canvasElement: HTMLDivElement | null = $state(null);
  let isSelecting = $state(false);
  let selectionStart: Point = $state({ x: 0, y: 0 });
  let selectionEnd: Point = $state({ x: 0, y: 0 });
  let viewport = $state({ top: 0, bottom: 0, left: 0, right: 0, width: 0, height: 0 });
  let widgets = $derived(getWidgetArray());

  // --- Derived State ---
  let visibleWidgets = $derived(calculateVisibleWidgets());

  // --- Logic ---
  function calculateVisibleWidgets(): WidgetConfig[] {
    if (!canvasElement) return widgets;

    return widgets.filter((widget) => {
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
  }

  function handleWidgetUpdate(event: CustomEvent<{ id: string; updates: Partial<WidgetConfig> }>) {
    updateWidget(event.detail.id, event.detail.updates);
  }

  // --- Event Handlers ---
  function handleScroll() {
    requestAnimationFrame(updateViewport);
  }

  function handleMouseDown(event: MouseEvent) {
    if (ui.editMode !== 'edit') return;
    const target = event.target as Element;
    if (target === canvasElement || target.closest('[data-canvas-background]')) {
      startSelection(event);
    }
  }

  function handleMouseMove(event: MouseEvent) {
    if (isSelecting) {
      updateSelection(event);
    }
  }

  function handleMouseUp() {
    if (isSelecting) {
      finishSelection();
    }
  }
  
  function handleCanvasRightClick(event: MouseEvent) {
    event.preventDefault();
    const canvasMenuItems: ContextMenuItem[] = [
      { type: 'item', label: 'Add Widget', action: 'add-widget' },
      { type: 'separator' },
      { type: 'item', label: 'Paste Widget', action: 'paste-widget', disabled: !ui.clipboard },
    ];
    ui.showContextMenu(event.clientX, event.clientY, canvasMenuItems, undefined, 'canvas');
  }

  function handleWidgetRightClick(event: MouseEvent, widgetId: string) {
    event.preventDefault();
    event.stopPropagation();

    // Select the widget if it's not already part of a multi-selection
    if (!ui.selectedWidgets.has(widgetId)) {
      ui.setSelectedWidgets(new Set([widgetId]));
    }

    const menuItems: ContextMenuItem[] = [
        { type: 'item', label: 'Cut', action: 'cut-widget' },
        { type: 'item', label: 'Copy', action: 'copy-widget' },
        { type: 'separator' },
        { type: 'item', label: 'Bring to Front', action: 'bring-front' },
        { type: 'item', label: 'Send to Back', action: 'send-back' },
        { type: 'separator' },
        { type: 'item', label: 'Delete', action: 'delete-widget' },
    ];
    ui.showContextMenu(event.clientX, event.clientY, menuItems, widgetId, 'widget');
  }

  // --- Selection Logic ---
  function startSelection(event: MouseEvent) {
    isSelecting = true;
    if (!canvasElement) return;
    const rect = canvasElement.getBoundingClientRect();
    selectionStart = { x: event.clientX - rect.left, y: event.clientY - rect.top };
    selectionEnd = { ...selectionStart };
    if (!event.shiftKey) {
      ui.clearSelection();
    }
  }

  function updateSelection(event: MouseEvent) {
    if (!isSelecting || !canvasElement) return;
    const rect = canvasElement.getBoundingClientRect();
    selectionEnd = { x: event.clientX - rect.left, y: event.clientY - rect.top };
  }

  function finishSelection() {
    isSelecting = false;
    const selectionBox = {
      x1: Math.min(selectionStart.x, selectionEnd.x),
      y1: Math.min(selectionStart.y, selectionEnd.y),
      x2: Math.max(selectionStart.x, selectionEnd.x),
      y2: Math.max(selectionStart.y, selectionEnd.y)
    };

    if (selectionBox.x2 - selectionBox.x1 > 5 && selectionBox.y2 - selectionBox.y1 > 5) {
      const selectedIds = widgets
        .filter(w =>
          w.pos_x < selectionBox.x2 &&
          w.pos_x + w.width > selectionBox.x1 &&
          w.pos_y < selectionBox.y2 &&
          w.pos_y + w.height > selectionBox.y1
        )
        .map(w => w.id);
      
      ui.setSelectedWidgets(new Set(selectedIds));
    }
  }

  // --- Effects ---
  let resizeObserver: ResizeObserver | undefined;
  
  $effect(() => {
    if (!canvasElement) return;
    
    updateViewport();
    canvasElement.addEventListener('scroll', handleScroll);
    resizeObserver = new ResizeObserver(updateViewport);
    resizeObserver.observe(canvasElement);

    document.addEventListener('mousedown', handleMouseDown);
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
    
    return () => {
      if (!canvasElement) return;
      canvasElement.removeEventListener('scroll', handleScroll);
      resizeObserver?.disconnect();
      document.removeEventListener('mousedown', handleMouseDown);
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  });
</script>

<div
  bind:this={canvasElement}
  class="relative h-full w-full overflow-auto bg-[var(--theme-background)]"
  oncontextmenu={handleCanvasRightClick}
  role="region"
  aria-label="Dashboard Canvas"
>
  <GridSystem />
  
  {#if isSelecting}
    <div
      class="absolute border-2 border-dashed border-[var(--theme-primary)] bg-[var(--theme-primary-translucent)]"
      style="
        left: {Math.min(selectionStart.x, selectionEnd.x)}px;
        top: {Math.min(selectionStart.y, selectionEnd.y)}px;
        width: {Math.abs(selectionEnd.x - selectionStart.x)}px;
        height: {Math.abs(selectionEnd.y - selectionStart.y)}px;
      "
    ></div>
  {/if}

  <!-- Render only visible widgets -->
  {#each visibleWidgets as widget (widget.id)}
    <WidgetContainer
      widget={widget}
      on:widget-updated={handleWidgetUpdate}
      on:contextmenu={(e) => handleWidgetRightClick(e.detail.originalEvent, widget.id)}
    />
  {/each}

  <div data-canvas-background class="absolute inset-0 -z-10"></div>
</div>

<NotificationCenter />

<style>
  /* No styles needed here as they are handled by Tailwind classes */
</style> 