/**
 * Advanced theme management for Ultimate Sensor Monitor
 * Default: Dark theme with contemporary aesthetic
 * Supports multiple color schemes, visual effects, and dynamic theming
 */

import { writable, derived } from "svelte/store";
import type { ColorScheme, ThemePreset } from "$lib/types/common";
// import { storage } from "$lib/utils/storage"; // TODO: Create storage utility

// Define built-in color schemes with dark theme as primary
export const colorSchemes: Record<string, ColorScheme> = {
  dark_default: {
    id: "dark_default",
    name: "Dark Default",
    isDark: true,
    colors: {
      primary: "#00d4ff",
      secondary: "#0099cc",
      accent: "#ff6b35",
      background: "#010204",
      surface: "#0a0f14",
      surface_elevated: "#141b22",
      border: "#1e2832",
      border_subtle: "#0f1419",
      text: "#ffffff",
      text_muted: "#8892a0",
      text_subtle: "#5c6670",
      success: "#00ff88",
      warning: "#ffaa00",
      error: "#ff4757",
      info: "#00d4ff",
    },
  },
  gamer_neon: {
    id: "gamer_neon",
    name: "Gamer Neon",
    isDark: true,
    colors: {
      primary: "#00ff41",
      secondary: "#ff0080",
      accent: "#ffff00",
      background: "#000000",
      surface: "#0a0a0a",
      surface_elevated: "#1a1a1a",
      border: "#333333",
      border_subtle: "#1a1a1a",
      text: "#ffffff",
      text_muted: "#a0a0a0",
      text_subtle: "#666666",
      success: "#00ff41",
      warning: "#ffff00",
      error: "#ff0080",
      info: "#00ffff",
    },
  },
  cyberpunk_matrix: {
    id: "cyberpunk_matrix",
    name: "Cyberpunk Matrix",
    isDark: true,
    colors: {
      primary: "#ff0080",
      secondary: "#00ffff",
      accent: "#ffff00",
      background: "#0f0f23",
      surface: "#1a1a2e",
      surface_elevated: "#16213e",
      border: "#2d3748",
      border_subtle: "#1a202c",
      text: "#ffffff",
      text_muted: "#c7c7c7",
      text_subtle: "#9ca3af",
      success: "#00ff88",
      warning: "#ffaa00",
      error: "#ff4757",
      info: "#00ffff",
    },
  },
  professional_dark: {
    id: "professional_dark",
    name: "Professional Dark",
    isDark: true,
    colors: {
      primary: "#4a90e2",
      secondary: "#2c3e50",
      accent: "#e74c3c",
      background: "#1a1a1a",
      surface: "#2d2d2d",
      surface_elevated: "#3d3d3d",
      border: "#4d4d4d",
      border_subtle: "#2d2d2d",
      text: "#ffffff",
      text_muted: "#b3b3b3",
      text_subtle: "#808080",
      success: "#2ecc71",
      warning: "#f1c40f",
      error: "#e74c3c",
      info: "#3498db",
    },
  },
  synthwave_retro: {
    id: "synthwave_retro",
    name: "Synthwave Retro",
    isDark: true,
    colors: {
      primary: "#ff006e",
      secondary: "#8338ec",
      accent: "#ffbe0b",
      background: "#0d1b2a",
      surface: "#1e1b3b",
      surface_elevated: "#2d2a4a",
      border: "#415a77",
      border_subtle: "#2d3748",
      text: "#ffffff",
      text_muted: "#a8dadc",
      text_subtle: "#718096",
      success: "#06ffa5",
      warning: "#ffbe0b",
      error: "#ff006e",
      info: "#8338ec",
    },
  },
  light_minimal: {
    id: "light_minimal",
    name: "Light Minimal",
    isDark: false,
    colors: {
      primary: "#2563eb",
      secondary: "#4f46e5",
      accent: "#7c3aed",
      background: "#ffffff",
      surface: "#f8fafc",
      surface_elevated: "#f1f5f9",
      border: "#e2e8f0",
      border_subtle: "#f1f5f9",
      text: "#0f172a",
      text_muted: "#475569",
      text_subtle: "#64748b",
      success: "#059669",
      warning: "#d97706",
      error: "#dc2626",
      info: "#2563eb",
    },
  },
};

