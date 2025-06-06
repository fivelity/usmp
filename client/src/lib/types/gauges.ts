// Gauge-related type definitions

export interface GaugeSettings {
  // Common settings
  min_value?: number;
  max_value?: number;
  unit?: string;
  format?: string;
  decimals?: number;
  show_value?: boolean;
  show_min_max?: boolean;
  show_unit?: boolean;
  color_scheme?: string;
  animation_duration?: number;
  update_interval?: number;
  custom_styles?: Record<string, string>;
  metadata?: Record<string, unknown>;

  // Radial gauge specific
  start_angle?: number;
  end_angle?: number;
  stroke_width?: number;
  color_primary?: string;
  color_secondary?: string;
  show_glow?: boolean;

  // Linear gauge specific
  orientation?: 'horizontal' | 'vertical';
  show_scale?: boolean;
  show_gradient?: boolean;
  bar_height?: number;

  // Graph gauge specific
  time_range?: number;
  line_color?: string;
  fill_area?: boolean;
  show_points?: boolean;
  show_grid?: boolean;
  animate_entry?: boolean;

  // Glassmorphic gauge specific
  style?: 'radial' | 'linear' | 'ring';
  glow_intensity?: number;

  // Image sequence specific
  frames?: string[];
  frameRate?: number;
  loop?: boolean;
  preloadFrames?: number;
  quality?: 'high' | 'low';
  interpolation?: 'linear' | 'nearest';
  showDebug?: boolean;
}

export interface SystemMetric {
  id: string;
  sensor_id: string;
  label: string;
  icon?: string;
  unit?: string;
  min_value?: number;
  max_value?: number;
  warning_threshold?: number;
  critical_threshold?: number;
  format?: "number" | "percentage" | "temperature" | "frequency" | "bytes";
}

export interface SystemStatusConfig extends GaugeSettings {
  // Layout options
  layout: "compact" | "detailed" | "minimal";
  columns: number;

  // Metric selection
  metrics: SystemMetric[];

  // Visual options
  show_icons: boolean;
  show_labels: boolean;
  show_values: boolean;
  show_units: boolean;

  // Color coding
  use_status_colors: boolean;
  warning_threshold: number;
  critical_threshold: number;

  // Animation
  animate_changes: boolean;
  update_animation: "fade" | "slide" | "pulse" | "none";
} 