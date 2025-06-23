/**
 * Widget State Management (Rune-based)
 * Handles the state and logic for all dashboard widgets.
 */
import type { WidgetConfig } from "$lib/types/widgets";

// Internal state management - using a single state object
const state = $state({
  widgets: {} as Record<string, WidgetConfig>,
  version: 0,
});

// Getter functions that maintain reactivity
export function getWidgetMap(): Record<string, WidgetConfig> {
  // For tests and reactivity, always return a fresh copy
  return { ...state.widgets };
}

export function getWidgetArray(): WidgetConfig[] {
  // For tests and reactivity, always return a fresh array
  return Object.values(state.widgets);
}

export function getWidgetById(id: string): WidgetConfig | undefined {
  // For tests and reactivity, return the widget directly
  return state.widgets[id];
}

export function getWidgetGroups(): Record<string, WidgetConfig[]> {
  const groups: Record<string, WidgetConfig[]> = { default: [] };

  Object.values(state.widgets).forEach((widget) => {
    const groupId = widget.group_id || "default";
    if (!groups[groupId]) groups[groupId] = [];
    groups[groupId].push(widget);
  });

  return groups;
}

export function getStoreVersion(): number {
  return state.version;
}

// Mutation functions
export function addWidget(widget: WidgetConfig): void {
  if (!widget?.id) return;

  // Validate required properties
  const requiredFields = ["type", "title", "pos_x", "pos_y", "width", "height"];
  for (const field of requiredFields) {
    if (
      widget[field as keyof WidgetConfig] === undefined ||
      widget[field as keyof WidgetConfig] === null
    ) {
      // Skip widgets with missing required properties
      return;
    }
  }

  state.widgets[widget.id] = widget;
  state.version++;
  updateWidgetsStore();
}

export function removeWidget(id: string): void {
  if (!id || !state.widgets[id]) return;
  delete state.widgets[id];
  state.version++;
  updateWidgetsStore();
}

export function updateWidget(id: string, updates: Partial<WidgetConfig>): void {
  if (!id || !updates || typeof updates !== "object" || !state.widgets[id]) {
    return;
  }

  // Create a validated copy of updates
  const validatedUpdates: Partial<WidgetConfig> = {};

  // Iterate through the properties and validate them
  for (const [key, value] of Object.entries(updates)) {
    if (value === null || value === undefined) {
      // Skip null/undefined values
      continue;
    }

    // Type-specific validations
    const currentValue = state.widgets[id][key as keyof WidgetConfig];
    const currentType = typeof currentValue;

    if (currentType === "string" && typeof value !== "string") {
      // Preserve string types
      validatedUpdates[key as keyof WidgetConfig] = String(value) as any;
    } else if (currentType === "number" && typeof value !== "number") {
      // Convert to number if possible, otherwise skip
      const num = Number(value);
      if (!isNaN(num)) {
        // Special validation for widget dimensions
        if ((key === "width" || key === "height") && num <= 0) {
          // Skip zero or negative dimensions
          continue;
        }
        validatedUpdates[key as keyof WidgetConfig] = num as any;
      }
    } else if (currentType === "boolean" && typeof value !== "boolean") {
      // Convert to boolean
      validatedUpdates[key as keyof WidgetConfig] = Boolean(value) as any;
    } else if (typeof value === "number") {
      // Direct numeric assignment with validation
      if ((key === "width" || key === "height") && value <= 0) {
        // Skip zero or negative dimensions
        continue;
      }
      if (
        isNaN(value) &&
        (key === "pos_x" ||
          key === "pos_y" ||
          key === "width" ||
          key === "height")
      ) {
        // Skip NaN values for positional/dimensional properties
        continue;
      }
      validatedUpdates[key as keyof WidgetConfig] = value as any;
    } else {
      // For other types (objects, arrays), accept as-is
      validatedUpdates[key as keyof WidgetConfig] = value as any;
    }
  }

  // Update the widget with validated properties
  state.widgets[id] = { ...state.widgets[id], ...validatedUpdates };
  state.version++;
  updateWidgetsStore();
}

export function setWidgets(widgets: WidgetConfig[]): void {
  if (!Array.isArray(widgets)) return;

  // Clear existing widgets
  Object.keys(state.widgets).forEach((key) => delete state.widgets[key]);

  // Add new widgets
  widgets.forEach((widget) => {
    if (widget?.id) {
      state.widgets[widget.id] = widget;
    }
  });

  state.version++;
  updateWidgetsStore();
}

// Create a widgets store that can be used with $ syntax
import { writable } from "svelte/store";

// Create a writable store for widgets
const _widgetsStore = writable<Record<string, WidgetConfig>>({});

