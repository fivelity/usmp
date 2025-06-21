import type { LayoutLoad } from "./$types";
import { browser } from "$app/environment";
import { apiService } from "$lib/services/api";
import {
  updateSensorSources,
  updateHardwareTree,
} from "$lib/stores/sensorData";

export const load: LayoutLoad = async ({ fetch: _fetch }) => {
  // This load function runs on the server during the initial page load.
  // We avoid running it on the client-side for subsequent navigations
  // because this data is foundational and not expected to change without a full reload.
  if (browser) {
    return;
  }

  console.log("[+layout.ts] Fetching initial data on the server...");

  try {
    const sensorsResponse = await apiService.getSensors();
    const sources = sensorsResponse.success
      ? sensorsResponse.data.sources
      : null;
    if (sources) {
      updateSensorSources(sources);
    }

    let hardwareTree = null;
    if (sources && sources["librehardware_updated"]?.active) {
      const treeResponse = await apiService.getHardwareTree();
      hardwareTree =
        treeResponse.success && treeResponse.data
          ? treeResponse.data.hardware
          : null;
      if (hardwareTree) {
        updateHardwareTree(hardwareTree);
      }
    }

    console.log("[+layout.ts] Initial data fetched successfully.");
  } catch (error) {
    console.error("[+layout.ts] Error fetching initial data:", error);
    // We don't return an error object to the page, just log it.
    // The page can gracefully handle the absence of data.
  }
};
