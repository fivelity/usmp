import { connectionStatus } from "./connectionStatus";
import { sensorStore } from "./data/sensors.svelte";
import { ui } from "./core/ui.svelte";

/**
 * Initialize all stores with default values
 */
export async function initializeStores() {
  console.log("[StoreInitialization] Initializing all stores...");

  // Reset connection state
  connectionStatus.set("disconnected");

  // Clear all sensor data, history, and metadata
  sensorStore.clearAllSensors();

  // Set default UI state
  ui.setEditMode("view");

  console.log("[StoreInitialization] All stores initialized");
}
