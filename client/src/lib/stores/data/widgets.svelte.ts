/**
 * Widget State Management (Rune-based)
 * Handles the state and logic for all dashboard widgets.
 */
import type { WidgetConfig } from "$lib/types";

// Internal state management - using a single state object
const state = $state({
  widgets: {} as Record<string, WidgetConfig>,
  version: 0
});

// Getter functions that maintain reactivity
export function getWidgetMap(): Record<string, WidgetConfig> {
  state.version; // Track dependency
  return { ...state.widgets };
}

export function getWidgetArray(): WidgetConfig[] {
  state.version; // Track dependency
  return Object.values(state.widgets);
}

export function getWidgetById(id: string): WidgetConfig | undefined {
  state.version; // Track dependency
  return state.widgets[id];
}

export function getWidgetGroups(): Record<string, WidgetConfig[]> {
  state.version; // Track dependency
  const groups: Record<string, WidgetConfig[]> = { default: [] };
  
  Object.values(state.widgets).forEach(widget => {
    const groupId = widget.group_id || 'default';
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
  state.widgets[widget.id] = widget;
  state.version++;
}

export function removeWidget(id: string): void {
  if (!id || !state.widgets[id]) return;
  delete state.widgets[id];
  state.version++;
}

export function updateWidget(id: string, updates: Partial<WidgetConfig>): void {
  if (!id || !updates || typeof updates !== 'object' || !state.widgets[id]) {
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
    
    if (currentType === 'string' && typeof value !== 'string') {
      // Preserve string types
      validatedUpdates[key as keyof WidgetConfig] = String(value) as any;
    } else if (currentType === 'number' && typeof value !== 'number') {
      // Convert to number if possible, otherwise skip
      const num = Number(value);
      if (!isNaN(num)) {
        validatedUpdates[key as keyof WidgetConfig] = num as any;
      }
    } else if (currentType === 'boolean' && typeof value !== 'boolean') {
      // Convert to boolean
      validatedUpdates[key as keyof WidgetConfig] = Boolean(value) as any;
    } else {
      // For other types (objects, arrays), accept as-is
      validatedUpdates[key as keyof WidgetConfig] = value as any;
    }
  }
  
  // Update the widget with validated properties
  state.widgets[id] = { ...state.widgets[id], ...validatedUpdates };
  state.version++;
}

export function setWidgets(widgets: WidgetConfig[]): void {
  if (!Array.isArray(widgets)) return;
  
  // Clear existing widgets
  Object.keys(state.widgets).forEach(key => delete state.widgets[key]);
  
  // Add new widgets
  widgets.forEach(widget => {
    if (widget?.id) {
      state.widgets[widget.id] = widget;
    }
  });
  
  state.version++;
}

// Create a widgets object that looks like the old exported widgets state
// but is actually just a proxy to our internal state
export const widgets: Record<string, WidgetConfig> = new Proxy({} as Record<string, WidgetConfig>, {
  get(target, prop) {
    // Forward property access to our internal state
    if (typeof prop === 'string') {
      state.version; // Access version to create dependency
      return state.widgets[prop];
    }
    return undefined;
  },
  set(target, prop, value) {
    // Forward property setting to our internal state
    if (typeof prop === 'string') {
      state.widgets[prop] = value;
      state.version++;
      return true;
    }
    return false;
  },
  deleteProperty(target, prop) {
    // Forward property deletion to our internal state
    if (typeof prop === 'string' && prop in state.widgets) {
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
    if (typeof prop === 'string') {
      state.version; // Access version to create dependency
      return prop in state.widgets;
    }
    return false;
  },
  getOwnPropertyDescriptor(target, prop) {
    // Get property descriptor from our internal state
    if (typeof prop === 'string') {
      state.version; // Access version to create dependency
      const value = state.widgets[prop];
      return {
        value,
        enumerable: true,
        configurable: true,
        writable: true
      };
    }
    return undefined;
  }
});

// Add backwards compatibility methods
Object.defineProperty(widgets, 'setWidgets', {
  value: setWidgets,
  configurable: true,
  enumerable: true,
  writable: true
});

// Add getWidgetMap as a method for backwards compatibility
Object.defineProperty(widgets, 'getWidgetMap', {
  value: getWidgetMap,
  configurable: true,
  enumerable: true,
  writable: true
});

// For backwards compatibility - instead of using a getter, recommend using getWidgetMap()
export function widgetMap() {
  return getWidgetMap();
}
