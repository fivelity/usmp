// Theme-related type definitions

export interface ColorScheme {
  id: string;
  name: string;
  isDark: boolean;
  colors: {
    // Primary Colors
    primary: string;
    secondary: string;
    accent: string;
    
    // Background Colors
    background: string;
    surface: string;
    surface_elevated: string;
    
    // Border Colors
    border: string;
    border_subtle: string;
    
    // Text Colors
    text: string;
    text_muted: string;
    text_subtle: string;
    
    // Status Colors
    success: string;
    warning: string;
    error: string;
    info: string;
  };
}

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
  reduce_motion: boolean;
  enable_shadows?: boolean;
  enable_gradients?: boolean;

  // Layout
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

export interface ThemePreset {
  id: string;
  name: string;
  description: string;
  category: 'professional' | 'gamer' | 'fui';
  colorScheme: ColorScheme;
  visualSettings: {
    materiality: number;
    information_density: number;
    animation_level: number;
    enable_blur_effects: boolean;
    enable_animations: boolean;
    enable_shadows?: boolean;
    reduce_motion: boolean;
    border_radius?: string | number;
    font_weight?: string;
  };
}

export interface ThemeExport {
  name: string;
  description: string;
  colorScheme: ColorScheme;
  visualSettings: VisualSettings;
  exported_at: string;
}
