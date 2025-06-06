import { writable, derived } from "svelte/store"
import type { VisualSettings } from "$lib/types"

// Visual settings state management using Svelte 5 runes
export const visualSettings = $state<VisualSettings>({
  // Core visual dimensions
  materiality: 0.5,
  information_density: 0.5,
  animation_level: 0.5,
  
  // Color scheme
  color_scheme: "professional",
  custom_colors: {},
  
  // Typography
  font_family: "Inter, system-ui, sans-serif",
  font_scale: 1.0,
  
  // Effects
  enable_blur_effects: true,
  enable_animations: true,
  reduce_motion: false,
  
  // Grid and layout
  grid_size: 10,
  snap_to_grid: true,
  show_grid: false,
  
  // Advanced visual features
  enable_shadows: true,
  enable_gradients: true,
  border_radius: 8,

  // Theme
  theme: 'light',
  background: '#ffffff',
  accent: '#3b82f6',
  text: '#1f2937',
  border: '#e5e7eb',
  primary: '#3b82f6',
  secondary: '#6b7280',
  success: '#10b981',
  warning: '#f59e0b',
  error: '#ef4444',
  info: '#3b82f6',

  // Accessibility & Layout
  highContrast: false,
  fontSize: 'medium',
  spacing: 'medium'
})

// Derived state
export const isDarkMode = $derived(visualSettings.theme === 'dark')
export const isHighContrast = $derived(visualSettings.highContrast)
export const hasAnimations = $derived(visualSettings.enable_animations && !visualSettings.reduce_motion)

// Visual settings utilities
export const visualUtils = {
  toggleTheme() {
    visualSettings.theme = visualSettings.theme === 'light' ? 'dark' : 'light'
  },
  
  updateColorScheme(scheme: string) {
    visualSettings.color_scheme = scheme
  },
  
  toggleGrid() {
    visualSettings.show_grid = !visualSettings.show_grid
  },
  
  toggleSnapToGrid() {
    visualSettings.snap_to_grid = !visualSettings.snap_to_grid
  },
  
  updateGridSize(size: number) {
    visualSettings.grid_size = size
  },
  
  toggleAnimations() {
    visualSettings.enable_animations = !visualSettings.enable_animations
  },
  
  toggleBlurEffects() {
    visualSettings.enable_blur_effects = !visualSettings.enable_blur_effects
  },
  
  updateFontScale(scale: number) {
    visualSettings.font_scale = scale
  },
  
  updateBorderRadius(radius: number) {
    visualSettings.border_radius = radius
  },

  toggleReduceMotion() {
    visualSettings.reduce_motion = !visualSettings.reduce_motion
  },

  setFontFamily(family: string) {
    visualSettings.font_family = family
  },

  toggleHighContrast() {
    visualSettings.highContrast = !visualSettings.highContrast
  },

  setFontSize(size: 'small' | 'medium' | 'large') {
    visualSettings.fontSize = size
  },

  setSpacing(size: 'small' | 'medium' | 'large') {
    visualSettings.spacing = size
  },

  toggleShadows() {
    visualSettings.enable_shadows = !visualSettings.enable_shadows
  },
  
  toggleGradients() {
    visualSettings.enable_gradients = !visualSettings.enable_gradients
  },

  updateSettings(newSettings: Partial<VisualSettings>) {
    for (const key in newSettings) {
      if (Object.prototype.hasOwnProperty.call(visualSettings, key)) {
        // Type assertion to allow dynamic key assignment while ensuring key exists
        (visualSettings as any)[key] = (newSettings as any)[key];
      }
    }
  }
}

// Enhanced visual settings with grid system
export const visualSettingsOriginal = writable<VisualSettings>({
  // Core visual dimensions (0-1 range)
  materiality: 0.5,
  information_density: 0.5,
  animation_level: 0.5,

  // Color scheme
  color_scheme: "professional",
  custom_colors: {},

  // Typography
  font_family: "Inter, system-ui, sans-serif",
  font_scale: 1.0,

  // Effects
  enable_blur_effects: true,
  enable_animations: true,
  reduce_motion: false,

  // Enhanced grid and layout
  grid_size: 10,
  snap_to_grid: true,
  show_grid: false,

  // Advanced visual features
  enable_shadows: true,
  enable_gradients: true,
  border_radius: 8,

  // Accessibility & Layout
  highContrast: false,
  fontSize: 'medium',
  spacing: 'medium',

  // Theme
  theme: 'light',
  background: '#ffffff',
  accent: '#3b82f6',
  text: '#1f2937',
  border: '#e5e7eb',
  primary: '#3b82f6',
  secondary: '#6b7280',
  success: '#10b981',
  warning: '#f59e0b',
  error: '#ef4444',
  info: '#3b82f6'
})

// Grid utilities
export const gridUtils = {
  snapToGrid: (value: number, gridSize: number): number => {
    return Math.round(value / gridSize) * gridSize
  },

  snapPosition: (x: number, y: number, gridSize: number) => ({
    x: Math.round(x / gridSize) * gridSize,
    y: Math.round(y / gridSize) * gridSize,
  }),

  snapSize: (width: number, height: number, gridSize: number) => ({
    width: Math.max(gridSize, Math.round(width / gridSize) * gridSize),
    height: Math.max(gridSize, Math.round(height / gridSize) * gridSize),
  }),

  getGridLines: (canvasWidth: number, canvasHeight: number, gridSize: number) => {
    const verticalLines = []
    const horizontalLines = []

    for (let x = 0; x <= canvasWidth; x += gridSize) {
      verticalLines.push(x)
    }

    for (let y = 0; y <= canvasHeight; y += gridSize) {
      horizontalLines.push(y)
    }

    return { verticalLines, horizontalLines }
  },
}

// Derived stores for computed values
export const computedVisualSettings = derived([visualSettingsOriginal], ([$visualSettings]) => ({
  ...$visualSettings,
  // Computed CSS custom properties
  cssVars: {
    "--visual-materiality": $visualSettings.materiality,
    "--visual-density": $visualSettings.information_density,
    "--visual-animation": $visualSettings.animation_level,
    "--grid-size": `${$visualSettings.grid_size}px`,
    "--border-radius": `${$visualSettings.border_radius}px`,
    "--font-scale": $visualSettings.font_scale,
  },
}))

// Auto-apply visual settings to CSS
if (typeof window !== "undefined") {
  computedVisualSettings.subscribe((settings) => {
    const root = document.documentElement
    Object.entries(settings.cssVars).forEach(([property, value]) => {
      root.style.setProperty(property, String(value))
    })
  })
}
