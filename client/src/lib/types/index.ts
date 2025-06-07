/**
 * Comprehensive type definitions for Ultimate Sensor Monitor
 * Centralized type system with proper documentation
 */

import type { WidgetConfig, ExtendedGaugeType } from "./widgets";

import type { GaugeSettings } from "./gauges";

// ============================================================================
// CORE DATA TYPES
// ============================================================================

export interface SensorData {
  id: string;
  name: string;
  category: string;
  unit: string;
  value: number;
  min_value?: number;
  max_value?: number;
  source: string;
  timestamp: string;
  status?: SensorStatus;
  metadata?: Record<string, unknown>;
}

export type SensorStatus = "normal" | "warning" | "critical" | "unknown";

export interface SensorSource {
  id: string;
  name: string;
  active: boolean;
  sensors: SensorData[];
  last_update: string;
  error_message?: string;
  metadata?: {
    type: string;
    version?: string;
    capabilities?: string[];
    [key: string]: unknown;
  };
}

export interface SensorInfo {
  id: string;
  name: string;
  category: string;
  unit: string;
  source: string;
  description?: string;
  metadata?: Record<string, unknown>;
}

export interface SensorSourceFromAPI {
  id: string;
  name: string;
  active: boolean;
  sensors: Record<string, SensorData>;
  last_update: string;
  error_message?: string;
  metadata?: Record<string, unknown>;
}

// ============================================================================
// WIDGET SYSTEM
// ============================================================================

export type GaugeType =
  | "text"
  | "radial"
  | "linear"
  | "graph"
  | "image"
  | "glassmorphic";

export type { WidgetConfig, ExtendedGaugeType } from "./widgets";

export type { GaugeSettings } from "./gauges";

export interface WidgetStyle {
  background_color?: string;
  border_color?: string;
  border_width?: number;
  border_radius?: number;
  padding?: number;
  margin?: number;
  opacity?: number;
  shadow?: string;
  font_family?: string;
  font_size?: number;
  font_weight?: number;
  text_color?: string;
  [key: string]: unknown;
}

export interface StyleSettings {
  background_color?: string;
  border_color?: string;
  border_width?: number;
  border_radius?: number;
  shadow?: string;
  opacity?: number;
  font_family?: string;
  font_size?: number;
  font_weight?: number;
  text_color?: string;
  [key: string]: unknown;
}

export interface WidgetGroup {
  id: string;
  name: string;
  widgets: string[];
  layout: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
  style?: WidgetStyle;
  metadata?: Record<string, unknown>;
}

// ============================================================================
// UI STATE MANAGEMENT
// ============================================================================

export type EditMode = "view" | "edit";

export interface Point {
  x: number;
  y: number;
}

export interface Size {
  width: number;
  height: number;
}

export interface Bounds extends Point, Size {}

export interface Selection {
  type: "widget" | "group";
  ids: string[];
  bounds?: Bounds;
}

export interface DragState {
  isDragging: boolean;
  startX: number;
  startY: number;
  currentX: number;
  currentY: number;
  widgetId?: string;
  groupId?: string;
}

export interface ResizeState {
  isResizing: boolean;
  handle: ResizeHandle;
  startPos: Point;
  startSize: Size;
  widgetId: string;
}

export type ResizeHandle = "nw" | "n" | "ne" | "e" | "se" | "s" | "sw" | "w";

export interface ContextMenuState {
  show: boolean;
  x: number;
  y: number;
  items: ContextMenuItem[];
  target?: {
    type: "widget" | "group" | "canvas";
    id?: string;
  };
}

export interface ContextMenuItem {
  id: string;
  label: string;
  icon?: string;
  action: () => void;
  disabled?: boolean;
  separator?: boolean;
  submenu?: ContextMenuItem[];
  shortcut?: string;
  category?: string;
}

// ============================================================================
// VISUAL SYSTEM
// ============================================================================

export interface VisualSettings {
  // Core visual dimensions
  materiality: number;
  information_density: number;
  animation_level: number;

  // Color scheme
  color_scheme: string;
  custom_colors: Record<string, string>;

  // Typography
  font_family: string;
  font_scale: number;

  // Effects
  enable_blur_effects: boolean;
  enable_animations: boolean;
  reduce_motion: boolean;

  // Grid and layout
  grid_size: number;
  snap_to_grid: boolean;
  show_grid: boolean;

  // Advanced visual features
  enable_shadows: boolean;
  enable_gradients: boolean;
  border_radius: "small" | "medium" | "large";
  font_weight: "normal" | "medium" | "bold";

  // Accessibility & Layout
  highContrast: boolean;
  fontSize: "small" | "medium" | "large";
  spacing: "small" | "medium" | "large";

  // Theme
  theme: "light" | "dark";
  background: string;
  accent: string;
  text: string;
  border: string;
  primary: string;
  secondary: string;
  success: string;
  warning: string;
  error: string;
  info: string;

  // Metadata
  metadata?: Record<string, unknown>;
}

export interface ColorScheme {
  id: string;
  name: string;
  description?: string;
  colors: {
    primary: string;
    secondary: string;
    accent: string;
    background: string;
    surface: string;
    surface_elevated: string;
    border: string;
    border_subtle: string;
    text: string;
    text_muted: string;
    text_subtle: string;
    success: string;
    warning: string;
    error: string;
    info: string;
    [key: string]: string;
  };
  metadata?: Record<string, unknown>;
}

export interface ThemePreset {
  id: string;
  name: string;
  description: string;
  visual_settings: Partial<VisualSettings>;
  color_scheme: ColorScheme;
  preview_image?: string;
  metadata?: Record<string, unknown>;
}

// ============================================================================
// DASHBOARD SYSTEM
// ============================================================================

