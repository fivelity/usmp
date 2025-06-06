// Store Exports - Centralized and Modular
// This file provides clean access to all stores while maintaining backward compatibility

// Core UI State
export {
  getEditMode,
  getSelectedWidgets,
  getContextMenu,
  getDragState,
  getShowLeftSidebar,
  getShowRightSidebar,
  hasSelection,
  selectedWidgetCount,
  uiUtils,
} from "./core/ui.svelte";

// Sensor State
import {
  sensorData as _sensorData,
  sensorSources as _sensorSources,
  availableSensors as _availableSensors,
  hardwareTree as _hardwareTree,
  activeSensors as _activeSensors,
  sensorCategories as _sensorCategories,
  sensorUtils as _sensorUtils,
} from "./sensorData.svelte";

export const sensorData = _sensorData;
export const sensorSources = _sensorSources;
export const availableSensors = _availableSensors;
export const hardwareTree = _hardwareTree;
export const activeSensors = _activeSensors;
export const sensorCategories = _sensorCategories;
export const sensorUtils = _sensorUtils;

// Visual Settings State
export { visualSettings, visualUtils } from "./core/visual.svelte";

// Widget Data State
export {
  widgets,
  widgetGroups,
  widgetArray,
  selectedWidgetConfigs,
  widgetUtils,
} from "./data/widgets";

// Dashboard Layout
export { dashboardLayout } from "./dashboardLayout";

// History State
export { historyStore } from "./history";

// Theme State
export {
  currentTheme,
  activeColorScheme,
  activeThemePreset,
  themePresets,
  colorSchemes,
  themeUtils,
} from "./themes";

// Initialize all stores
export { initializeStores } from "./initialization";

// Connection Status
export { connectionStatus } from "./connectionStatus";

// Import utilities for comprehensive storeUtils
import { widgetUtils } from "./data/widgets";
import { uiUtils } from "./core/ui.svelte";
import { visualUtils } from "./core/visual.svelte";

import { sensorUtils as importedSensorUtils } from "./sensorData.svelte";

// Comprehensive backward compatibility utilities
export const storeUtils = {
  // Widget management (from widgetUtils)
  ...widgetUtils,

  // UI management (from uiUtils)
  ...uiUtils,

  // Visual settings management (from visualUtils)
  updateVisualSettings: visualUtils.updateSettings,

  // Sensor data management (now from sensorUtils in sensorData.svelte.ts)
  ...importedSensorUtils,
};
