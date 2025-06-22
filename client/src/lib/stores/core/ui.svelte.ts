/**
 * UI State Management Store (Rune-based)
 * Handles application UI state like edit mode, selection, sidebars, context menus, etc.
 */
import type {
  EditMode,
  DragState,
  ContextMenuState,
  ContextMenuItem,
} from "$lib/types/ui";
import type { WidgetConfig } from "$lib/types/widgets";

// Core UI state
let editMode = $state<EditMode>("view");
let selectedWidgets = $state<Set<string>>(new Set());
let contextMenu = $state<ContextMenuState>({
  show: false,
  x: 0,
  y: 0,
  items: [],
  targetId: undefined,
  targetType: undefined,
});
let dragState = $state<DragState>({
  isDragging: false,
  startX: 0,
  startY: 0,
  currentX: 0,
  currentY: 0,
});
let leftSidebarVisible = $state(true);
let rightSidebarVisible = $state(false);
let clipboard = $state<WidgetConfig[] | null>(null);

// UI state and utilities object
export const ui = {
  get editMode() {
    return editMode;
  },
  get selectedWidgets() {
    return selectedWidgets;
  },
  get contextMenu() {
    return contextMenu;
  },
  get dragState() {
    return dragState;
  },
  get leftSidebarVisible() {
    return leftSidebarVisible;
  },
  get rightSidebarVisible() {
    return rightSidebarVisible;
  },
  get clipboard() {
    return clipboard;
  },
  // ADDED: New reactive getters for selection state
  get hasSelection() {
    return selectedWidgets.size > 0;
  },
  get selectedWidgetCount() {
    return selectedWidgets.size;
  },

  // Methods
  setEditMode: (newMode: EditMode) => {
    editMode = newMode;
  },
  toggleEditMode: () => {
    editMode = editMode === "edit" ? "view" : "edit";
  },
  setSelectedWidgets: (widgets: Set<string>) => {
    selectedWidgets = widgets;
  },
  addSelectedWidget: (widgetId: string) => {
    selectedWidgets.add(widgetId);
  },
  removeSelectedWidget: (widgetId: string) => {
    selectedWidgets.delete(widgetId);
  },
  clearSelection: () => {
    selectedWidgets = new Set();
  },
  showContextMenu: (
    x: number,
    y: number,
    items: ContextMenuItem[],
    targetId?: string,
    targetType?: string,
  ) => {
    contextMenu = { show: true, x, y, items, targetId, targetType };
  },
  hideContextMenu: () => {
    contextMenu.show = false;
  },
  setDragState: (state: Partial<DragState>) => {
    dragState = { ...dragState, ...state };
  },
  resetDragState: () => {
    dragState = {
      isDragging: false,
      startX: 0,
      startY: 0,
      currentX: 0,
      currentY: 0,
    };
  },
  toggleLeftSidebar: () => {
    leftSidebarVisible = !leftSidebarVisible;
  },
  toggleRightSidebar: () => {
    rightSidebarVisible = !rightSidebarVisible;
  },
  setClipboard: (widgets: WidgetConfig[]) => {
    clipboard = widgets;
  },
  clearClipboard: () => {
    clipboard = null;
  },
};

// Export reactive values separately for easier consumption
export function hasSelection() {
  return selectedWidgets.size > 0;
}

export function selectedWidgetCount() {
  return selectedWidgets.size;
}

// Additional utility functions
export function getEditMode() {
  return editMode;
}

export function getSelectedWidgets() {
  return selectedWidgets;
}