export interface DashboardLayout {
  canvas_width: number;
  canvas_height: number;
  background_type: "solid" | "gradient" | "image" | "pattern";
  background_settings: Record<string, unknown>;
  grid_settings: {
    visible: boolean;
    snap: boolean;
    color: string;
    size: number;
  };
  metadata?: Record<string, unknown>;
}

export interface DashboardPreset {
  id?: string;
  name: string;
  description?: string;
  widgets: WidgetConfig[];
  widget_groups: WidgetGroup[];
  layout: DashboardLayout;
  visual_settings: VisualSettings;
  created_at?: string;
  updated_at?: string;
  version: string;
  author?: string;
  tags?: string[];
  preview_image?: string;
  metadata?: Record<string, unknown>;
}

// ============================================================================
// COMMUNICATION
// ============================================================================

export interface WebSocketMessage {
  type: string;
  timestamp: string;
  data?: unknown;
  content?: unknown;
  message?: string;
  id?: string;
  metadata?: Record<string, unknown>;
}

export interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
  timestamp?: string;
  metadata?: Record<string, unknown>;
}

// ============================================================================
// EVENTS
// ============================================================================

export interface WidgetEvent {
  type:
    | "select"
    | "deselect"
    | "move"
    | "resize"
    | "lock"
    | "unlock"
    | "delete"
    | "duplicate";
  widget_id: string;
  data?: unknown;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export interface GroupEvent {
  type: "create" | "update" | "delete" | "select" | "move";
  group_id: string;
  data?: unknown;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export interface SystemEvent {
  type: "error" | "warning" | "info" | "success";
  message: string;
  details?: unknown;
  timestamp: string;
  id: string;
  metadata?: Record<string, unknown>;
}

// ============================================================================
// CONFIGURATION
// ============================================================================

export interface AppConfig {
  data: {
    useDemoData: boolean;
    autoCreateWidgets: boolean;
    maxWidgetsPerCategory: number;
    dataRetentionDays: number;
  };
  ui: {
    defaultEditMode: EditMode;
    showSplash: boolean;
    autoOpenLeftSidebar: boolean;
    autoOpenRightSidebar: boolean;
    enableTooltips: boolean;
    enableAnimations: boolean;
  };
  performance: {
    widgetUpdateThrottle: number;
    maxGraphPoints: number;
    enableHardwareAcceleration: boolean;
    maxConcurrentWidgets: number;
  };
  debug: {
    debugMode: boolean;
    showPerformanceMetrics: boolean;
    logSensorUpdates: boolean;
    enableDevTools: boolean;
  };
  canvas: {
    defaultCanvasWidth: number;
    defaultCanvasHeight: number;
    defaultGridSize: number;
    defaultSnapToGrid: boolean;
    defaultShowGrid: boolean;
    maxCanvasSize: number;
  };
  sensors: {
    connectionTimeout: number;
    maxRetryAttempts: number;
    updateInterval: number;
    enableAutoDiscovery: boolean;
  };
  widgets: {
    defaultWidgetWidth: number;
    defaultWidgetHeight: number;
    minWidgetWidth: number;
    minWidgetHeight: number;
    maxWidgetWidth: number;
    maxWidgetHeight: number;
    widgetSpacing: number;
    widgetRowHeight: number;
    widgetsPerRow: number;
  };
  metadata?: Record<string, unknown>;
}

// ============================================================================
// UTILITY TYPES
// ============================================================================

export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

export type RequiredFields<T, K extends keyof T> = T & Required<Pick<T, K>>;

export type OptionalFields<T, K extends keyof T> = Omit<T, K> &
  Partial<Pick<T, K>>;

// ============================================================================
// COMPONENT PROPS
// ============================================================================

export interface BaseComponentProps {
  class?: string;
  style?: string;
  id?: string;
  "data-testid"?: string;
  "aria-label"?: string;
  "aria-describedby"?: string;
  "aria-hidden"?: boolean;
  role?: string;
  tabindex?: number;
}

export interface InteractiveComponentProps extends BaseComponentProps {
  disabled?: boolean;
  loading?: boolean;
  onClick?: (event: MouseEvent) => void;
  onKeyDown?: (event: KeyboardEvent) => void;
  onFocus?: (event: FocusEvent) => void;
  onBlur?: (event: FocusEvent) => void;
  children?: () => unknown;
}

export interface FormComponentProps extends InteractiveComponentProps {
  name?: string;
  required?: boolean;
  error?: string;
  helperText?: string;
  label?: string;
  placeholder?: string;
  value?: unknown;
  onChange?: (event: Event) => void;
  onInput?: (event: Event) => void;
}

// ============================================================================
// COMPONENT PROPS
// ============================================================================

export interface Widget {
  id: string;
  type: ExtendedGaugeType;
  name: string;
  x: number;
  y: number;
  width: number;
  height: number;
  groupId?: string;
  config: GaugeSettings;
  style?: WidgetStyle;
  metadata?: Record<string, unknown>;
  is_locked?: boolean;
}

export interface WidgetUtils {
  createGroupFromSelection(name: string): WidgetGroup;
  updateGroupLayout(
    groupId: string,
    x: number,
    y: number,
    width: number,
    height: number,
  ): void;
  moveWidgetToGroup(widgetId: string, groupId: string): void;
  removeWidgetFromGroup(widgetId: string): void;
  deleteGroup(groupId: string): void;
  updateWidget(widgetId: string, updates: Partial<WidgetConfig>): void;
  lockWidgets(widgetIds: string[]): void;
  unlockWidgets(widgetIds: string[]): void;
  hasGroup(id: string): boolean;
  removeWidget(id: string): void;
}
