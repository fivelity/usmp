import type { LayoutLoad } from './$types';
import { apiService } from '$lib/services/api';
import { browser } from '$app/environment';

export const load: LayoutLoad = async ({ fetch: _fetch }) => {
  // This load function runs on the server during the initial page load.
  // We avoid running it on the client-side for subsequent navigations
  // because this data is foundational and not expected to change without a full reload.
  if (browser) {
    return {
      initialSensors: null,
      initialTree: null
    };
  }

  console.log('[+layout.ts] Fetching initial data on the server...');

  try {
    const sensorsResponse = await apiService.getSensors();
    const sources = sensorsResponse.success ? sensorsResponse.data.sources : null;

    let hardwareTree = null;
    if (sources && sources['librehardware_updated']?.active) {
      const treeResponse = await apiService.getHardwareTree();
      hardwareTree = treeResponse.success && treeResponse.data ? treeResponse.data.hardware : null;
    }

    console.log('[+layout.ts] Initial data fetched successfully.');
    return {
      initialSensors: sources,
      initialTree: hardwareTree
    };
  } catch (error) {
    console.error('[+layout.ts] Error fetching initial data:', error);
    return {
      initialSensors: null,
      initialTree: null,
      error: 'Failed to load initial sensor data.'
    };
  }
}; 