/**
 * Widget State Management (Rune-based)
 * Handles the state and logic for all dashboard widgets.
 */
import type { WidgetConfig } from "$lib/types";

// State
export const widgets = $state<Record<string, WidgetConfig>>({});

// Derived State
export const widgetArray = $derived(Object.values(widgets));
export const widgetGroups = $derived(
  widgetArray.reduce(
    (acc, w) => {
      const group = w.group_id || "default";
      if (!acc[group]) acc[group] = [];
      acc[group].push(w);
      return acc;
    },
    {} as Record<string, WidgetConfig[]>,
  ),
);

// This would typically be derived from the UI store's selectedWidgets state
export const selectedWidgetConfigs = $derived([]);

// Utilities
const addWidget = (widget: WidgetConfig) => {
  widgets[widget.id] = widget;
};

const removeWidget = (widgetId: string) => {
  delete widgets[widgetId];
};

const updateWidget = (widgetId: string, newConfig: Partial<WidgetConfig>) => {
  if (widgets[widgetId]) {
    widgets[widgetId] = { ...widgets[widgetId], ...newConfig };
  }
};

const selectWidget = (widgetId: string) => {
  // This should interact with the UI store
  console.log("Selecting widget:", widgetId);
};

const deselectWidget = (widgetId: string) => {
  // This should interact with the UI store
  console.log("Deselecting widget:", widgetId);
};

const clearSelectedWidgets = () => {
  // This should interact with the UI store
  console.log("Clearing selected widgets");
};

export const widgetUtils = {
  updateGroupLayout: () => {},
  lockWidgets: () => {},
  unlockWidgets: () => {},
  createGroupFromSelection: () => {},
  deleteGroup: () => {},
  moveWidgetToGroup: () => {},
  removeWidgetFromGroup: () => {},
  updateWidget,
};

// Exporting all functions
export {
  addWidget,
  removeWidget,
  updateWidget,
  selectWidget,
  deselectWidget,
  clearSelectedWidgets,
};
