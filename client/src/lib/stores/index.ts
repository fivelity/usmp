// Store Exports - Centralized and Modular
// This file provides clean access to all stores while maintaining backward compatibility

// Core UI State
export {
  editMode,
  selectedWidgets,
  contextMenu,
  dragState,
  showLeftSidebar,
  showRightSidebar,
  hasSelection,
  selectedWidgetCount,
  uiUtils,
} from "./core/ui.svelte"

// Sensor State
export {
  sensorData,
  sensorSources,
  availableSensors,
  hardwareTree,
  activeSensors,
  sensorCategories,
  sensorUtils,
} from "./sensorData"

// Visual Settings State
export {
  visualSettings,
  visualUtils,
} from "./core/visual"

// Widget Data State
export {
  widgets,
  widgetGroups,
  widgetArray,
  selectedWidgetConfigs,
  widgetUtils,
} from "./data/widgets"

// Dashboard Layout
export { dashboardLayout } from "./dashboardLayout"

// History State
export { historyStore } from "./history"

// Theme State
export {
  currentTheme,
  activeColorScheme,
  activeThemePreset,
  themePresets,
  colorSchemes,
  themeUtils
} from "./themes"

// Initialize all stores
export { initializeStores } from "./initialization"

// Connection Status
export { connectionStatus } from "./connectionStatus"

// Import utilities for comprehensive storeUtils
import { widgetUtils } from "./data/widgets"
import { uiUtils } from "./core/ui.svelte"
import { visualUtils } from "./core/visual"
import { sensorData } from "./data/sensors"
import { sensorSources } from "./sensorSources"
import { availableSensors } from "./availableSensors"
import { hardwareTree } from "./hardwareTree"
import type { SensorData, SensorInfo, SensorSourceFromAPI, SensorSource } from "$lib/types"

// Comprehensive backward compatibility utilities
export const storeUtils = {
  // Widget management (from widgetUtils)
  ...widgetUtils,

  // UI management (from uiUtils)
  ...uiUtils,

  // Visual settings management (from visualUtils)
  updateVisualSettings: visualUtils.updateSettings,

  // Sensor data management
  updateSensorData: (data: Record<string, SensorData>) => {
    sensorData.set(data)
  },

  updateSensorSources: (apiPayload: Record<string, SensorSourceFromAPI> | null | undefined) => {
    const newAvailableSensors: SensorInfo[] = []
    const newSensorSourcesForStore: SensorSource[] = []

    if (apiPayload && typeof apiPayload === "object") {
      const sourcesFromAPIArray: SensorSourceFromAPI[] = Object.values(apiPayload)

      for (const sourceAPI of sourcesFromAPIArray) {
        if (sourceAPI && sourceAPI.active && sourceAPI.sensors && typeof sourceAPI.sensors === "object") {
          const currentSourceSensors: SensorData[] = []
          for (const sensor_data_item of Object.values(sourceAPI.sensors)) {
            if (sensor_data_item) {
              newAvailableSensors.push({
                id: sensor_data_item.id,
                name: sensor_data_item.name,
                category: sensor_data_item.category,
                unit: sensor_data_item.unit,
                source: sourceAPI.id,
              })
              currentSourceSensors.push(sensor_data_item)
            }
          }
          newSensorSourcesForStore.push({
            id: sourceAPI.id,
            name: sourceAPI.name,
            active: sourceAPI.active,
            sensors: currentSourceSensors,
            last_update: sourceAPI.last_update,
            error_message: sourceAPI.error_message,
          })
        } else if (sourceAPI) {
          newSensorSourcesForStore.push({
            id: sourceAPI.id,
            name: sourceAPI.name,
            active: sourceAPI.active,
            sensors: [],
            last_update: sourceAPI.last_update,
            error_message: sourceAPI.error_message,
          })
        }
      }
    }

    sensorSources.set(newSensorSourcesForStore)
    availableSensors.set(newAvailableSensors)
  },

  updateHardwareTree: (tree: any[] | any) => {
    const treeArray = Array.isArray(tree) ? tree : tree ? [tree] : []
    hardwareTree.set(treeArray)
  },
}
