<script lang="ts">
  import { currentTheme, themeUtils } from '$lib/stores/themes';
  import { Button } from '../index';

  // Enhanced theme presets with gamer and professional focus
  const enhancedThemePresets = {
    // Professional Themes (Dieter Rams inspired)
    professional_minimal: {
      id: 'professional_minimal',
      name: 'Professional Minimal',
      description: 'Clean, functional design inspired by Dieter Rams principles',
      category: 'professional',
      visual_settings: {
        materiality: 0.1,
        information_density: 0.4,
        animation_level: 0.2,
        enable_blur_effects: false,
        enable_animations: true,
        reduce_motion: false
      },
      color_scheme: {
        id: 'professional_minimal',
        name: 'Professional Minimal',
        isDark: false,
        colors: {
          primary: '#2563eb',
          secondary: '#64748b',
          accent: '#0ea5e9',
          background: '#ffffff',
          surface: '#f8fafc',
          border: '#e2e8f0',
          text: '#0f172a',
          text_muted: '#64748b',
          success: '#059669',
          warning: '#d97706',
          error: '#dc2626',
          info: '#0284c7'
        }
      }
    },
    
    professional_dark: {
      id: 'professional_dark',
      name: 'Professional Dark',
      description: 'Sophisticated dark theme for professional environments',
      category: 'professional',
      visual_settings: {
        materiality: 0.3,
        information_density: 0.5,
        animation_level: 0.3,
        enable_blur_effects: true,
        enable_animations: true,
        reduce_motion: false
      },
      color_scheme: {
        id: 'professional_dark',
        name: 'Professional Dark',
        isDark: true,
        colors: {
          primary: '#3b82f6',
          secondary: '#6366f1',
          accent: '#8b5cf6',
          background: '#0f172a',
          surface: '#1e293b',
          border: '#334155',
          text: '#f1f5f9',
          text_muted: '#94a3b8',
          success: '#10b981',
          warning: '#f59e0b',
          error: '#ef4444',
          info: '#06b6d4'
        }
      }
    },

    // Gamer Themes
    gamer_neon: {
      id: 'gamer_neon',
      name: 'Gamer Neon',
      description: 'High-energy neon theme for gaming setups',
      category: 'gamer',
      visual_settings: {
        materiality: 0.8,
        information_density: 0.7,
        animation_level: 0.9,
        enable_blur_effects: true,
        enable_animations: true,
        reduce_motion: false
      },
      color_scheme: {
        id: 'gamer_neon',
        name: 'Gamer Neon',
        isDark: true,
        colors: {
          primary: '#00ff41',
          secondary: '#ff0080',
          accent: '#ffff00',
          background: '#0a0a0a',
          surface: '#1a1a1a',
          border: '#333333',
          text: '#ffffff',
          text_muted: '#a0a0a0',
          success: '#00ff41',
          warning: '#ffff00',
          error: '#ff0080',
          info: '#00ffff'
        }
      }
    },

    gamer_cyberpunk: {
      id: 'gamer_cyberpunk',
      name: 'Cyberpunk 2077',
      description: 'Futuristic cyberpunk aesthetic with neon accents',
      category: 'gamer',
      visual_settings: {
        materiality: 0.9,
        information_density: 0.8,
        animation_level: 0.8,
        enable_blur_effects: true,
        enable_animations: true,
        reduce_motion: false
      },
      color_scheme: {
        id: 'gamer_cyberpunk',
        name: 'Cyberpunk 2077',
        isDark: true,
        colors: {
          primary: '#ff006e',
          secondary: '#8338ec',
          accent: '#ffbe0b',
          background: '#0d1b2a',
          surface: '#2d1b69',
          border: '#415a77',
          text: '#ffffff',
          text_muted: '#a8dadc',
          success: '#06ffa5',
          warning: '#ffbe0b',
          error: '#ff006e',
          info: '#8338ec'
        }
      }
    },

    gamer_synthwave: {
      id: 'gamer_synthwave',
      name: 'Synthwave Retro',
      description: '80s retrowave vibes with gradient effects',
      category: 'gamer',
      visual_settings: {
        materiality: 0.7,
        information_density: 0.6,
        animation_level: 0.7,
        enable_blur_effects: true,
        enable_animations: true,
        reduce_motion: false
      },
      color_scheme: {
        id: 'gamer_synthwave',
        name: 'Synthwave Retro',
        isDark: true,
        colors: {
          primary: '#ff0080',
          secondary: '#00ffff',
          accent: '#ffff00',
          background: '#1a0033',
          surface: '#2d1b69',
          border: '#7209b7',
          text: '#ffffff',
          text_muted: '#c77dff',
          success: '#00ffff',
          warning: '#ffff00',
          error: '#ff0080',
          info: '#7209b7'
        }
      }
    },

    // FUI (Fantasy User Interface) Themes
    fui_military: {
      id: 'fui_military',
      name: 'Military HUD',
      description: 'Tactical military interface design',
      category: 'fui',
      visual_settings: {
        materiality: 0.6,
        information_density: 0.8,
        animation_level: 0.6,
        enable_blur_effects: false,
        enable_animations: true,
        reduce_motion: false
      },
      color_scheme: {
        id: 'fui_military',
        name: 'Military HUD',
        isDark: true,
        colors: {
          primary: '#00ff00',
          secondary: '#ffff00',
          accent: '#ff8800',
          background: '#001100',
          surface: '#002200',
          border: '#004400',
          text: '#00ff00',
          text_muted: '#88ff88',
          success: '#00ff00',
          warning: '#ffff00',
          error: '#ff0000',
          info: '#00ffff'
        }
      }
    },

    fui_scifi: {
      id: 'fui_scifi',
      name: 'Sci-Fi Interface',
      description: 'Futuristic science fiction UI design',
      category: 'fui',
      visual_settings: {
        materiality: 0.8,
        information_density: 0.7,
        animation_level: 0.8,
        enable_blur_effects: true,
        enable_animations: true,
        reduce_motion: false
      },
      color_scheme: {
        id: 'fui_scifi',
        name: 'Sci-Fi Interface',
        isDark: true,
        colors: {
          primary: '#00d4ff',
          secondary: '#0099cc',
          accent: '#66e0ff',
          background: '#0a1929',
          surface: '#1e3a5f',
          border: '#2d5aa0',
          text: '#ffffff',
          text_muted: '#b3d9ff',
          success: '#00ff88',
          warning: '#ffaa00',
          error: '#ff4444',
          info: '#00d4ff'
        }
      }
    }
  };

  // Categorize themes
  let categorizedThemes = $derived({
    professional: Object.values(enhancedThemePresets).filter(t => t.category === 'professional'),
    gamer: Object.values(enhancedThemePresets).filter(t => t.category === 'gamer'),
    fui: Object.values(enhancedThemePresets).filter(t => t.category === 'fui')
  });

  function applyTheme(themeId: string) {
    currentTheme.set(themeId);
    
    // Apply the theme immediately
    const theme = enhancedThemePresets[themeId as keyof typeof enhancedThemePresets];
    if (theme) {
      themeUtils.applyTheme(theme.color_scheme);
    }
  }

  function getPreviewGradient(theme: any) {
    const colors = theme.color_scheme.colors;
    return `linear-gradient(135deg, ${colors.primary}, ${colors.secondary}, ${colors.accent})`;
  }
