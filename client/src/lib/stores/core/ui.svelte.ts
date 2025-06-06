/**
 * UI State Management Store
 * Handles application UI state like edit mode, selection, context menus, etc.
 */

import type { EditMode, ContextMenuState, DragState } from '$lib/types';


// Core UI state management using Svelte 5 runes
let editMode = $state<EditMode>('view');
const selectedWidgets = $state<Set<string>>(new Set());
const contextMenu = $state<ContextMenuState>({
  show: false,
  x: 0,
  y: 0,
  items: []
});

const dragState = $state<DragState>({
  isDragging: false,
  startX: 0,
  startY: 0,
  currentX: 0,
  currentY: 0
});

let showLeftSidebar = $state<boolean>(true);
let showRightSidebar = $state<boolean>(true);

// Derived state
export const hasSelection = $derived(selectedWidgets.size > 0);
export const selectedWidgetCount = $derived(selectedWidgets.size);

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
      selectedWidgets.clear(); selectedWidgets.add(widgetId);
    }
  },
  
  deselectWidget(widgetId: string) {
    selectedWidgets.delete(widgetId);
  },
  
  clearSelection() {
    selectedWidgets.clear();
  },
  
  showContextMenu(x: number, y: number, items: any[]) {
    contextMenu.show = true;
    contextMenu.x = x;
    contextMenu.y = y;
    contextMenu.items = items;
  },
  
  hideContextMenu() {
    contextMenu.show = false;
  },
  
  startDrag(x: number, y: number) {
    dragState.isDragging = true;
    dragState.startX = x;
    dragState.startY = y;
    dragState.currentX = x;
    dragState.currentY = y;
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
    selectedWidgets.clear();
    contextMenu.show = false;
    contextMenu.x = 0;
    contextMenu.y = 0;
    contextMenu.items = [];
    dragState.isDragging = false;
    dragState.startX = 0;
    dragState.startY = 0;
    dragState.currentX = 0;
    dragState.currentY = 0;
  }
};

export {
  editMode,
  selectedWidgets,
  contextMenu,
  dragState,
  showLeftSidebar,
  showRightSidebar
};
