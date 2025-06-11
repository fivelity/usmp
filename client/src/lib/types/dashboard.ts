/**
 * Type definitions for dashboard layout and configuration.
 */

export interface BackgroundSettings {
  color?: string;
  image?: string;
  gradient?: [string, string];
}

export interface GridSettings {
  visible: boolean;
  snap: boolean;
  color: string;
  size: number;
}

export interface DashboardLayout {
  canvas_width: number;
  canvas_height: number;
  background_type: "solid" | "image" | "gradient";
  background_settings: BackgroundSettings;
  grid_settings: GridSettings;
}