</script>

<div class="theme-gallery">
  <div class="gallery-header">
    <h2>Theme Gallery</h2>
    <p>Choose from professional, gaming, and FUI themes designed for different use cases</p>
  </div>

  <!-- Professional Themes -->
  <div class="theme-category">
    <h3>
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
      </svg>
      Professional
    </h3>
    <p class="category-description">Clean, functional designs inspired by Dieter Rams principles</p>
    
    <div class="theme-grid">
      {#each categorizedThemes.professional as theme}
        <div 
          class="theme-card"
          class:active={$currentTheme === theme.id}
          role="button"
          tabindex="0"
          onclick={() => applyTheme(theme.id)}
          onkeydown={(e) => { if (e.key === 'Enter') applyTheme(theme.id); }}
        >
          <div class="theme-preview" style="background: {getPreviewGradient(theme)}">
            <div class="preview-elements">
              <div class="preview-widget" style="background: {theme.color_scheme.colors.surface}; border-color: {theme.color_scheme.colors.border}">
                <div class="preview-text" style="color: {theme.color_scheme.colors.text}">CPU</div>
                <div class="preview-value" style="color: {theme.color_scheme.colors.primary}">45°C</div>
              </div>
              <div class="preview-gauge">
                <div class="gauge-fill" style="background: {theme.color_scheme.colors.primary}"></div>
              </div>
            </div>
          </div>
          
          <div class="theme-info">
            <h4>{theme.name}</h4>
            <p>{theme.description}</p>
            
            <div class="theme-colors">
              <div class="color-dot" style="background: {theme.color_scheme.colors.primary}" title="Primary"></div>
              <div class="color-dot" style="background: {theme.color_scheme.colors.secondary}" title="Secondary"></div>
              <div class="color-dot" style="background: {theme.color_scheme.colors.accent}" title="Accent"></div>
            </div>
          </div>
        </div>
      {/each}
    </div>
  </div>

  <!-- Gaming Themes -->
  <div class="theme-category">
    <h3>
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
      </svg>
      Gaming
    </h3>
    <p class="category-description">High-energy themes perfect for gaming setups and enthusiasts</p>
    
    <div class="theme-grid">
      {#each categorizedThemes.gamer as theme}
        <div 
          class="theme-card"
          class:active={$currentTheme === theme.id}
          role="button"
          tabindex="0"
          onclick={() => applyTheme(theme.id)}
          onkeydown={(e) => { if (e.key === 'Enter') applyTheme(theme.id); }}
        >
          <div class="theme-preview" style="background: {getPreviewGradient(theme)}">
            <div class="preview-elements">
              <div class="preview-widget gamer" style="background: {theme.color_scheme.colors.surface}; border-color: {theme.color_scheme.colors.border}">
                <div class="preview-text" style="color: {theme.color_scheme.colors.text}">GPU</div>
                <div class="preview-value glow" style="color: {theme.color_scheme.colors.primary}">78°C</div>
              </div>
              <div class="preview-gauge gamer">
                <div class="gauge-fill glow" style="background: {theme.color_scheme.colors.primary}"></div>
              </div>
            </div>
          </div>
          
          <div class="theme-info">
            <h4>{theme.name}</h4>
            <p>{theme.description}</p>
            
            <div class="theme-colors">
              <div class="color-dot glow" style="background: {theme.color_scheme.colors.primary}" title="Primary"></div>
              <div class="color-dot glow" style="background: {theme.color_scheme.colors.secondary}" title="Secondary"></div>
              <div class="color-dot glow" style="background: {theme.color_scheme.colors.accent}" title="Accent"></div>
            </div>
          </div>
        </div>
      {/each}
    </div>
  </div>

  <!-- FUI Themes -->
  <div class="theme-category">
    <h3>
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
      </svg>
      FUI (Fantasy UI)
    </h3>
    <p class="category-description">Futuristic interfaces inspired by sci-fi and military HUDs</p>
    
    <div class="theme-grid">
      {#each categorizedThemes.fui as theme}
        <div 
          class="theme-card"
          class:active={$currentTheme === theme.id}
          role="button"
          tabindex="0"
          onclick={() => applyTheme(theme.id)}
          onkeydown={(e) => { if (e.key === 'Enter') applyTheme(theme.id); }}
        >
          <div class="theme-preview" style="background: {getPreviewGradient(theme)}">
            <div class="preview-elements">
              <div class="preview-widget fui" style="background: {theme.color_scheme.colors.surface}; border-color: {theme.color_scheme.colors.border}">
                <div class="preview-text" style="color: {theme.color_scheme.colors.text}">SYS</div>
                <div class="preview-value" style="color: {theme.color_scheme.colors.primary}">ONLINE</div>
              </div>
              <div class="preview-gauge fui">
                <div class="gauge-fill" style="background: {theme.color_scheme.colors.primary}"></div>
              </div>
            </div>
          </div>
          
          <div class="theme-info">
            <h4>{theme.name}</h4>
            <p>{theme.description}</p>
            
            <div class="theme-colors">
              <div class="color-dot" style="background: {theme.color_scheme.colors.primary}" title="Primary"></div>
              <div class="color-dot" style="background: {theme.color_scheme.colors.secondary}" title="Secondary"></div>
              <div class="color-dot" style="background: {theme.color_scheme.colors.accent}" title="Accent"></div>
            </div>
          </div>
        </div>
      {/each}
    </div>
  </div>

  <!-- Custom Theme Actions -->
  <div class="custom-actions">
    <Button variant="outline" onclick={() => console.log('Create Custom Theme')}>
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
      </svg>
      Create Custom
    </Button>
    
    <Button variant="outline" onclick={() => console.log('Import Theme')}>
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
      </svg>
      Import Theme
    </Button>
  </div>
</div>

<style>
  .theme-gallery {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
  }

  .gallery-header {
    text-align: center;
    margin-bottom: 3rem;
  }

  .gallery-header h2 {
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    color: #1e293b;
  }

  .gallery-header p {
    font-size: 1.125rem;
    color: #64748b;
    margin: 0;
  }

  .theme-category {
    margin-bottom: 3rem;
  }

  .theme-category h3 {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
    color: #1e293b;
  }

  .category-description {
    font-size: 1rem;
    color: #64748b;
    margin: 0 0 1.5rem 0;
  }

  .theme-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .theme-card {
    background: white;
    border-radius: 1rem;
    border: 2px solid #e2e8f0;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .theme-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    border-color: #3b82f6;
  }

  .theme-card.active {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  .theme-preview {
    height: 120px;
    padding: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
  }

  .preview-elements {
    display: flex;
    gap: 1rem;
    align-items: center;
  }

  .preview-widget {
    padding: 0.75rem;
    border-radius: 0.5rem;
    border: 1px solid;
    min-width: 80px;
    text-align: center;
  }

  .preview-widget.gamer {
    box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
  }

  .preview-widget.fui {
    clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 100%, 10px 100%);
  }

  .preview-text {
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
  }

  .preview-value {
    font-size: 1rem;
    font-weight: 700;
  }

  .preview-value.glow {
    text-shadow: 0 0 10px currentColor;
  }

  .preview-gauge {
    width: 60px;
    height: 8px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    overflow: hidden;
  }

  .preview-gauge.gamer {
    box-shadow: 0 0 5px rgba(0, 255, 255, 0.5);
  }

  .preview-gauge.fui {
    border-radius: 0;
    clip-path: polygon(0 0, calc(100% - 4px) 0, 100% 100%, 4px 100%);
  }

  .gauge-fill {
    height: 100%;
    width: 70%;
    transition: width 0.3s ease;
  }

  .gauge-fill.glow {
    box-shadow: 0 0 10px currentColor;
  }

  .theme-info {
    padding: 1.5rem;
  }

  .theme-info h4 {
    font-size: 1.125rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
    color: #1e293b;
  }

  .theme-info p {
    font-size: 0.875rem;
    color: #64748b;
    margin: 0 0 1rem 0;
    line-height: 1.5;
  }

  .theme-colors {
    display: flex;
    gap: 0.5rem;
  }

  .color-dot {
    width: 1rem;
    height: 1rem;
    border-radius: 50%;
    border: 2px solid white;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  }

  .color-dot.glow {
    box-shadow: 0 0 8px currentColor, 0 1px 3px rgba(0, 0, 0, 0.2);
  }

  .custom-actions {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 1px solid #e2e8f0;
  }

  /* Dark mode adjustments */
  :global(.dark) .theme-card {
    background: #1e293b;
    border-color: #334155;
  }

  :global(.dark) .gallery-header h2,
  :global(.dark) .theme-category h3,
  :global(.dark) .theme-info h4 {
    color: #f1f5f9;
  }

  :global(.dark) .gallery-header p,
  :global(.dark) .category-description,
  :global(.dark) .theme-info p {
    color: #94a3b8;
  }
</style>
