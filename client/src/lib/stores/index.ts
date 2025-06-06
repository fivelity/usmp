// Store Exports - Centralized and Modular
// This file provides clean access to all stores while maintaining backward compatibility

// Core UI State
import {
  getEditMode as editMode,
  getSelectedWidgets as selectedWidgets,
  getContextMenu,
  getDragState,
  getShowLeftSidebar,
  getShowRightSidebar,
  hasSelection,
  selectedWidgetCount,
  uiUtils,
  getEditMode,
  getSelectedWidgets,
} from "./core/ui.svelte";

export {
  editMode,
  selectedWidgets,
  getContextMenu,
  getDragState,
  getShowLeftSidebar,
  getShowRightSidebar,
  hasSelection,
  selectedWidgetCount,
  uiUtils,
  getEditMode,
  getSelectedWidgets,
};

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
} from "./data/widgets";

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
import {
  sensorData,
  sensorsBySource,
  sensorUtils,
  sensorMetadata,
  sensorHistory,
  sensorsByCategory,
  activeSensors,
  filteredSensorData,
  sensorDataUtils,
} from "./data/sensors";

export {
  sensorData,
  sensorsBySource,
  sensorUtils,
  sensorMetadata,
  sensorHistory,
  sensorsByCategory,
  activeSensors,
  filteredSensorData,
  sensorDataUtils,
};

// Available Sensors and Sources
export { availableSensors, sensorSources } from "./sensorData.svelte";

// Hardware Tree
export { hardwareTree } from "./hardwareTree";

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
} from "./history";

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
  showWidget: (id: string) => widgetUtils.updateWidget(id, { is_visible: true }),
  hideWidget: (id: string) => widgetUtils.updateWidget(id, { is_visible: false }),

  // Group management
  createGroup: widgetUtils.createGroupFromSelection,
  deleteGroup: widgetUtils.deleteGroup,
  addToGroup: widgetUtils.moveWidgetToGroup,
  removeFromGroup: widgetUtils.removeWidgetFromGroup,
  updateGroupLayout: widgetUtils.updateGroupLayout,

  // UI management
  clearSelection: uiUtils.clearSelection,
  hideContextMenu: uiUtils.hideContextMenu,
  toggleEditMode: uiUtils.toggleEditMode,

  // Visual settings management
  updateVisualSettings: visualUtils.updateSettings,
  toggleDarkMode: visualUtils.toggleTheme,
  setColorScheme: visualUtils.updateColorScheme,

  // Sensor data management
  updateSensorData: sensorUtils.updateSensorData,
  clearSensorData: sensorUtils.clearSensorData,

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
} from "$lib/types/stores";
