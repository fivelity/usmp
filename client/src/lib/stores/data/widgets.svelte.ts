/**
 * Widget State Management (Rune-based)
 * Handles the state and logic for all dashboard widgets.
 */
import type { WidgetConfig } from "$lib/types";

// State
export const widgets = $state<Record<string, WidgetConfig>>({});

// Alias to expose the raw widget record for external consumers (e.g. import/export tooling)
/**
 * Reactive alias to the internal `widgets` record.  This is intentionally **read-only**
 * outside of this module – use the provided utilities (`addWidget`, `removeWidget`,
 * `updateWidget`, `setWidgets`, …) to mutate state.  Top-level components like
 * `TopBar.svelte` rely on this alias for exporting the current dashboard preset.
 */
export const widgetMap = widgets;

// Derived State
export const widgetArray = $derived((): WidgetConfig[] =>
  Object.values(widgets) as WidgetConfig[],
);

export const widgetGroups = $derived((): Record<string, WidgetConfig[]> => {
  const groups: Record<string, WidgetConfig[]> = {};
  for (const w of Object.values(widgets) as WidgetConfig[]) {
    const group = w.group_id ?? "default";
    (groups[group] ??= []).push(w);
  }
  return groups;
});

// Placeholder – will later derive from UI selection state
export const selectedWidgetConfigs = $derived((): WidgetConfig[] => []);

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

/**
 * Replace the entire widget collection with a new set.
 *
 * This is primarily used when importing or loading a preset that already
 * contains a fully-formed array of `WidgetConfig` objects.
 */
const setWidgets = (newWidgets: WidgetConfig[]): void => {
  // Clear existing keys
  Object.keys(widgets).forEach((key) => delete widgets[key]);

  // Repopulate from the incoming array, safeguarding against duplicate IDs.
  for (const widget of newWidgets) {
    widgets[widget.id] = widget;
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
  setWidgets,
};

// Backwards-compatibility: expose setWidgets directly on the reactive record so
// legacy imports (`widgets.setWidgets(...)`) still compile.
(widgets as unknown as { setWidgets: typeof setWidgets }).setWidgets = setWidgets;

// Backwards-compatibility: expose widgetMap as a property for legacy `widgets.widgetMap`
(widgets as unknown as { widgetMap: typeof widgets }).widgetMap = widgets;

// Exporting all functions
export {
  addWidget,
  removeWidget,
  updateWidget,
  setWidgets,
  selectWidget,
  deselectWidget,
  clearSelectedWidgets,
};
