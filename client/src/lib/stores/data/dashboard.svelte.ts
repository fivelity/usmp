/**
 * Dashboard layout store using Svelte 5 runes
 * Manages dashboard configuration with validation and error handling
 */

import type {
  DashboardLayout,
  BackgroundSettings,
  GridSettings,
} from "$lib/types/dashboard";

/**
 * Default dashboard layout configuration
 */
const DEFAULT_LAYOUT: DashboardLayout = {
  // Legacy fields (kept for backward compatibility)
  grid_size: [100, 100],
  background_color: "#1a1a1a",
  show_grid: true,
  grid_color: "#333333",
  background_opacity: 1,

  // Required fields
  canvas_width: 1920,
  canvas_height: 1080,
  background_type: "solid",
  background_settings: {
    color: "#1a1a1a",
  },
  grid_settings: {
    visible: true,
    snap: true,
    color: "#333333",
    size: 20,
  },
};

/**
 * Validation utilities for dashboard configuration
 */
const validateBackgroundSettings = (settings: BackgroundSettings): void => {
  if (!settings || typeof settings !== "object") {
    throw new Error("Invalid background settings: must be an object");
  }

  if (settings.color && typeof settings.color !== "string") {
    throw new Error("Invalid background color: must be a string");
  }

  if (settings.image && typeof settings.image !== "string") {
    throw new Error("Invalid background image: must be a string");
  }

  if (
    settings.gradient &&
    (!Array.isArray(settings.gradient) || settings.gradient.length !== 2)
  ) {
    throw new Error(
      "Invalid background gradient: must be an array of two strings",
    );
  }
};

const validateGridSettings = (settings: GridSettings): void => {
  if (!settings || typeof settings !== "object") {
    throw new Error("Invalid grid settings: must be an object");
  }

  if (typeof settings.visible !== "boolean") {
    throw new Error("Invalid grid visible setting: must be a boolean");
  }

  if (typeof settings.snap !== "boolean") {
    throw new Error("Invalid grid snap setting: must be a boolean");
  }

  if (typeof settings.color !== "string") {
    throw new Error("Invalid grid color: must be a string");
  }

  if (typeof settings.size !== "number" || settings.size <= 0) {
    throw new Error("Invalid grid size: must be a positive number");
  }
};

const validateDashboardLayout = (layout: DashboardLayout): void => {
  if (!layout || typeof layout !== "object") {
    throw new Error("Invalid dashboard layout: must be an object");
  }

  if (typeof layout.canvas_width !== "number" || layout.canvas_width <= 0) {
    throw new Error("Invalid canvas width: must be a positive number");
  }

  if (typeof layout.canvas_height !== "number" || layout.canvas_height <= 0) {
    throw new Error("Invalid canvas height: must be a positive number");
  }

  if (!["solid", "image", "gradient"].includes(layout.background_type)) {
    throw new Error(
      'Invalid background type: must be "solid", "image", or "gradient"',
    );
  }

  validateBackgroundSettings(layout.background_settings);
  validateGridSettings(layout.grid_settings);
};

/**
 * Create dashboard store with comprehensive functionality
 */