// Define built-in theme presets with dark as default
export const themePresets: Record<string, ThemePreset> = {
  dark_default: {
    id: "dark_default",
    name: "Dark Default",
    description: "Contemporary dark theme with precise aesthetics",
    category: "professional",
    visualSettings: {
      materiality: 0.6,
      information_density: 0.6,
      animation_level: 0.5,
      enable_blur_effects: true,
      enable_animations: true,
      enable_shadows: true,
      border_radius: "medium",
      font_weight: "normal",
    },
    colorScheme: colorSchemes.dark_default!,
  },
  gamer_immersive: {
    id: "gamer_immersive",
    name: "Gamer Immersive",
    description: "High-energy neon theme for gaming setups",
    category: "gamer",
    visualSettings: {
      materiality: 0.8,
      information_density: 0.7,
      animation_level: 0.9,
      enable_blur_effects: true,
      enable_animations: true,
      enable_shadows: true,
      border_radius: "large",
      font_weight: "medium",
    },
    colorScheme: colorSchemes.gamer_neon!,
  },
  cyberpunk_matrix: {
    id: "cyberpunk_matrix",
    name: "Cyberpunk Matrix",
    description: "Futuristic cyberpunk aesthetic with matrix vibes",
    category: "gamer",
    visualSettings: {
      materiality: 0.9,
      information_density: 0.8,
      animation_level: 0.8,
      enable_blur_effects: true,
      enable_animations: true,
      enable_shadows: true,
      border_radius: "small",
      font_weight: "bold",
    },
    colorScheme: colorSchemes.cyberpunk_matrix!,
  },
  professional_dark: {
    id: "professional_dark",
    name: "Professional Dark",
    description: "Sophisticated dark theme for professional environments",
    category: "professional",
    visualSettings: {
      materiality: 0.4,
      information_density: 0.5,
      animation_level: 0.3,
      enable_blur_effects: false,
      enable_animations: true,
      enable_shadows: false,
      border_radius: "small",
      font_weight: "normal",
    },
    colorScheme: colorSchemes.professional_dark!,
  },
  synthwave_retro: {
    id: "synthwave_retro",
    name: "Synthwave Retro",
    description: "Retro theme with synthwave vibes",
    category: "fui",
    visualSettings: {
      materiality: 0.7,
      information_density: 0.6,
      animation_level: 0.7,
      enable_blur_effects: true,
      enable_animations: true,
      enable_shadows: true,
      border_radius: "medium",
      font_weight: "medium",
    },
    colorScheme: colorSchemes.synthwave_retro!,
  },
  light_minimal: {
    id: "light_minimal",
    name: "Light Minimal",
    description: "Minimalistic light theme",
    category: "professional",
    visualSettings: {
      materiality: 0.2,
      information_density: 0.4,
      animation_level: 0.2,
      enable_blur_effects: false,
      enable_animations: false,
      enable_shadows: false,
      border_radius: "medium",
      font_weight: "normal",
    },
    colorScheme: colorSchemes.professional_dark!,
  },
};

// Theme store with dark as default
// TODO: Implement proper storage utility
const savedTheme =
  typeof window !== "undefined"
    ? localStorage.getItem("ultimon-current-theme")
    : null;
export const currentTheme = writable<string>(savedTheme || "dark_default");
export const customColorScheme = writable<ColorScheme | null>(null);

// Derived stores
export const activeColorScheme = derived(
  [currentTheme, customColorScheme],
  ([$currentTheme, $customColorScheme]) => {
    if ($customColorScheme) {
      return $customColorScheme;
    }
    return colorSchemes[$currentTheme] || colorSchemes.dark_default;
  },
);

export const activeThemePreset = derived(
  [currentTheme, customColorScheme],
  ([$currentTheme, $customColorScheme]) => {
    if ($customColorScheme) {
      return {
        ...themePresets.dark_default,
        colorScheme: $customColorScheme,
      };
    }
    return themePresets[$currentTheme] || themePresets.dark_default;
  },
);

