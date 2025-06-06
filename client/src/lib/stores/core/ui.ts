/**
 * UI State Management Store
 * Handles application UI state like edit mode, selection, context menus, etc.
 */

import type { EditMode, ContextMenuState, DragState } from '$lib/types';


// Core UI state management using Svelte 5 runes
export let editMode = $state<EditMode>('view');
export let selectedWidgets = $state<Set<string>>(new Set());
export let contextMenu = $state<ContextMenuState>({
  show: false,
  x: 0,
  y: 0,
  items: []
});

export let dragState = $state<DragState>({
  isDragging: false,
  startX: 0,
  startY: 0,
  currentX: 0,
  currentY: 0
});

export let showLeftSidebar = $state<boolean>(true);
export let showRightSidebar = $state<boolean>(true);

// Derived state
export let hasSelection = $derived(selectedWidgets.size > 0);
export let selectedWidgetCount = $derived(selectedWidgets.size);

// UI utilities
export const uiUtils = {
  setEditMode(newMode: EditMode) {
    editMode = newMode;
  },

  toggleEditMode() {
    editMode = editMode === 'edit' ? 'view' : 'edit';
  },
  
  selectWidget(widgetId: string, multiSelect = false) {
    if (multiSelect) {
      selectedWidgets.add(widgetId);
    } else {
      selectedWidgets = new Set([widgetId]);
    }
  },
  
  deselectWidget(widgetId: string) {
    selectedWidgets.delete(widgetId);
  },
  
  clearSelection() {
    selectedWidgets = new Set();
  },
  
  showContextMenu(x: number, y: number, items: any[]) {
    contextMenu = {
      show: true,
      x,
      y,
      items
    };
  },
  
  hideContextMenu() {
    contextMenu.show = false;
  },
  
  startDrag(x: number, y: number) {
    dragState = {
      isDragging: true,
      startX: x,
      startY: y,
      currentX: x,
      currentY: y
    };
  },
  
  updateDrag(x: number, y: number) {
    dragState.currentX = x;
    dragState.currentY = y;
  },
  
  endDrag() {
    dragState.isDragging = false;
  },
  
  toggleLeftSidebar() {
    showLeftSidebar = !showLeftSidebar;
  },
  
  toggleRightSidebar() {
    showRightSidebar = !showRightSidebar;
  },
  
  // Bulk UI reset
  resetUI() {
    selectedWidgets = new Set();
    contextMenu = { show: false, x: 0, y: 0, items: [] };
    dragState = {
      isDragging: false,
      startX: 0,
      startY: 0,
      currentX: 0,
      currentY: 0
    };
  }
};
