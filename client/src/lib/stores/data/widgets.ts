/**
 * Widget Store
 * 
 * This file implements the widget store using Svelte's store system.
 */

import { writable, derived } from 'svelte/store';
import type { Widget, WidgetGroup, WidgetConfig, WidgetUtils } from '$lib/types';

// Core widget state
type WidgetState = Record<string, Widget>;
type WidgetGroupState = Record<string, WidgetGroup>;
type WidgetConfigState = Record<string, WidgetConfig>;

// State management
export const widgets = writable<WidgetState>({});
export const widgetGroups = writable<WidgetGroupState>({});
export const selectedWidgetConfigs = writable<WidgetConfigState>({});

// Widget management functions
export function addWidget(widget: Widget) {
  widgets.update(state => {
    state[widget.id] = widget;
    return state;
  });
}

export function updateWidget(id: string, updates: Partial<Widget>) {
  widgets.update(state => {
    if (state[id]) {
      state[id] = { ...state[id], ...updates };
    }
    return state;
  });
}

export function removeWidget(id: string) {
  widgets.update(state => {
    delete state[id];
    return state;
  });
  selectedWidgetConfigs.update(state => {
    delete state[id];
    return state;
  });
}

// Widget group management functions
export function addWidgetGroup(group: WidgetGroup) {
  widgetGroups.update(state => {
    state[group.id] = group;
    return state;
  });
}

export function updateWidgetGroup(id: string, updates: Partial<WidgetGroup>) {
  widgetGroups.update(state => {
    if (state[id]) {
      state[id] = { ...state[id], ...updates };
    }
    return state;
  });
}

export function removeWidgetGroup(id: string) {
  widgetGroups.update(state => {
    const group = state[id];
    if (group) {
      group.widgets.forEach(widgetId => {
        removeWidget(widgetId);
      });
    }
    delete state[id];
    return state;
  });
}

// Widget selection functions
export function selectWidget(id: string, config: WidgetConfig) {
  selectedWidgetConfigs.update(state => {
    state[id] = config;
    return state;
  });
}

export function deselectWidget(id: string) {
  selectedWidgetConfigs.update(state => {
    delete state[id];
    return state;
  });
}

export function clearSelectedWidgets() {
  selectedWidgetConfigs.set({});
}

// Computed values
export const widgetArray = derived(widgets, $widgets => Object.values($widgets));

export const selectedWidgets = derived(
  [widgets, selectedWidgetConfigs],
  ([$widgets, $selectedWidgetConfigs]) => 
    Object.keys($selectedWidgetConfigs)
      .map(id => $widgets[id])
      .filter((widget): widget is Widget => widget !== undefined)
);

// Utility functions
export function getWidgetById(id: string): Widget | undefined {
  let result: Widget | undefined;
  widgets.subscribe(state => {
    result = state[id];
  })();
  return result;
}

export function getWidgetsByGroup(groupId: string): Widget[] {
  let result: Widget[] = [];
  widgets.subscribe(state => {
    result = Object.values(state).filter(widget => widget.groupId === groupId);
  })();
  return result;
}

export function getWidgetGroupById(id: string): WidgetGroup | undefined {
  let result: WidgetGroup | undefined;
  widgetGroups.subscribe(state => {
    result = state[id];
  })();
  return result;
}

// Import/Export functions
export function exportWidgets(): WidgetState {
  let result: WidgetState = {};
  widgets.subscribe(state => {
    result = { ...state };
  })();
  return result;
}

export function exportWidgetGroups(): WidgetGroupState {
  let result: WidgetGroupState = {};
  widgetGroups.subscribe(state => {
    result = { ...state };
  })();
  return result;
}

export function importWidgets(data: WidgetState) {
  widgets.set({ ...data });
}

export function importWidgetGroups(data: WidgetGroupState) {
  widgetGroups.set({ ...data });
}

// Widget utilities
export const widgetUtils: WidgetUtils = {
  // Group management
  createGroupFromSelection(name: string): WidgetGroup {
    let selectedIds: string[] = [];
    selectedWidgetConfigs.subscribe(state => {
      selectedIds = Object.keys(state);
    })();
    
    const group: WidgetGroup = {
      id: crypto.randomUUID(),
      name,
      widgets: selectedIds,
      layout: {
        x: 0,
        y: 0,
        width: 0,
        height: 0
      }
    };
    
    addWidgetGroup(group);
    return group;
  },

  // Layout management
  updateGroupLayout(groupId: string, x: number, y: number, width: number, height: number): void {
    updateWidgetGroup(groupId, {
      layout: { x, y, width, height }
    });
  },

  // Widget organization
  moveWidgetToGroup(widgetId: string, groupId: string): void {
    updateWidget(widgetId, { groupId });
  },

  // Group operations
  removeWidgetFromGroup(widgetId: string): void {
    updateWidget(widgetId, { groupId: undefined });
  },

  deleteGroup(groupId: string): void {
    widgetGroups.update(state => {
      const group = state[groupId];
      if (group) {
        group.widgets.forEach(widgetId => {
          updateWidget(widgetId, { groupId: undefined });
        });
      }
      delete state[groupId];
      return state;
    });
  },

  // Widget operations
  updateWidget(widgetId: string, updates: Partial<WidgetConfig>): void {
    updateWidget(widgetId, updates);
  },

  removeWidget(id: string): void {
    removeWidget(id);
  },

  lockWidgets(widgetIds: string[]): void {
    widgetIds.forEach(id => {
      updateWidget(id, { is_locked: true });
    });
  },

  unlockWidgets(widgetIds: string[]): void {
    widgetIds.forEach(id => {
      updateWidget(id, { is_locked: false });
    });
  },

  // Utility functions
  hasGroup(id: string): boolean {
    let result = false;
    widgetGroups.subscribe(state => {
      result = id in state;
    })();
    return result;
  }
};