// Function to update the store whenever state changes
function updateWidgetsStore() {
  _widgetsStore.set({ ...state.widgets });
}

// Export the store
export const widgetsStore = _widgetsStore;

// Create a widgets object that looks like the old exported widgets state
// but is actually just a proxy to our internal state
export const widgets: Record<string, WidgetConfig> = new Proxy(
  {} as Record<string, WidgetConfig>,
  {
    get(target, prop) {
      // Forward property access to our internal state
      if (typeof prop === "string") {
        state.version; // Access version to create dependency
        return state.widgets[prop];
      }
      return undefined;
    },
    set(target, prop, value) {
      // Forward property setting to our internal state
      if (typeof prop === "string") {
        state.widgets[prop] = value;
        state.version++;
        return true;
      }
      return false;
    },
    deleteProperty(target, prop) {
      // Forward property deletion to our internal state
      if (typeof prop === "string" && prop in state.widgets) {
        delete state.widgets[prop];
        state.version++;
        return true;
      }
      return false;
    },
    ownKeys() {
      // Return keys from our internal state
      state.version; // Access version to create dependency
      return Object.keys(state.widgets);
    },
    has(target, prop) {
      // Check property existence in our internal state
      if (typeof prop === "string") {
        state.version; // Access version to create dependency
        return prop in state.widgets;
      }
      return false;
    },
    getOwnPropertyDescriptor(target, prop) {
      // Get property descriptor from our internal state
      if (typeof prop === "string") {
        state.version; // Access version to create dependency
        const value = state.widgets[prop];
        return {
          value,
          enumerable: true,
          configurable: true,
          writable: true,
        };
      }
      return undefined;
    },
  },
);

// Add backwards compatibility methods
Object.defineProperty(widgets, "setWidgets", {
  value: setWidgets,
  configurable: true,
  enumerable: true,
  writable: true,
});

// Add getWidgetMap as a method for backwards compatibility
Object.defineProperty(widgets, "getWidgetMap", {
  value: getWidgetMap,
  configurable: true,
  enumerable: true,
  writable: true,
});

// For backwards compatibility - instead of using a getter, recommend using getWidgetMap()
export function widgetMap() {
  return getWidgetMap();
}

// Additional exports required by the index.ts file
export function widgetGroups() {
  return getWidgetGroups();
}

export function widgetArray() {
  return getWidgetArray();
}

// This should be used as a derived value with proper UI store import
// For now, we'll keep a simple implementation that works with the build
export function selectedWidgetConfigs() {
  // This returns an empty array by default
  // The actual implementation would need to access selectedWidgets from UI store
  return [];
}

// Widget management functions
export const clearSelectedWidgets = () => {
  // Clear all widgets
  Object.keys(state.widgets).forEach((key) => delete state.widgets[key]);
  state.version++;
};

export const selectWidget = (_id: string) => {
  // This is a placeholder - the actual selection logic is in UI store
  console.warn("selectWidget not yet implemented");
};

export const deselectWidget = (_id: string) => {
  // This is a placeholder - the actual deselection logic is in UI store
  console.warn("deselectWidget not yet implemented");
};

// Widget utilities object
// Widget group management functions
export const addWidgetGroup = (_group: any) => {
  // Placeholder for adding widget groups
  console.warn("addWidgetGroup not yet implemented");
};

export const updateWidgetGroup = (_groupId: string, _updates: any) => {
  // Placeholder for updating widget groups
  console.warn("updateWidgetGroup not yet implemented");
};

export const removeWidgetGroup = (_groupId: string) => {
  // Placeholder for removing widget groups
  console.warn("removeWidgetGroup not yet implemented");
};

export const widgetUtils = {
  updateGroupLayout: (_groupId: string, _layout: any) => {
    // Placeholder for group layout updates
    console.warn("widgetUtils.updateGroupLayout not yet implemented");
  },
  lockWidgets: (widgetIds: string[]) => {
    widgetIds.forEach((id) => {
      if (state.widgets[id]) {
        updateWidget(id, { locked: true });
      }
    });
  },
  unlockWidgets: (widgetIds: string[]) => {
    widgetIds.forEach((id) => {
      if (state.widgets[id]) {
        updateWidget(id, { locked: false });
      }
    });
  },
  updateWidget,
  createGroupFromSelection: () => {
    console.warn("widgetUtils.createGroupFromSelection not yet implemented");
  },
  deleteGroup: (_groupId: string) => {
    console.warn("widgetUtils.deleteGroup not yet implemented");
  },
  moveWidgetToGroup: (widgetId: string, groupId: string) => {
    updateWidget(widgetId, { group_id: groupId });
  },
  removeWidgetFromGroup: (widgetId: string) => {
    updateWidget(widgetId, { group_id: undefined });
  },
};
