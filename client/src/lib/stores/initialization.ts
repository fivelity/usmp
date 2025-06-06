import { connectionStatus } from "./connectionStatus";
import { sensorUtils } from "./sensorData.svelte";
import { uiUtils } from "./core/ui.svelte";

/**
 * Initialize all stores with default values
 */
export async function initializeStores() {
  console.log("[StoreInitialization] Initializing all stores...");

  // Reset connection state
  connectionStatus.set("disconnected");

  // Clear sensor data
  sensorUtils.updateSensorData({});
  sensorUtils.updateSensorSources(null); // This updates both sensorSources and availableSensors
  sensorUtils.updateHardwareTree([]);

  // Set default UI state
  uiUtils.setEditMode("view");

  console.log("[StoreInitialization] All stores initialized");
}