function createDashboardStore() {
  let layout = $state<DashboardLayout>({ ...DEFAULT_LAYOUT });

  return {
    /**
     * Get current dashboard layout
     * @returns Current dashboard layout configuration
     */
    get layout() {
      return layout;
    },

    /**
     * Set new dashboard layout with validation
     * @param newLayout - New dashboard layout configuration
     */
    setLayout(newLayout: DashboardLayout) {
      try {
        validateDashboardLayout(newLayout);
        layout = { ...newLayout };
        console.log("[DashboardStore] Layout updated successfully");
      } catch (error) {
        console.error("[DashboardStore] Error setting layout:", error);
        throw error;
      }
    },

    /**
     * Update canvas dimensions
     * @param width - Canvas width in pixels
     * @param height - Canvas height in pixels
     */
    updateCanvasDimensions(width: number, height: number) {
      try {
        if (typeof width !== "number" || width <= 0) {
          throw new Error("Invalid width: must be a positive number");
        }
        if (typeof height !== "number" || height <= 0) {
          throw new Error("Invalid height: must be a positive number");
        }

        layout = {
          ...layout,
          canvas_width: width,
          canvas_height: height,
        };
        console.log(
          `[DashboardStore] Canvas dimensions updated to ${width}x${height}`,
        );
      } catch (error) {
        console.error(
          "[DashboardStore] Error updating canvas dimensions:",
          error,
        );
        throw error;
      }
    },

    /**
     * Update background settings
     * @param settings - New background settings
     */
    updateBackgroundSettings(settings: Partial<BackgroundSettings>) {
      try {
        if (!settings || typeof settings !== "object") {
          throw new Error("Invalid background settings: must be an object");
        }

        const newSettings = { ...layout.background_settings, ...settings };
        validateBackgroundSettings(newSettings);

        layout = {
          ...layout,
          background_settings: newSettings,
        };
        console.log("[DashboardStore] Background settings updated");
      } catch (error) {
        console.error(
          "[DashboardStore] Error updating background settings:",
          error,
        );
        throw error;
      }
    },

    /**
     * Update grid settings
     * @param settings - New grid settings
     */
    updateGridSettings(settings: Partial<GridSettings>) {
      try {
        if (!settings || typeof settings !== "object") {
          throw new Error("Invalid grid settings: must be an object");
        }

        const newSettings = { ...layout.grid_settings, ...settings };
        validateGridSettings(newSettings);

        layout = {
          ...layout,
          grid_settings: newSettings,
          // Update legacy fields for backward compatibility
          show_grid: newSettings.visible,
          grid_color: newSettings.color,
        };
        console.log("[DashboardStore] Grid settings updated");
      } catch (error) {
        console.error("[DashboardStore] Error updating grid settings:", error);
        throw error;
      }
    },

    /**
     * Set background type with validation
     * @param type - Background type
     */
    setBackgroundType(type: "solid" | "image" | "gradient") {
      try {
        if (!["solid", "image", "gradient"].includes(type)) {
          throw new Error("Invalid background type");
        }

        layout = {
          ...layout,
          background_type: type,
        };
        console.log(`[DashboardStore] Background type set to ${type}`);
      } catch (error) {
        console.error("[DashboardStore] Error setting background type:", error);
        throw error;
      }
    },

    /**
     * Reset layout to defaults
     */
    resetToDefaults() {
      try {
        layout = { ...DEFAULT_LAYOUT };
        console.log("[DashboardStore] Layout reset to defaults");
      } catch (error) {
        console.error("[DashboardStore] Error resetting layout:", error);
      }
    },

    /**
     * Export dashboard configuration
     * @returns Serializable dashboard configuration
     */
    exportConfig() {
      try {
        return {
          layout: { ...layout },
          timestamp: new Date().toISOString(),
          version: "1.0.0",
        };
      } catch (error) {
        console.error("[DashboardStore] Error exporting config:", error);
        return {
          layout: { ...DEFAULT_LAYOUT },
          timestamp: new Date().toISOString(),
          version: "1.0.0",
        };
      }
    },

    /**
     * Import dashboard configuration
     * @param config - Configuration object to import
     */
    importConfig(config: {
      layout: DashboardLayout;
      timestamp?: string;
      version?: string;
    }) {
      try {
        if (!config || !config.layout) {
          throw new Error("Invalid configuration: missing layout");
        }

        validateDashboardLayout(config.layout);
        layout = { ...config.layout };
        console.log("[DashboardStore] Configuration imported successfully");
      } catch (error) {
        console.error("[DashboardStore] Error importing config:", error);
        throw error;
      }
    },

    /**
     * Get current canvas aspect ratio
     * @returns Aspect ratio as width/height
     */
    getAspectRatio(): number {
      return layout.canvas_width / layout.canvas_height;
    },

    /**
     * Check if grid is visible
     * @returns True if grid is visible
     */
    isGridVisible(): boolean {
      return layout.grid_settings.visible;
    },

    /**
     * Check if grid snap is enabled
     * @returns True if grid snap is enabled
     */
    isGridSnapEnabled(): boolean {
      return layout.grid_settings.snap;
    },

    /**
     * Get effective background color
     * @returns Background color string
     */
    getBackgroundColor(): string {
      return (
        layout.background_settings.color || layout.background_color || "#1a1a1a"
      );
    },

    /**
     * Get effective grid color
     * @returns Grid color string
     */
    getGridColor(): string {
      return layout.grid_settings.color || layout.grid_color || "#333333";
    },
  };
}

/**
 * Global dashboard store instance
 */
export const dashboard = createDashboardStore();

// Export alias for backwards compatibility
export const dashboardStore = dashboard;
