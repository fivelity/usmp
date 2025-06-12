# Navigation System Documentation

## Overview

The Ultimate Sensor Monitor features a **comprehensive navigation system** designed for efficiency, accessibility, and intuitive user interaction. The navigation is built around a dark-first design with the primary background color **#010204**, ensuring excellent visibility and reduced eye strain during extended monitoring sessions.

## Navigation Architecture

### Primary Navigation Structure

\`\`\`
┌─────────────────────────────────────────────────────────────┐
│                     Top Bar                                 │
├─────────────────────────────────────────────────────────────┤
│ Left     |                                       | Right    │
│ Sidebar  |          Main Canvas                  | Sidebar  │
│          |                                       |          │
│ - Widgets│         Dashboard Area                | - Props  │
│ - Sensors│                                       | - Themes │
│ - Tools  │                                       | - Config │
└─────────────────────────────────────────────────────────────┘
\`\`\`

### Navigation Components

1. **Top Bar**: Global actions and status indicators
2. **Left Sidebar**: Widget library, sensor browser, and tools
3. **Right Sidebar**: Properties panel, themes, and configuration
4. **Main Canvas**: Interactive dashboard workspace
5. **Context Menus**: Right-click actions and quick access
6. **Modal Dialogs**: Settings, import/export, image upload, and detailed configuration

## Top Bar Navigation

### Layout and Structure

\`\`\`html
<header class="top-bar" role="banner">
  <div class="top-bar-left">
    <!-- Logo and App Title -->
    <div class="app-branding">
      <img src="/logo.svg" alt="Ultimate Sensor Monitor" class="logo">
      <h1 class="app-title">Ultimate Sensor Monitor</h1>
    </div>
    
    <!-- Main Navigation -->
    <nav class="main-nav" role="navigation" aria-label="Main navigation">
      <button class="nav-item" aria-label="Dashboard">
        <Icon name="dashboard" />
        <span>Dashboard</span>
      </button>
      <button class="nav-item" aria-label="Widgets">
        <Icon name="widgets" />
        <span>Widgets</span>
      </button>
      <button class="nav-item" aria-label="Sensors">
        <Icon name="sensors" />
        <span>Sensors</span>
      </button>
    </nav>
  </div>
  
  <div class="top-bar-center">
    <!-- Dashboard Title and Status -->
    <div class="dashboard-info">
      <h2 class="dashboard-title">My Gaming Setup</h2>
      <span class="connection-status" aria-live="polite">
        <Icon name="wifi" />
        Connected
      </span>
    </div>
  </div>
  
  <div class="top-bar-right">
    <!-- Action Buttons -->
    <div class="action-buttons">
      <button class="btn-icon" aria-label="Grid settings" title="Grid Settings">
        <Icon name="grid" />
      </button>
      <button class="btn-icon" aria-label="Theme selector" title="Theme Selector">
        <Icon name="palette" />
      </button>
      <button class="btn-icon" aria-label="Settings" title="Settings">
        <Icon name="settings" />
      </button>
      <button class="btn-icon" aria-label="Share dashboard" title="Share">
        <Icon name="share" />
      </button>
    </div>
  </div>
</header>
\`\`\`

### Top Bar Features

#### Connection Status Indicator
- **Real-time status**: Live connection status with visual indicators
- **Color coding**: Green (connected), yellow (connecting), red (disconnected)
- **Accessibility**: Screen reader announcements for status changes
- **Tooltip information**: Detailed connection information on hover

#### Quick Actions
- **Grid Toggle**: Enable/disable grid snapping and visibility
- **Theme Selector**: Quick access to theme switching
- **Settings**: Global application settings
- **Share**: Export and sharing options

## Left Sidebar Navigation

### Widget Library Panel Example

\`\`\`html
<aside class="left-sidebar" role="complementary" aria-label="Widget library and tools">
  <div class="sidebar-section">
    <h3 class="section-title">
      <Icon name="widgets" />
      Widget Library
      <button class="collapse-btn" aria-label="Collapse widget library">
        <Icon name="chevron-down" />
      </button>
    </h3>
    
    <div class="widget-categories">
      <div class="category-group">
        <h4 class="category-title">Gauges</h4>
        <div class="widget-grid">
          <button class="widget-item" draggable="true" 
                  aria-label="Radial gauge widget"
                  data-widget-type="radial">
            <div class="widget-preview">
              <Icon name="gauge-radial" />
            </div>
            <span class="widget-name">Radial Gauge</span>
          </button>
          <!-- More widget items -->
        </div>
      </div>
    </div>
  </div>
</aside>
\`\`\`

#### Widget Categories

1. **Gauges**
   - Radial Gauge
   - Linear Gauge
   - Arc Gauge
   - System Status

2. **Graphs**
   - Line Chart
   - Area Chart
   - Bar Chart
   - Real-time Graph

3. **Text & Info**
   - Text Display
   - Value Display
   - Status Indicator
   - Clock Widget

4. **Custom**
   - Image Sequence
~~   - Glassmorphic Panel ~~
~~   - Custom Background ~~

#### Drag and Drop Interface Example

\`\`\`typescript
// Widget drag implementation
function handleWidgetDragStart(event: DragEvent, widgetType: string) {
  event.dataTransfer?.setData('application/widget-type', widgetType);
  event.dataTransfer?.setData('text/plain', widgetType);
  
  // Visual feedback
  const dragImage = createDragPreview(widgetType);
  event.dataTransfer?.setDragImage(dragImage, 50, 50);
}

function handleCanvasDrop(event: DragEvent) {
  event.preventDefault();
  const widgetType = event.dataTransfer?.getData('application/widget-type');
  const position = getDropPosition(event);
  
  if (widgetType) {
    createWidget(widgetType, position);
  }
}
\`\`\`

### Sensor Browser Panel Example

\`\`\`html
<div class="sidebar-section">
  <h3 class="section-title">
    <Icon name="sensors" />
    Sensor Browser
    <div class="section-actions">
      <button class="btn-icon-sm" aria-label="Refresh sensors" title="Refresh">
        <Icon name="refresh" />
      </button>
      <button class="btn-icon-sm" aria-label="Sensor settings" title="Settings">
        <Icon name="settings" />
      </button>
    </div>
  </h3>
  
  <div class="sensor-tree" role="tree" aria-label="Hardware sensors">
    <div class="sensor-category" role="treeitem" aria-expanded="true">
      <button class="category-toggle" aria-label="Expand CPU sensors">
        <Icon name="chevron-down" />
        <Icon name="cpu" />
        <span>CPU (Intel i7-12700K)</span>
      </button>
      
      <div class="sensor-list" role="group">
        <div class="sensor-item" role="treeitem" draggable="true"
             aria-label="CPU temperature sensor">
          <Icon name="thermometer" />
          <span class="sensor-name">CPU Temperature</span>
          <span class="sensor-value">65°C</span>
        </div>
        <!-- More sensor items -->
      </div>
    </div>
  </div>
</div>
\`\`\`

#### Sensor Tree/List Features

- **Hierarchical structure**: Organized by hardware component (or default structure provided by driver)
- **Real-time values**: Live sensor readings in the tree/list
- **Drag and drop**: Drag sensors directly to canvas
- **Search functionality**: Filter sensors by name or type
- **Status indicators**: Visual indicators for sensor working state

### Tools Panel Example

\`\`\`html
<div class="sidebar-section">
  <h3 class="section-title">
    <Icon name="tools" />
    Tools
  </h3>
  
  <div class="tool-grid">
    <button class="tool-item" aria-label="Alignment tools">
      <Icon name="align-center" />
      <span>Align</span>
    </button>
    <button class="tool-item" aria-label="Distribution tools">
      <Icon name="distribute" />
      <span>Distribute</span>
    </button>
    <button class="tool-item" aria-label="Grid settings">
      <Icon name="grid" />
      <span>Grid</span>
    </button>
    <button class="tool-item" aria-label="Snap settings">
      <Icon name="magnet" />
      <span>Snap</span>
    </button>
  </div>
</div>
\`\`\`

## Right Sidebar Navigation

### Properties Panel Example

\`\`\`html
<aside class="right-sidebar" role="complementary" aria-label="Properties and configuration">
  <div class="sidebar-section">
    <h3 class="section-title">
      <Icon name="settings" />
      Properties
    </h3>
    
    <div class="properties-content" role="tabpanel">
      <!-- Dynamic content based on selection -->
      <div class="property-group">
        <label class="property-label" for="widget-title">Title</label>
        <input type="text" id="widget-title" class="property-input" 
               value="CPU Temperature" aria-describedby="title-help">
        <small id="title-help" class="property-help">
          Display name for this widget
        </small>
      </div>
      
      <div class="property-group">
        <label class="property-label" for="sensor-select">Sensor</label>
        <select id="sensor-select" class="property-select">
          <option value="cpu_temp">CPU Temperature</option>
          <option value="gpu_temp">GPU Temperature</option>
        </select>
      </div>
    </div>
  </div>
</aside>
\`\`\`

### Theme Gallery Panel Example

\`\`\`html
<div class="sidebar-section">
  <h3 class="section-title">
    <Icon name="palette" />
    Themes
  </h3>
  
  <div class="theme-gallery">
    <div class="theme-categories">
      <button class="category-tab active" data-category="all">All</button>
      <button class="category-tab" data-category="dark">Dark</button>
      <button class="category-tab" data-category="gaming">Gaming</button>
      <button class="category-tab" data-category="professional">Professional</button>
    </div>
    
    <div class="theme-grid">
      <button class="theme-card active" data-theme="dark_default"
              aria-label="Dark Default theme" aria-pressed="true">
        <div class="theme-preview">
          <div class="preview-bg" style="background: #010204;"></div>
          <div class="preview-accent" style="background: #00d4ff;"></div>
        </div>
        <span class="theme-name">Dark Default</span>
      </button>
      <!-- More theme cards -->
    </div>
  </div>
</div>
\`\`\`

## Interactive Elements

### Context Menus Example

\`\`\`html
<div class="context-menu" role="menu" aria-label="Widget actions">
  <button class="menu-item" role="menuitem" aria-label="Edit widget">
    <Icon name="edit" />
    <span>Edit</span>
    <kbd class="shortcut">E</kbd>
  </button>
  <button class="menu-item" role="menuitem" aria-label="Duplicate widget">
    <Icon name="copy" />
    <span>Duplicate</span>
    <kbd class="shortcut">Ctrl+D</kbd>
  </button>
  <div class="menu-separator" role="separator"></div>
  <button class="menu-item danger" role="menuitem" aria-label="Delete widget">
    <Icon name="trash" />
    <span>Delete</span>
    <kbd class="shortcut">Del</kbd>
  </button>
</div>
\`\`\`

### Modal Dialogs Example

\`\`\`html
<div class="modal-overlay" role="dialog" aria-labelledby="settings-title" 
     aria-describedby="settings-description">
  <div class="modal-container">
    <header class="modal-header">
      <h2 id="settings-title" class="modal-title">Settings</h2>
      <button class="modal-close" aria-label="Close settings">
        <Icon name="x" />
      </button>
    </header>
    
    <div class="modal-body">
      <p id="settings-description" class="modal-description">
        Configure application preferences and behavior.
      </p>
      <!-- Settings content -->
    </div>
    
    <footer class="modal-footer">
      <button class="btn-secondary">Cancel</button>
      <button class="btn-primary">Save Changes</button>
    </footer>
  </div>
</div>
\`\`\`

## Keyboard Navigation

### Keyboard Shortcuts Example

| Shortcut | Action | Context |
|----------|--------|---------|
| `Tab` | Navigate between elements | Global |
| `Shift+Tab` | Navigate backwards | Global |
| `Enter` | Activate button/link | Focused element |
| `Space` | Toggle checkbox/button | Focused element |
| `Escape` | Close modal/menu | Modal/Menu |
| `Ctrl+S` | Save dashboard | Dashboard |
| `Ctrl+Z` | Undo action | Dashboard |
| `Ctrl+Y` | Redo action | Dashboard |
| `Delete` | Delete selected widget | Selected widget |
| `Ctrl+D` | Duplicate widget | Selected widget |
| `Arrow Keys` | Move widget (1px) | Selected widget |
| `Shift+Arrow` | Move widget (10px) | Selected widget |

### Focus Management Example

\`\`\`typescript
// Focus trap for modals
class FocusTrap {
  private focusableElements: HTMLElement[];
  private firstElement: HTMLElement;
  private lastElement: HTMLElement;
  
  constructor(container: HTMLElement) {
    this.focusableElements = this.getFocusableElements(container);
    this.firstElement = this.focusableElements[0];
    this.lastElement = this.focusableElements[this.focusableElements.length - 1];
  }
  
  handleTabKey(event: KeyboardEvent) {
    if (event.key !== 'Tab') return;
    
    if (event.shiftKey) {
      if (document.activeElement === this.firstElement) {
        event.preventDefault();
        this.lastElement.focus();
      }
    } else {
      if (document.activeElement === this.lastElement) {
        event.preventDefault();
        this.firstElement.focus();
      }
    }
  }
}
\`\`\`

## Accessibility Features

### Screen Reader Support Example

\`\`\`html
<!-- Live regions for dynamic updates -->
<div aria-live="polite" aria-atomic="true" class="sr-only">
  <span id="status-announcements"></span>
</div>

<!-- Skip links for keyboard users -->
<a href="#main-content" class="skip-link">Skip to main content</a>
<a href="#sidebar-nav" class="skip-link">Skip to navigation</a>

<!-- Landmark elements -->
<main id="main-content" role="main" aria-label="Dashboard workspace">
  <!-- Main content -->
</main>

<nav role="navigation" aria-label="Widget library">
  <!-- Navigation content -->
</nav>
\`\`\`

### ARIA Labels and Descriptions Example

\`\`\`html
<!-- Descriptive labels -->
<button aria-label="Add radial gauge widget to dashboard" 
        aria-describedby="radial-gauge-description">
  <Icon name="gauge-radial" />
  Radial Gauge
</button>

<div id="radial-gauge-description" class="sr-only">
  Creates a circular gauge perfect for displaying temperature, 
  percentage, or other numeric values with visual appeal.
</div>

<!-- State announcements -->
<button aria-pressed="true" aria-label="Grid snapping enabled">
  <Icon name="grid" />
  Grid Snap
</button>
\`\`\`

### Color and Contrast

All navigation elements meet WCAG 2.1 AA standards:
- **Text contrast**: Minimum 4.5:1 ratio
- **Interactive elements**: Enhanced contrast for better visibility
- **Focus indicators**: High contrast focus rings
- **Status indicators**: Multiple visual cues (color + icon + text)

## Responsive Behavior

### Mobile Navigation Example

\`\`\`html
<!-- Mobile navigation toggle -->
<button class="mobile-nav-toggle" aria-label="Toggle navigation menu"
        aria-expanded="false" aria-controls="mobile-nav">
  <Icon name="menu" />
</button>

<!-- Collapsible mobile navigation -->
<nav id="mobile-nav" class="mobile-nav" aria-hidden="true">
  <div class="mobile-nav-content">
    <!-- Simplified navigation for mobile -->
  </div>
</nav>
\`\`\`

### Breakpoint Adaptations

- **Desktop (1024px+)**: Full sidebar navigation
- **Tablet (768px-1023px)**: Collapsible sidebars
- **Mobile (< 768px)**: Drawer-style navigation
- **Touch devices**: Larger touch targets (44px minimum)

## Performance Considerations

### Lazy Loading Example

\`\`\`typescript
// Lazy load sidebar content
const LazyWidgetLibrary = lazy(() => import('./WidgetLibrary.svelte'));
const LazySensorBrowser = lazy(() => import('./SensorBrowser.svelte'));

// Virtualized lists for large datasets
import { VirtualList } from '@sveltejs/virtual-list';
\`\`\`

### Smooth Animations Example

\`\`\`css
/* Hardware-accelerated animations */
.sidebar-panel {
  transform: translateX(-100%);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: transform;
}

.sidebar-panel.open {
  transform: translateX(0);
}
\`\`\`

This navigation system provides a comprehensive, accessible, and efficient way for users to interact with the Ultimate Sensor Monitor, ensuring that all functionality is discoverable and usable across different devices and interaction methods.
