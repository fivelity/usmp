/**
 * UI State Management Store
 * Handles application UI state like edit mode, selection, context menus, etc.
 */

import { writable, derived, get } from "svelte/store";
import type { EditMode, DragState } from "$lib/types";

// Define the structure for a context menu item
interface BaseContextMenuItem {
  id?: string;
  disabled?: boolean;
  icon?: string;
  shortcut?: string;
}

interface ActionContextMenuItem extends BaseContextMenuItem {
  type: "item";
  label: string;
  action: string; // A string identifier for the action to be taken
}

interface SeparatorContextMenuItem extends BaseContextMenuItem {
  id?: never; // Separators typically don't have IDs
  type: "separator";
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

// Core UI state management using Svelte stores
const editMode = writable<EditMode>("view");
const selectedWidgets = writable<Set<string>>(new Set());
const contextMenu = writable<ContextMenuState>({
  show: false,
  x: 0,
  y: 0,
  items: [],
  targetId: undefined,
  targetType: undefined,
});
const dragState = writable<DragState>({
  isDragging: false,
  startX: 0,
  startY: 0,
  currentX: 0,
  currentY: 0,
});
const showLeftSidebar = writable<boolean>(true);
const showRightSidebar = writable<boolean>(true);

// Derived state
const hasSelection = derived(
  selectedWidgets,
  ($selectedWidgets) => $selectedWidgets.size > 0,
);
const selectedWidgetCount = derived(
  selectedWidgets,
  ($selectedWidgets) => $selectedWidgets.size,
);

// Getter functions for store values
export const getEditMode = () => get(editMode);
export const getSelectedWidgets = () => get(selectedWidgets);
export const getContextMenu = () => get(contextMenu);
export const getDragState = () => get(dragState);
export const getShowLeftSidebar = () => get(showLeftSidebar);
export const getShowRightSidebar = () => get(showRightSidebar);

// UI utilities
export const uiUtils = {
  setEditMode(newMode: EditMode) {
    editMode.set(newMode);
  },

  toggleEditMode() {
    editMode.update((mode) => (mode === "edit" ? "view" : "edit"));
  },

  setSelectedWidgets(widgets: Set<string>) {
    selectedWidgets.set(widgets);
  },

  addSelectedWidget(widgetId: string) {
    selectedWidgets.update((widgets) => {
      widgets.add(widgetId);
      return widgets;
    });
  },

  removeSelectedWidget(widgetId: string) {
    selectedWidgets.update((widgets) => {
      widgets.delete(widgetId);
      return widgets;
    });
  },

  clearSelection() {
    selectedWidgets.set(new Set());
  },

  showContextMenu(
    x: number,
    y: number,
    items: ContextMenuItem[],
    targetId?: string,
    targetType?: string,
  ) {
    contextMenu.set({
      show: true,
      x,
      y,
      items,
      targetId,
      targetType,
    });
  },

  hideContextMenu() {
    contextMenu.update((menu) => ({
      ...menu,
      show: false,
    }));
  },

  setDragState(state: Partial<DragState>) {
    dragState.update((current) => ({
      ...current,
      ...state,
    }));
  },

  resetDragState() {
    dragState.set({
      isDragging: false,
      startX: 0,
      startY: 0,
      currentX: 0,
      currentY: 0,
    });
  },

  toggleLeftSidebar() {
    showLeftSidebar.update((visible) => !visible);
  },

  toggleRightSidebar() {
    showRightSidebar.update((visible) => !visible);
  },
};

// Export stores
export {
  editMode,
  selectedWidgets,
  contextMenu,
  dragState,
  showLeftSidebar,
  showRightSidebar,
  hasSelection,
  selectedWidgetCount,
};