// Theme utility functions
export const themeUtils = {
  // Apply theme to CSS custom properties
  applyTheme: (scheme: ColorScheme) => {
    if (typeof document === "undefined") return;

    const root = document.documentElement;

    Object.entries(scheme.colors).forEach(([key, value]) => {
      root.style.setProperty(`--theme-${key.replace("_", "-")}`, value);
    });
  },

  // Get all available themes
  getAvailableThemes: () => {
    return Object.values(themePresets);
  },

  // Get all available color schemes
  getAvailableColorSchemes: () => {
    return Object.values(colorSchemes);
  },

  // Create custom color scheme
  createCustomColorScheme: (
    name: string,
    colors: ColorScheme["colors"],
  ): ColorScheme => {
    return {
      id: `custom_${Date.now()}`,
      name,
      isDark: true, // Default to dark for custom themes
      colors,
    };
  },

  // Generate theme variations
  generateThemeVariation: (
    baseScheme: ColorScheme,
    adjustment: "darker" | "lighter" | "saturated" | "desaturated",
  ): ColorScheme => {
    const adjustColor = (hex: string): string => {
      const num = Number.parseInt(hex.replace("#", ""), 16);
      let r = (num >> 16) & 255;
      let g = (num >> 8) & 255;
      let b = num & 255;

      switch (adjustment) {
        case "darker":
          r = Math.max(0, r - 20);
          g = Math.max(0, g - 20);
          b = Math.max(0, b - 20);
          break;
        case "lighter":
          r = Math.min(255, r + 20);
          g = Math.min(255, g + 20);
          b = Math.min(255, b + 20);
          break;
        case "saturated": {
          const avg = (r + g + b) / 3;
          r = Math.min(255, r + (r - avg) * 0.2);
          g = Math.min(255, g + (g - avg) * 0.2);
          b = Math.min(255, b + (b - avg) * 0.2);
          break;
        }
        case "desaturated": {
          const average = (r + g + b) / 3;
          r = r + (average - r) * 0.3;
          g = g + (average - g) * 0.3;
          b = b + (average - b) * 0.3;
          break;
        }
      }

      return `#${Math.round(r).toString(16).padStart(2, "0")}${Math.round(g).toString(16).padStart(2, "0")}${Math.round(b).toString(16).padStart(2, "0")}`;
    };

    const adjustedColors = Object.fromEntries(
      Object.entries(baseScheme.colors).map(([key, color]) => [
        key,
        adjustColor(color),
      ]),
    ) as ColorScheme["colors"];

    return {
      id: `${baseScheme.id}_${adjustment}`,
      name: `${baseScheme.name} (${adjustment})`,
      isDark: baseScheme.isDark,
      colors: adjustedColors,
    };
  },

  // Export theme configuration
  exportTheme: (themeId: string) => {
    const preset = themePresets[themeId];
    if (!preset) return null;

    return {
      name: preset.name,
      description: preset.description,
      colorScheme: preset.colorScheme,
      visualSettings: preset.visualSettings,
      exported_at: new Date().toISOString(),
      version: "1.0",
    };
  },

  // Import theme configuration
  importTheme: (themeData: any): ThemePreset | null => {
    try {
      const imported: ThemePreset = {
        id: `imported_${Date.now()}`,
        name: themeData.name || "Imported Theme",
        description: themeData.description || "Imported theme configuration",
        category: themeData.category || 'professional',
        colorScheme: themeData.colorScheme || themeData.color_scheme,
        visualSettings: themeData.visualSettings || themeData.visual_settings,
      };

      return imported;
    } catch (error) {
      console.error("Failed to import theme:", error);
      return null;
    }
  },
};

// Auto-apply theme when it changes
if (typeof window !== "undefined") {
  activeColorScheme.subscribe((scheme) => {
    if (scheme) {
      themeUtils.applyTheme(scheme);
    }
  });

  // Load saved theme from localStorage, default to dark
  const savedTheme = localStorage.getItem("ultimon-current-theme");
  if (savedTheme && themePresets[savedTheme]) {
    currentTheme.set(savedTheme);
  } else {
    currentTheme.set("dark_default");
  }

  // Save theme changes
  currentTheme.subscribe((theme) => {
    localStorage.setItem("ultimon-current-theme", theme);
  });
}
