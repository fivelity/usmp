/**
 * UI State Management Store
 * Handles application UI state like edit mode, selection, context menus, etc.
 */

import type { EditMode, DragState } from '$lib/types';

// Define the structure for a context menu item
interface BaseContextMenuItem {
  id?: string;
  disabled?: boolean;
  icon?: string;
  shortcut?: string;
}

interface ActionContextMenuItem extends BaseContextMenuItem {
  type: 'item';
  label: string;
  action: string; // A string identifier for the action to be taken
}

interface SeparatorContextMenuItem extends BaseContextMenuItem {
  type: 'separator';
  label?: never; // Separators typically don't have labels or actions
  action?: never;
}

export type ContextMenuItem = ActionContextMenuItem | SeparatorContextMenuItem;

// Update ContextMenuState to use the new ContextMenuItem type
export interface ContextMenuState {
  show: boolean;
  x: number;
  y: number;
  items: ContextMenuItem[];
  targetId?: string; // Optional: ID of the element the context menu is for
  targetType?: string; // Optional: Type of the element (e.g., 'widget', 'canvas')
}

// Core UI state management using Svelte 5 runes
let _editMode = $state<EditMode>('view');
let _selectedWidgets = $state(new Set<string>());
export function getSelectedWidgets() { return _selectedWidgets; }

let _contextMenu = $state<ContextMenuState>({
  show: false,
  x: 0,
  y: 0,
  items: [],
  targetId: undefined,
  targetType: undefined
});
export function getContextMenu() { return _contextMenu; }

let _dragState = $state<DragState>({
  isDragging: false,
  startX: 0,
  startY: 0,
  currentX: 0,
  currentY: 0
});
export function getDragState() { return _dragState; }

let _showLeftSidebar = $state<boolean>(true);
let _showRightSidebar = $state<boolean>(true);

// Derived state
const _hasSelection = $derived(_selectedWidgets.size > 0);
const _selectedWidgetCount = $derived(_selectedWidgets.size);

export function hasSelection() {
  return _hasSelection;
}

export function selectedWidgetCount() {
  return _selectedWidgetCount;
}

// UI utilities
export const uiUtils = {
  setEditMode(newMode: EditMode) {
    _editMode = newMode;
  },

  toggleEditMode() {
    _editMode = _editMode === 'edit' ? 'view' : 'edit';
  },
  
  selectWidget(widgetId: string, multiSelect = false) {
    if (multiSelect) {
      _selectedWidgets.add(widgetId);
    } else {
      _selectedWidgets.clear(); _selectedWidgets.add(widgetId);
    }
  },
  
  deselectWidget(widgetId: string) {
    _selectedWidgets.delete(widgetId);
  },
  
  clearSelection() {
    _selectedWidgets.clear();
  },
  
  addToSelection(widgetId: string) {
    _selectedWidgets.add(widgetId);
  },
  
  replaceSelection(widgetIds: string[]) {
    _selectedWidgets = new Set(widgetIds);
  },
  
  showContextMenu(x: number, y: number, items: ContextMenuItem[], targetId?: string, targetType?: string) {
    _contextMenu.show = true;
    _contextMenu.x = x;
    _contextMenu.y = y;
    _contextMenu.items = items;
    _contextMenu.targetId = targetId;
    _contextMenu.targetType = targetType;
  },
  
  hideContextMenu() {
    _contextMenu.show = false;
  },
  
  startDrag(x: number, y: number) {
    _dragState.isDragging = true;
    _dragState.startX = x;
    _dragState.startY = y;
    _dragState.currentX = x;
    _dragState.currentY = y;
  },
  
  updateDrag(x: number, y: number) {
    _dragState.currentX = x;
    _dragState.currentY = y;
    // The line above already correctly sets _dragState.currentY, this was a duplicate.
  },
  
  endDrag() {
    _dragState.isDragging = false;
  },
  
  toggleLeftSidebar() {
    _showLeftSidebar = !_showLeftSidebar;
  },
  
  toggleRightSidebar() {
    _showRightSidebar = !_showRightSidebar;
  },
  
  // Bulk UI reset
  resetUI() {
    _selectedWidgets.clear();
    _contextMenu.show = false;
    _contextMenu.x = 0;
    _contextMenu.y = 0;
    _contextMenu.items = [];
    _dragState.isDragging = false;
    _dragState.startX = 0;
    _dragState.startY = 0;
    _dragState.currentX = 0;
    _dragState.currentY = 0;
  }
};

// Getter functions for reassigned state
export function getEditMode() {
  return _editMode;
}

export function getShowLeftSidebar() {
  return _showLeftSidebar;
}

export function getShowRightSidebar() {
  return _showRightSidebar;
}

// All necessary exports are handled by individual 'export function ...' or 'export const uiUtils = ...'
// The direct export of reassigned state variables (selectedWidgets, contextMenu, dragState) is not allowed
// and has been replaced by getter functions (getSelectedWidgets, getContextMenu, getDragState).
