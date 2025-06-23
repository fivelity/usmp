/**
 * Common type definitions used throughout the application
 */

// Base component props interface
export interface BaseComponentProps {
  class?: string;
  id?: string;
  style?: string;
}

// Color scheme definitions
export interface ColorScheme {
  id: string;
  name: string;
  description?: string;
  colors: Record<string, string>;
  isDark: boolean;
}

// Theme preset definitions
export interface ThemePreset {
  id: string;
  name: string;
  description?: string;
  category: string;
  colorScheme: ColorScheme;
  visualSettings: Partial<VisualSettings>;
}

// Visual settings interface
export interface VisualSettings {
  // Core visual dimensions (0-1 range)
  materiality: number;
  information_density: number;
  animation_level: number;

  // Color scheme
  color_scheme: string;
  colorScheme?: string; // Alternative property name
  custom_colors: Record<string, string>;

  // Typography
  font_family: string;
  font_scale: number;
  fontSize?: "small" | "medium" | "large";

  // Effects
  enable_blur_effects: boolean;
  enable_animations: boolean;
  enable_shadows?: boolean;
  enable_gradients?: boolean;
  reduce_motion: boolean;

  // Grid and layout
  grid_size: number;
  snap_to_grid: boolean;
  show_grid: boolean;
  border_radius?: number;

  // Accessibility
  highContrast?: boolean;
  spacing?: "small" | "medium" | "large";

  // Theme colors
  theme?: "light" | "dark";
  background: string;
  accent?: string;
  text?: string;
  border?: string;
  primary?: string;
  secondary?: string;
  success?: string;
  warning?: string;
  error?: string;
  info?: string;
}

// Generic utility types
export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;
export type RequiredBy<T, K extends keyof T> = T & Required<Pick<T, K>>;

// Event handler types
export type EventHandler<T = Event> = (event: T) => void;
export type ChangeHandler<T = any> = (value: T) => void;

export interface Point {
  x: number;
  y: number;
}
