import type { Writable, Readable } from 'svelte/store';
import type { 
  SensorData, 
  SensorInfo, 
  SensorSourceFromAPI, 
  SensorSource,
  WidgetConfig,
  WidgetGroup,
  VisualSettings,
  EditMode,
  Selection,
  DragState,
  ContextMenuState,
  DashboardLayout,
  DashboardPreset,
  SystemEvent,
  WebSocketMessage,
  ApiResponse
} from './index';

// Core UI State
export interface UIState {
  editMode: Writable<EditMode>;
  selectedWidgets: Writable<Selection>;
  contextMenu: Writable<ContextMenuState>;
  dragState: Writable<DragState>;
  showLeftSidebar: Writable<boolean>;
  showRightSidebar: Writable<boolean>;
  hasSelection: Readable<boolean>;
  selectedWidgetCount: Readable<number>;
  isDragging: Readable<boolean>;
  isResizing: Readable<boolean>;
  isSelecting: Readable<boolean>;
}

// Sensor State
export interface SensorState {
  sensorData: Writable<Record<string, SensorData>>;
  sensorSources: Writable<SensorSource[]>;
  availableSensors: Writable<SensorInfo[]>;
  hardwareTree: Writable<Record<string, unknown>[]>;
  activeSensors: Readable<SensorData[]>;
  sensorCategories: Readable<string[]>;
  sensorStatus: Readable<Record<string, string>>;
  lastUpdate: Readable<string>;
  connectionStatus: Readable<'connected' | 'disconnected' | 'connecting' | 'error'>;
}

// Visual Settings State
export interface VisualState {
  visualSettings: Writable<VisualSettings>;
  currentTheme: Readable<string>;
  isDarkMode: Readable<boolean>;
  colorScheme: Readable<Record<string, string>>;
}

// Widget Data State
export interface WidgetState {
  widgets: Writable<Record<string, WidgetConfig>>;
  widgetGroups: Writable<Record<string, WidgetGroup>>;
  widgetArray: Readable<WidgetConfig[]>;
  selectedWidgetConfigs: Readable<WidgetConfig[]>;
  widgetOrder: Writable<string[]>;
  widgetVisibility: Writable<Record<string, boolean>>;
  widgetLockState: Writable<Record<string, boolean>>;
}

// Dashboard State
export interface DashboardState {
  layout: Writable<DashboardLayout>;
  presets: Writable<DashboardPreset[]>;
  currentPreset: Writable<string | null>;
  isEditing: Readable<boolean>;
  isFullscreen: Readable<boolean>;
  zoomLevel: Writable<number>;
}

// System State
export interface SystemState {
  events: Writable<SystemEvent[]>;
  notifications: Writable<WebSocketMessage[]>;
  errors: Writable<Error[]>;
  warnings: Writable<string[]>;
  isInitialized: Readable<boolean>;
  isDemoMode: Readable<boolean>;
}

// Store Utilities
export interface StoreUtils {
  // Widget management
  addWidget: (widget: WidgetConfig) => void;
  removeWidget: (id: string) => void;
  updateWidget: (id: string, updates: Partial<WidgetConfig>) => void;
  clearAllWidgets: () => void;
  moveWidget: (id: string, x: number, y: number) => void;
  resizeWidget: (id: string, width: number, height: number) => void;
  lockWidget: (id: string) => void;
  unlockWidget: (id: string) => void;
  showWidget: (id: string) => void;
  hideWidget: (id: string) => void;
  
  // Group management
  createGroup: (name: string, widgetIds: string[]) => void;
  deleteGroup: (id: string) => void;
  addToGroup: (groupId: string, widgetId: string) => void;
  removeFromGroup: (widgetId: string) => void;
  updateGroupLayout: (groupId: string, x: number, y: number, width: number, height: number) => void;
  
  // UI management
  clearSelection: () => void;
  hideContextMenu: () => void;
  toggleEditMode: () => void;
  toggleFullscreen: () => void;
  setZoomLevel: (level: number) => void;
  
  // Visual settings management
  updateVisualSettings: (settings: Partial<VisualSettings>) => void;
  toggleDarkMode: () => void;
  setColorScheme: (scheme: string) => void;
  
  // Sensor data management
  updateSensorData: (data: Record<string, SensorData>) => void;
  updateSensorSources: (apiPayload: Record<string, SensorSourceFromAPI> | null | undefined) => void;
  updateHardwareTree: (tree: Record<string, unknown>[] | unknown) => void;
  clearSensorData: () => void;
  
  // Dashboard management
  savePreset: (name: string, description?: string) => void;
  loadPreset: (id: string) => void;
  deletePreset: (id: string) => void;
  resetLayout: () => void;
  
  // System management
  addSystemEvent: (event: SystemEvent) => void;
  clearSystemEvents: () => void;
  setDemoMode: (enabled: boolean) => void;
  initialize: () => Promise<void>;
}

// Store initialization
export interface StoreInitialization {
  initializeStores: () => Promise<void>;
  resetStores: () => void;
  loadStoresFromStorage: () => Promise<void>;
  saveStoresToStorage: () => Promise<void>;
}

// Store types
export type Store = {
  ui: UIState;
  sensors: SensorState;
  visual: VisualState;
  widgets: WidgetState;
  dashboard: DashboardState;
  system: SystemState;
  utils: StoreUtils;
  init: StoreInitialization;
}; 