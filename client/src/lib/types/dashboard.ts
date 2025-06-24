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
  /** Legacy grid size tuple [width, height] */
  grid_size?: [number, number];
  /** Legacy flat background color (hex) */
  background_color?: string;
  /** Legacy flag to toggle grid visibility */
  show_grid?: boolean;
  /** Legacy grid color (hex) */
  grid_color?: string;
  /** Legacy background opacity (0-1) */
  background_opacity?: number;
  canvas_width: number;
  canvas_height: number;
  background_type: "solid" | "image" | "gradient";
  background_settings: BackgroundSettings;
  grid_settings: GridSettings;
}
