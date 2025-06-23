// Store Exports - Centralized and Modular
// This file provides clean access to all stores while maintaining backward compatibility

// Core UI State
import { ui, hasSelection, selectedWidgetCount } from "./core/ui.svelte";

export { ui, hasSelection, selectedWidgetCount };

// Re-export selectedWidgets for easier access
export const selectedWidgets = ui.selectedWidgets;

// Re-export sensor utilities
export { availableSensors } from "./data/sensors.svelte";

// Widget Data State
import {
  widgets,
  widgetGroups,
  widgetArray,
  selectedWidgetConfigs,
  widgetUtils,
  addWidget,
  removeWidget,
  updateWidget,
  clearSelectedWidgets,
  selectWidget,
  deselectWidget,
} from "./data/widgets.svelte";

export {
  widgets,
  widgetGroups,
  widgetArray,
  selectedWidgetConfigs,
  widgetUtils,
  addWidget,
  removeWidget,
  updateWidget,
  clearSelectedWidgets,
  selectWidget,
  deselectWidget,
};

// Sensor Data State
export * from "./data/sensors.svelte";

// Dashboard Layout
import { dashboardLayout } from "./dashboardLayout";
export { dashboardLayout };

// History State
export {
  historyStore,
  MoveWidgetCommand,
  ResizeWidgetCommand,
  AddWidgetCommand,
  RemoveWidgetCommand,
  UpdateWidgetCommand,
  GroupWidgetsCommand,
  BatchCommand,
} from "./history.svelte";

// Theme State
export {
  currentTheme,
  activeColorScheme,
  activeThemePreset,
  themePresets,
  colorSchemes,
  themeUtils,
} from "./themes";

// Connection Status
export { connectionStatus } from "./connectionStatus";

// Notification State
export { notifications, notify } from "./notifications";

// System Status
import { systemStatus } from "./systemStatus";
export { systemStatus };

// Visual Settings
import {
  visualSettings,
  visualUtils,
  gridUtils,
  computedVisualSettings,
  getIsDarkMode,
  getIsHighContrast,
  getHasAnimations,
} from "./core/visual.svelte";

export {
  visualSettings,
  visualUtils,
  gridUtils,
  computedVisualSettings,
  getIsDarkMode,
  getIsHighContrast,
  getHasAnimations,
};

// Store Utilities
export { initializeStores } from "./initialization";

import { updateSensorData, updateHardwareTree } from "./sensorData";

// Store Utilities
export const storeUtils = {
  // Widget management
  addWidget,
  removeWidget,
  updateWidget,
  clearAllWidgets: clearSelectedWidgets,
  moveWidget: widgetUtils.updateGroupLayout,
  resizeWidget: widgetUtils.updateGroupLayout,
  lockWidget: widgetUtils.lockWidgets,
  unlockWidget: widgetUtils.unlockWidgets,
  showWidget: (id: string) =>
    widgetUtils.updateWidget(id, { is_visible: true }),
  hideWidget: (id: string) =>
    widgetUtils.updateWidget(id, { is_visible: false }),

  // Group management
  createGroup: widgetUtils.createGroupFromSelection,
  deleteGroup: widgetUtils.deleteGroup,
  addToGroup: widgetUtils.moveWidgetToGroup,
  removeFromGroup: widgetUtils.removeWidgetFromGroup,
  updateGroupLayout: widgetUtils.updateGroupLayout,

  // UI management
  clearSelection: ui.clearSelection,
  selectWidget: ui.selectWidget,
  hideContextMenu: ui.hideContextMenu,
  toggleEditMode: ui.toggleEditMode,

  // Visual settings management
  updateVisualSettings: visualUtils.updateSettings,
  toggleDarkMode: visualUtils.toggleTheme,
  setColorScheme: visualUtils.updateColorScheme,

  // Sensor data management
  updateSensorData,
  updateHardwareTree,

  // System management
  addSystemEvent: systemStatus.addEvent,
  clearSystemEvents: systemStatus.clearEvents,
};

// Export types
export type {
  UIState,
  WidgetState,
  SensorState,
  DashboardState,
  VisualState,
  SystemState,
  StoreUtils,
  StoreInitialization,
  Store,
} from "$lib/types/stores.d";
