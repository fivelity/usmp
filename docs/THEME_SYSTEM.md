# Theme System Documentation

## Overview

The Ultimate Sensor Monitor features a **sophisticated theme system** designed around a **dark-first approach** with the primary background color **#010204**. The system provides multiple carefully crafted themes that cater to different user preferences and use cases, from gaming enthusiasts to professional environments.

## Theme Architecture

### Core Theme Structure

\`\`\`typescript
interface ColorScheme {
  id: string;
  name: string;
  colors: {
    // Primary Colors
    primary: string;           // Main accent color
    secondary: string;         // Secondary accent
    accent: string;           // Highlight color
    
    // Background Colors
    background: string;        // Main background (#010204 for dark themes)
    surface: string;          // Widget/panel backgrounds
    surface_elevated: string; // Modal/dropdown backgrounds
    
    // Border Colors
    border: string;           // Primary borders
    border_subtle: string;    // Subtle dividers
    
    // Text Colors
    text: string;             // Primary text
    text_muted: string;       // Secondary text
    text_subtle: string;      // Tertiary text
    
    // Status Colors
    success: string;          // Success states
    warning: string;          // Warning states
    error: string;            // Error states
    info: string;             // Information states
  };
}

interface ThemePreset {
  id: string;
  name: string;
  description: string;
  visual_settings: {
    materiality: number;        // 0-1, glass/material effects
    information_density: number; // 0-1, UI density
    animation_level: number;    // 0-1, animation intensity
    enable_blur_effects: boolean;
    enable_animations: boolean;
    enable_shadows: boolean;
    border_radius: 'small' | 'medium' | 'large';
    font_weight: 'normal' | 'medium' | 'bold';
  };
  color_scheme: ColorScheme;
}
\`\`\`

## Available Themes

### 1. Dark Default (Primary Theme)

**Target Audience**: General users, contemporary aesthetic preference
**Background**: #010204 (Deep dark blue-black)

\`\`\`css
:root[data-theme="dark_default"] {
  --theme-primary: #00d4ff;        /* Bright cyan */
  --theme-secondary: #0099cc;      /* Darker cyan */
  --theme-accent: #ff6b35;         /* Orange accent */
  --theme-background: #010204;     /* Deep dark blue */
  --theme-surface: #0a0f14;        /* Slightly lighter surface */
  --theme-surface-elevated: #141b22; /* Elevated surfaces */
  --theme-border: #1e2832;         /* Subtle borders */
  --theme-border-subtle: #0f1419;  /* Very subtle borders */
  --theme-text: #ffffff;           /* Pure white text */
  --theme-text-muted: #8892a0;     /* Muted blue-gray */
  --theme-text-subtle: #5c6670;    /* Subtle gray */
  --theme-success: #00ff88;        /* Bright green */
  --theme-warning: #ffaa00;        /* Amber warning */
  --theme-error: #ff4757;          /* Red error */
  --theme-info: #00d4ff;           /* Cyan info */
}
\`\`\`

**Visual Settings**:
- Materiality: 60% (moderate glass effects)
- Information Density: 60% (balanced layout)
- Animation Level: 50% (subtle animations)
- Blur Effects: Enabled
- Shadows: Enabled
- Border Radius: Medium (8px)

### 2. Gamer Neon

**Target Audience**: Gaming enthusiasts, RGB setups
**Background**: #000000 (Pure black for maximum contrast)

\`\`\`css
:root[data-theme="gamer_neon"] {
  --theme-primary: #00ff41;        /* Matrix green */
  --theme-secondary: #ff0080;      /* Hot pink */
  --theme-accent: #ffff00;         /* Electric yellow */
  --theme-background: #000000;     /* Pure black */
  --theme-surface: #0a0a0a;        /* Dark surface */
  --theme-surface-elevated: #1a1a1a; /* Elevated dark */
  --theme-border: #333333;         /* Gray borders */
  --theme-border-subtle: #1a1a1a;  /* Subtle borders */
  --theme-text: #ffffff;           /* White text */
  --theme-text-muted: #a0a0a0;     /* Light gray */
  --theme-text-subtle: #666666;    /* Medium gray */
  --theme-success: #00ff41;        /* Neon green */
  --theme-warning: #ffff00;        /* Neon yellow */
  --theme-error: #ff0080;          /* Neon pink */
  --theme-info: #00ffff;           /* Cyan */
}
\`\`\`

**Visual Settings**:
- Materiality: 80% (strong glass effects)
- Information Density: 70% (dense information)
- Animation Level: 90% (high animation)
- Blur Effects: Enabled
- Shadows: Enabled with glow
- Border Radius: Large (12px)

### 3. Cyberpunk Matrix

**Target Audience**: Sci-fi enthusiasts, futuristic aesthetic
**Background**: #0f0f23 (Dark purple-blue)

\`\`\`css
:root[data-theme="cyberpunk_matrix"] {
  --theme-primary: #ff0080;        /* Hot pink */
  --theme-secondary: #00ffff;      /* Cyan */
  --theme-accent: #ffff00;         /* Yellow */
  --theme-background: #0f0f23;     /* Dark purple */
  --theme-surface: #1a1a2e;        /* Purple surface */
  --theme-surface-elevated: #16213e; /* Elevated purple */
  --theme-border: #2d3748;         /* Blue-gray border */
  --theme-border-subtle: #1a202c;  /* Subtle border */
  --theme-text: #ffffff;           /* White text */
  --theme-text-muted: #c7c7c7;     /* Light gray */
  --theme-text-subtle: #9ca3af;    /* Medium gray */
  --theme-success: #00ff88;        /* Matrix green */
  --theme-warning: #ffaa00;        /* Orange */
  --theme-error: #ff4757;          /* Red */
  --theme-info: #00ffff;           /* Cyan */
}
\`\`\`

**Visual Settings**:
- Materiality: 90% (maximum glass effects)
- Information Density: 80% (high density)
- Animation Level: 80% (strong animations)
- Blur Effects: Enabled
- Shadows: Enabled with colored glow
- Border Radius: Small (4px)

### 4. Professional Dark

**Target Audience**: Business users, professional environments
**Background**: #0f172a (Professional dark blue)

\`\`\`css
:root[data-theme="professional_dark"] {
  --theme-primary: #3b82f6;        /* Professional blue */
  --theme-secondary: #6366f1;      /* Indigo */
  --theme-accent: #8b5cf6;         /* Purple accent */
  --theme-background: #0f172a;     /* Professional dark */
  --theme-surface: #1e293b;        /* Slate surface */
  --theme-surface-elevated: #334155; /* Elevated slate */
  --theme-border: #475569;         /* Slate border */
  --theme-border-subtle: #334155;  /* Subtle border */
  --theme-text: #f8fafc;           /* Off-white text */
  --theme-text-muted: #cbd5e1;     /* Light slate */
  --theme-text-subtle: #94a3b8;    /* Medium slate */
  --theme-success: #10b981;        /* Professional green */
  --theme-warning: #f59e0b;        /* Amber */
  --theme-error: #ef4444;          /* Red */
  --theme-info: #3b82f6;           /* Blue */
}
\`\`\`

**Visual Settings**:
- Materiality: 40% (minimal effects)
- Information Density: 50% (balanced)
- Animation Level: 30% (subtle)
- Blur Effects: Disabled
- Shadows: Disabled
- Border Radius: Small (4px)

### 5. Synthwave Retro

**Target Audience**: Retro enthusiasts, 80s aesthetic lovers
**Background**: #0d1b2a (Deep retro blue)

\`\`\`css
:root[data-theme="synthwave_retro"] {
  --theme-primary: #ff006e;        /* Hot pink */
  --theme-secondary: #8338ec;      /* Purple */
  --theme-accent: #ffbe0b;         /* Golden yellow */
  --theme-background: #0d1b2a;     /* Deep blue */
  --theme-surface: #1e1b3b;        /* Purple surface */
  --theme-surface-elevated: #2d2a4a; /* Elevated purple */
  --theme-border: #415a77;         /* Blue-gray */
  --theme-border-subtle: #2d3748;  /* Subtle border */
  --theme-text: #ffffff;           /* White text */
  --theme-text-muted: #a8dadc;     /* Light blue */
  --theme-text-subtle: #718096;    /* Gray-blue */
  --theme-success: #06ffa5;        /* Neon green */
  --theme-warning: #ffbe0b;        /* Golden yellow */
  --theme-error: #ff006e;          /* Hot pink */
  --theme-info: #8338ec;           /* Purple */
}
\`\`\`

**Visual Settings**:
- Materiality: 70% (retro glass effects)
- Information Density: 60% (balanced)
- Animation Level: 70% (smooth animations)
- Blur Effects: Enabled
- Shadows: Enabled with glow
- Border Radius: Medium (8px)

### 6. Light Minimal (Alternative)

**Target Audience**: Users preferring light themes, bright environments
**Background**: #ffffff (Pure white)

\`\`\`css
:root[data-theme="light_minimal"] {
  --theme-primary: #2563eb;        /* Blue */
  --theme-secondary: #4f46e5;      /* Indigo */
  --theme-accent: #7c3aed;         /* Purple */
  --theme-background: #ffffff;     /* White */
  --theme-surface: #f8fafc;        /* Light gray */
  --theme-surface-elevated: #f1f5f9; /* Elevated light */
  --theme-border: #e2e8f0;         /* Light border */
  --theme-border-subtle: #f1f5f9;  /* Subtle border */
  --theme-text: #0f172a;           /* Dark text */
  --theme-text-muted: #475569;     /* Medium gray */
  --theme-text-subtle: #64748b;    /* Light gray */
  --theme-success: #059669;        /* Green */
  --theme-warning: #d97706;        /* Orange */
  --theme-error: #dc2626;          /* Red */
  --theme-info: #2563eb;           /* Blue */
}
\`\`\`

## Theme Selection Interface

### Theme Gallery Component

\`\`\`svelte
<!-- ThemeGallery.svelte -->
<script lang="ts">
  import { currentTheme, themePresets } from '$lib/stores/themes';
  import { createEventDispatcher } from 'svelte';
  
  const dispatch = createEventDispatcher();
  let selectedCategory = 'all';
  
  $: filteredThemes = Object.values(themePresets).filter(theme => {
    if (selectedCategory === 'all') return true;
    if (selectedCategory === 'dark') return theme.id.includes('dark') || theme.id.includes('gamer') || theme.id.includes('cyberpunk') || theme.id.includes('synthwave');
    if (selectedCategory === 'gaming') return theme.id.includes('gamer') || theme.id.includes('cyberpunk') || theme.id.includes('synthwave');
    if (selectedCategory === 'professional') return theme.id.includes('professional') || theme.id.includes('minimal');
    return false;
  });
  
  function selectTheme(themeId: string) {
    currentTheme.set(themeId);
    dispatch('theme-changed', { themeId });
  }
</script>

<div class="theme-gallery" role="region" aria-label="Theme selection">
  <!-- Category Tabs -->
  <div class="theme-categories" role="tablist">
    <button class="category-tab" 
            class:active={selectedCategory === 'all'}
            role="tab" 
            aria-selected={selectedCategory === 'all'}
            on:click={() => selectedCategory = 'all'}>
      All Themes
    </button>
    <button class="category-tab" 
            class:active={selectedCategory === 'dark'}
            role="tab" 
            aria-selected={selectedCategory === 'dark'}
            on:click={() => selectedCategory = 'dark'}>
      Dark Themes
    </button>
    <button class="category-tab" 
            class:active={selectedCategory === 'gaming'}
            role="tab" 
            aria-selected={selectedCategory === 'gaming'}
            on:click={() => selectedCategory = 'gaming'}>
      Gaming
    </button>
    <button class="category-tab" 
            class:active={selectedCategory === 'professional'}
            role="tab" 
            aria-selected={selectedCategory === 'professional'}
            on:click={() => selectedCategory = 'professional'}>
      Professional
    </button>
  </div>
  
  <!-- Theme Grid -->
  <div class="theme-grid" role="tabpanel">
    {#each filteredThemes as theme (theme.id)}
      <button class="theme-card" 
              class:active={$currentTheme === theme.id}
              aria-label="Select {theme.name} theme"
              aria-pressed={$currentTheme === theme.id}
              on:click={() => selectTheme(theme.id)}>
        
        <!-- Theme Preview -->
        <div class="theme-preview">
          <div class="preview-background" 
               style="background-color: {theme.color_scheme.colors.background};">
            <div class="preview-surface" 
                 style="background-color: {theme.color_scheme.colors.surface};">
              <div class="preview-accent" 
                   style="background-color: {theme.color_scheme.colors.primary};">
              </div>
              <div class="preview-text" 
                   style="color: {theme.color_scheme.colors.text};">
                Aa
              </div>
            </div>
          </div>
        </div>
        
        <!-- Theme Info -->
        <div class="theme-info">
          <h4 class="theme-name">{theme.name}</h4>
          <p class="theme-description">{theme.description}</p>
        </div>
        
        <!-- Active Indicator -->
        {#if $currentTheme === theme.id}
          <div class="active-indicator" aria-hidden="true">
            <Icon name="check" />
          </div>
        {/if}
      </button>
    {/each}
  </div>
</div>

<style>
  .theme-gallery {
    padding: 1rem;
  }
  
  .theme-categories {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid var(--theme-border-subtle);
  }
  
  .category-tab {
    padding: 0.5rem 1rem;
    background: transparent;
    border: none;
    color: var(--theme-text-muted);
    cursor: pointer;
    border-bottom: 2px solid transparent;
    transition: all 0.2s ease;
  }
  
  .category-tab:hover {
    color: var(--theme-text);
    background: var(--theme-surface);
  }
  
  .category-tab.active {
    color: var(--theme-primary);
    border-bottom-color: var(--theme-primary);
  }
  
  .theme-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
  }
  
  .theme-card {
    position: relative;
    background: var(--theme-surface);
    border: 1px solid var(--theme-border);
    border-radius: 8px;
    padding: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
  }
  
  .theme-card:hover {
    border-color: var(--theme-primary);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }
  
  .theme-card.active {
    border-color: var(--theme-primary);
    box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.2);
  }
  
  .theme-preview {
    width: 100%;
    height: 80px;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 0.75rem;
  }
  
  .preview-background {
    width: 100%;
    height: 100%;
    padding: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .preview-surface {
    width: 80%;
    height: 80%;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px;
  }
  
  .preview-accent {
    width: 20px;
    height: 20px;
    border-radius: 50%;
  }
  
  .preview-text {
    font-weight: 600;
    font-size: 14px;
  }
  
  .theme-info {
    margin-bottom: 0.5rem;
  }
  
  .theme-name {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--theme-text);
    margin: 0 0 0.25rem 0;
  }
  
  .theme-description {
    font-size: 0.75rem;
    color: var(--theme-text-muted);
    margin: 0;
    line-height: 1.3;
  }
  
  .active-indicator {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    width: 24px;
    height: 24px;
    background: var(--theme-primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--theme-background);
  }
</style>
\`\`\`

## Theme Switching Implementation

### Programmatic Theme Switching

\`\`\`typescript
// Theme switching service
import { currentTheme, activeColorScheme, themeUtils } from '$lib/stores/themes';

export class ThemeService {
  static switchTheme(themeId: string): void {
    // Validate theme exists
    if (!themePresets[themeId]) {
      console.warn(`Theme "${themeId}" not found`);
      return;
    }
    
    // Update store
    currentTheme.set(themeId);
    
    // Apply CSS custom properties
    const scheme = themePresets[themeId].color_scheme;
    themeUtils.applyTheme(scheme);
    
    // Save to localStorage
    localStorage.setItem('ultimon-current-theme', themeId);
    
    // Announce to screen readers
    this.announceThemeChange(themePresets[themeId].name);
  }
  
  static announceThemeChange(themeName: string): void {
    const announcement = document.getElementById('theme-announcements');
    if (announcement) {
      announcement.textContent = `Theme changed to ${themeName}`;
    }
  }
  
  static getSystemPreference(): 'dark' | 'light' {
    if (typeof window === 'undefined') return 'dark';
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  
  static initializeTheme(): void {
    const savedTheme = localStorage.getItem('ultimon-current-theme');
    const systemPreference = this.getSystemPreference();
    
    if (savedTheme && themePresets[savedTheme]) {
      this.switchTheme(savedTheme);
    } else {
      // Default to dark theme regardless of system preference
      this.switchTheme('dark_default');
    }
  }
}
\`\`\`

### Theme Toggle Component

\`\`\`svelte
<!-- ThemeToggle.svelte -->
<script lang="ts">
  import { currentTheme, themePresets } from '$lib/stores/themes';
  import { ThemeService } from '$lib/services/themeService';
  
  let isOpen = false;
  let buttonRef: HTMLButtonElement;
  
  $: currentThemeData = themePresets[$currentTheme];
  
  function toggleDropdown() {
    isOpen = !isOpen;
  }
  
  function selectTheme(themeId: string) {
    ThemeService.switchTheme(themeId);
    isOpen = false;
    buttonRef.focus();
  }
  
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      isOpen = false;
      buttonRef.focus();
    }
  }
</script>

<div class="theme-toggle" on:keydown={handleKeydown}>
  <button 
    bind:this={buttonRef}
    class="theme-button"
    aria-label="Select theme: {currentThemeData.name}"
    aria-expanded={isOpen}
    aria-haspopup="listbox"
    on:click={toggleDropdown}>
    
    <div class="theme-preview-mini">
      <div class="preview-dot" 
           style="background-color: {currentThemeData.color_scheme.colors.primary};">
      </div>
      <div class="preview-dot" 
           style="background-color: {currentThemeData.color_scheme.colors.secondary};">
      </div>
      <div class="preview-dot" 
           style="background-color: {currentThemeData.color_scheme.colors.accent};">
      </div>
    </div>
    
    <span class="theme-name">{currentThemeData.name}</span>
    <Icon name="chevron-down" class="chevron" class:rotated={isOpen} />
  </button>
  
  {#if isOpen}
    <div class="theme-dropdown" role="listbox" aria-label="Available themes">
      {#each Object.values(themePresets) as theme (theme.id)}
        <button 
          class="theme-option"
          class:selected={$currentTheme === theme.id}
          role="option"
          aria-selected={$currentTheme === theme.id}
          on:click={() => selectTheme(theme.id)}>
          
          <div class="option-preview">
            <div class="preview-dot" 
                 style="background-color: {theme.color_scheme.colors.primary};">
            </div>
            <div class="preview-dot" 
                 style="background-color: {theme.color_scheme.colors.secondary};">
            </div>
            <div class="preview-dot" 
                 style="background-color: {theme.color_scheme.colors.accent};">
            </div>
          </div>
          
          <div class="option-info">
            <span class="option-name">{theme.name}</span>
            <span class="option-description">{theme.description}</span>
          </div>
          
          {#if $currentTheme === theme.id}
            <Icon name="check" class="check-icon" />
          {/if}
        </button>
      {/each}
    </div>
  {/if}
</div>

<!-- Screen reader announcements -->
<div id="theme-announcements" aria-live="polite" aria-atomic="true" class="sr-only">
</div>

<style>
  .theme-toggle {
    position: relative;
  }
  
  .theme-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    background: var(--theme-surface);
    border: 1px solid var(--theme-border);
    border-radius: 6px;
    color: var(--theme-text);
    cursor: pointer;
    transition: all 0.2s ease;
    min-width: 160px;
  }
  
  .theme-button:hover {
    background: var(--theme-surface-elevated);
    border-color: var(--theme-primary);
  }
  
  .theme-button:focus {
    outline: 2px solid var(--theme-primary);
    outline-offset: 2px;
  }
  
  .theme-preview-mini {
    display: flex;
    gap: 2px;
  }
  
  .preview-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }
  
  .theme-name {
    flex: 1;
    text-align: left;
    font-size: 0.875rem;
    font-weight: 500;
  }
  
  .chevron {
    transition: transform 0.2s ease;
  }
  
  .chevron.rotated {
    transform: rotate(180deg);
  }
  
  .theme-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: var(--theme-surface-elevated);
    border: 1px solid var(--theme-border);
    border-radius: 6px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    z-index: 1000;
    max-height: 300px;
    overflow-y: auto;
    margin-top: 4px;
  }
  
  .theme-option {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    width: 100%;
    padding: 0.75rem;
    background: transparent;
    border: none;
    color: var(--theme-text);
    cursor: pointer;
    transition: background-color 0.2s ease;
    text-align: left;
  }
  
  .theme-option:hover {
    background: var(--theme-surface);
  }
  
  .theme-option.selected {
    background: rgba(0, 212, 255, 0.1);
  }
  
  .option-preview {
    display: flex;
    gap: 2px;
  }
  
  .option-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .option-name {
    font-size: 0.875rem;
    font-weight: 500;
  }
  
  .option-description {
    font-size: 0.75rem;
    color: var(--theme-text-muted);
    line-height: 1.2;
  }
  
  .check-icon {
    color: var(--theme-primary);
    width: 16px;
    height: 16px;
  }
</style>
\`\`\`

## Custom Theme Creation

### Theme Builder Interface

\`\`\`svelte
<!-- ThemeBuilder.svelte -->
<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { themeUtils } from '$lib/stores/themes';
  import ColorPicker from '$lib/components/ui/ColorPicker.svelte';
  
  const dispatch = createEventDispatcher();
  
  let customTheme = {
    name: 'My Custom Theme',
    description: 'A personalized theme',
    colors: {
      primary: '#00d4ff',
      secondary: '#0099cc',
      accent: '#ff6b35',
      background: '#010204',
      surface: '#0a0f14',
      surface_elevated: '#141b22',
      border: '#1e2832',
      border_subtle: '#0f1419',
      text: '#ffffff',
      text_muted: '#8892a0',
      text_subtle: '#5c6670',
      success: '#00ff88',
      warning: '#ffaa00',
      error: '#ff4757',
      info: '#00d4ff'
    }
  };
  
  function updateColor(colorKey: string, value: string) {
    customTheme.colors[colorKey] = value;
    customTheme = { ...customTheme };
    previewTheme();
  }
  
  function previewTheme() {
    const scheme = themeUtils.createCustomColorScheme(
      customTheme.name, 
      customTheme.colors
    );
    themeUtils.applyTheme(scheme);
  }
  
  function saveTheme() {
    const scheme = themeUtils.createCustomColorScheme(
      customTheme.name, 
      customTheme.colors
    );
    dispatch('theme-created', { scheme });
  }
</script>

<div class="theme-builder">
  <header class="builder-header">
    <h3>Custom Theme Builder</h3>
    <p>Create your own personalized theme</p>
  </header>
  
  <div class="builder-content">
    <!-- Theme Info -->
    <div class="theme-info-section">
      <div class="form-group">
        <label for="theme-name">Theme Name</label>
        <input 
          id="theme-name"
          type="text" 
          bind:value={customTheme.name}
          class="form-input">
      </div>
      
      <div class="form-group">
        <label for="theme-description">Description</label>
        <textarea 
          id="theme-description"
          bind:value={customTheme.description}
          class="form-textarea"
          rows="2">
        </textarea>
      </div>
    </div>
    
    <!-- Color Sections -->
    <div class="color-sections">
      <!-- Primary Colors -->
      <div class="color-section">
        <h4>Primary Colors</h4>
        <div class="color-grid">
          <div class="color-item">
            <label for="primary-color">Primary</label>
            <ColorPicker 
              id="primary-color"
              value={customTheme.colors.primary}
              on:change={(e) => updateColor('primary', e.detail.value)} />
          </div>
          
          <div class="color-item">
            <label for="secondary-color">Secondary</label>
            <ColorPicker 
              id="secondary-color"
              value={customTheme.colors.secondary}
              on:change={(e) => updateColor('secondary', e.detail.value)} />
          </div>
          
          <div class="color-item">
            <label for="accent-color">Accent</label>
            <ColorPicker 
              id="accent-color"
              value={customTheme.colors.accent}
              on:change={(e) => updateColor('accent', e.detail.value)} />
          </div>
        </div>
      </div>
      
      <!-- Background Colors -->
      <div class="color-section">
        <h4>Background Colors</h4>
        <div class="color-grid">
          <div class="color-item">
            <label for="background-color">Background</label>
            <ColorPicker 
              id="background-color"
              value={customTheme.colors.background}
              on:change={(e) => updateColor('background', e.detail.value)} />
          </div>
          
          <div class="color-item">
            <label for="surface-color">Surface</label>
            <ColorPicker 
              id="surface-color"
              value={customTheme.colors.surface}
              on:change={(e) => updateColor('surface', e.detail.value)} />
          </div>
          
          <div class="color-item">
            <label for="surface-elevated-color">Surface Elevated</label>
            <ColorPicker 
              id="surface-elevated-color"
              value={customTheme.colors.surface_elevated}
              on:change={(e) => updateColor('surface_elevated', e.detail.value)} />
          </div>
        </div>
      </div>
      
      <!-- Text Colors -->
      <div class="color-section">
        <h4>Text Colors</h4>
        <div class="color-grid">
          <div class="color-item">
            <label for="text-color">Text</label>
            <ColorPicker 
              id="text-color"
              value={customTheme.colors.text}
              on:change={(e) => updateColor('text', e.detail.value)} />
          </div>
          
          <div class="color-item">
            <label for="text-muted-color">Text Muted</label>
            <ColorPicker 
              id="text-muted-color"
              value={customTheme.colors.text_muted}
              on:change={(e) => updateColor('text_muted', e.detail.value)} />
          </div>
          
          <div class="color-item">
            <label for="text-subtle-color">Text Subtle</label>
            <ColorPicker 
              id="text-subtle-color"
              value={customTheme.colors.text_subtle}
              on:change={(e) => updateColor('text_subtle', e.detail.value)} />
          </div>
        </div>
      </div>
    </div>
    
    <!-- Preview -->
    <div class="theme-preview-section">
      <h4>Preview</h4>
      <div class="preview-container" 
           style="background-color: {customTheme.colors.background};">
        <div class="preview-widget" 
             style="background-color: {customTheme.colors.surface}; 
                    border-color: {customTheme.colors.border};">
          <div class="preview-header" 
               style="color: {customTheme.colors.text};">
            Widget Title
          </div>
          <div class="preview-content">
            <div class="preview-accent-bar" 
                 style="background-color: {customTheme.colors.primary};">
            </div>
            <div class="preview-text" 
                 style="color: {customTheme.colors.text_muted};">
              Sample content text
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <footer class="builder-footer">
    <button class="btn-secondary" on:click={() => dispatch('cancel')}>
      Cancel
    </button>
    <button class="btn-primary" on:click={saveTheme}>
      Save Theme
    </button>
  </footer>
</div>
\`\`\`

## Accessibility Considerations

### High Contrast Support

\`\`\`css
/* High contrast mode detection */
@media (prefers-contrast: high) {
  :root {
    --theme-border: #ffffff;
    --theme-text: #ffffff;
    --theme-background: #000000;
  }
  
  .theme-card {
    border-width: 2px;
  }
  
  .theme-button:focus {
    outline-width: 3px;
  }
}
\`\`\`

### Reduced Motion Support

\`\`\`css
/* Respect reduced motion preferences */
@media (prefers-reduced-motion: reduce) {
  .theme-card,
  .theme-button,
  .chevron {
    transition: none;
  }
  
  .theme-card:hover {
    transform: none;
  }
}
\`\`\`

### Color Blind Accessibility

All themes are designed with color blindness considerations:
- **Sufficient contrast ratios** for all color combinations
- **Multiple visual cues** beyond color (icons, text, patterns)
- **Tested with color blindness simulators** for protanopia, deuteranopia, and tritanopia
- **Alternative indicators** for status and state information

## Performance Optimization

### CSS Custom Properties Strategy

\`\`\`css
/* Efficient theme switching using CSS custom properties */
:root {
  /* Base theme variables */
  --theme-transition: color 0.2s ease, background-color 0.2s ease, border-color 0.2s ease;
}

/* All themed elements use custom properties */
.themed-element {
  color: var(--theme-text);
  background-color: var(--theme-surface);
  border-color: var(--theme-border);
  transition: var(--theme-transition);
}
\`\`\`

### Theme Preloading

\`\`\`typescript
// Preload theme assets
export class ThemePreloader {
  static preloadThemeAssets(themeId: string): void {
    const theme = themePresets[themeId];
    if (!theme) return;
    
    // Preload any theme-specific assets
    if (theme.visual_settings.enable_blur_effects) {
      this.preloadBlurShaders();
    }
    
    // Cache theme in memory
    this.cacheTheme(theme);
  }
  
  static preloadBlurShaders(): void {
    // Preload CSS filters and backdrop-filter support
    const testElement = document.createElement('div');
    testElement.style.backdropFilter = 'blur(10px)';
    document.body.appendChild(testElement);
    document.body.removeChild(testElement);
  }
  
  static cacheTheme(theme: ThemePreset): void {
    // Store theme in memory for instant switching
    sessionStorage.setItem(`theme_cache_${theme.id}`, JSON.stringify(theme));
  }
}
\`\`\`

This comprehensive theme system provides users with a rich selection of carefully crafted themes while maintaining the dark-first approach with the signature #010204 background color, ensuring an optimal monitoring experience across different preferences and use cases.
