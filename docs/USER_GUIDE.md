# Ultimate Sensor Monitor - User Guide (Version 2.0.0)

Welcome to the Ultimate Sensor Monitor v2.0.0! This guide will help you understand how to use the application to monitor your system's hardware and customize your dashboard.

## Table of Contents

1.  [Introduction](#1-introduction)
2.  [Getting Started](#2-getting-started)
*   [Launching the Application](#launching-the-application)
*   [Understanding the Interface](#understanding-the-interface)
3.  [Dashboard Customization](#3-dashboard-customization)
*   [Working with Widgets](#working-with-widgets)
*   [Adding Widgets](#adding-widgets)
*   [Moving and Resizing Widgets](#moving-and-resizing-widgets)
*   [Widget Configuration (Widget Inspector)](#widget-configuration-widget-inspector)
*   [Widget Locking and Grouping](#widget-locking-and-grouping)
4.  [Available Widget Types](#4-available-widget-types)
*   [Text Gauge](#text-gauge)
*   [Radial Gauge](#radial-gauge)
*   [Linear Gauge](#linear-gauge)
*   [Graph Gauge](#graph-gauge)
*   [Image Sequence Gauge](#image-sequence-gauge)
*   [Glassmorphic Gauge](#glassmorphic-gauge)
*   [System Status Widget](#system-status-widget)
5.  [Advanced Layout Tools](#5-advanced-layout-tools)
*   [Grid System](#grid-system)
*   [Snap Guides](#snap-guides)
*   [Alignment Tools](#alignment-tools)
6.  [Managing Sensor Sources](#6-managing-sensor-sources)
7.  [Themes and Appearance](#7-themes-and-appearance)
*   [Applying Pre-built Themes (ThemeGallery)](#applying-pre-built-themes-themegallery)
*   [Customizing Visual Dimensions (VisualDimensionsPanel)](#customizing-visual-dimensions-visualdimensionspanel)
8.  [Image Upload Manager (for Image Sequence Gauge)](#8-image-upload-manager)
9.  [Sharing and Importing Creations (ShareCreationModal)](#9-sharing-and-importing-creations-sharecreationmodal)
*   [Exporting Dashboard Presets](#exporting-dashboard-presets)
*   [Importing Dashboard Presets](#importing-dashboard-presets)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Introduction

Ultimate Sensor Monitor provides a real-time, customizable dashboard to visualize your PC's hardware sensor data. Version 2.0.0 brings a more robust, secure, and feature-rich experience with an enhanced UI and more powerful customization options.

## 2. Getting Started

### Launching the Application

-   **Windows Users**: Use the provided `start_ultimon_full.bat` (recommended for full functionality including backend sensor data) or `start_ultimon_quick.bat` (frontend only with mock data) scripts located in the project's root directory. You can also use `create_executable_shortcut.bat` to create desktop shortcuts for these.
-   **Other Platforms/Manual Start**: Follow the instructions in the [Setup Guide](SETUP_GUIDE.md). This typically involves starting the Python backend server and the Svelte frontend development server separately.

Once launched, the application will be accessible in your web browser, typically at `http://localhost:5173` (frontend) while the backend runs on `http://localhost:8000`.

### Understanding the Interface

The interface consists of:
-   **Top Bar**: Access to global controls like mode toggle (View/Edit), preset management (Load/Save), theme selection via the `ThemeGallery`, and access to the `ShareCreationModal`.
-   **Left Sidebar**: Contains the `SensorSourceList` to discover available sensors and add new widgets to the dashboard. It also hosts tools like the `WidgetGroupManager` and `ImageUploadManager`.
-   **Dashboard Canvas**: The main interactive area where you arrange, resize, and interact with your widgets. This is powered by the `DashboardCanvas` component.
-   **Right Sidebar**: Houses the `WidgetInspector` for configuring selected widgets and the `VisualDimensionsPanel` for global styling and theme adjustments.

## 3. Dashboard Customization

### Working with Widgets

Widgets are the core components of your dashboard, each displaying data from a specific sensor using various visual styles.

### Adding Widgets

1.  Ensure you are in **Edit Mode** (toggle in the Top Bar).
2.  Open the **Left Sidebar**.
3.  Browse or search the `SensorSourceList` for the desired sensor (e.g., CPU Temperature, GPU Load).
4.  Click or drag the sensor onto the **Dashboard Canvas**. A default widget (usually a Text Gauge) will be created.

### Moving and Resizing Widgets

In **Edit Mode**:
-   **Move**: Click and drag a widget to a new position. Snap guides will help with alignment.
-   **Resize**: Select a widget. Use the resize handles (small squares) that appear on its border to change its dimensions.

### Widget Configuration (Widget Inspector)

1.  Select a widget on the canvas (in Edit Mode).
2.  The **Right Sidebar** will display the `WidgetInspector`.
3.  Adjust settings such as:
-   **Gauge Type**: Change the visual representation (e.g., from Text to Radial).
-   **Sensor**: Reassign the widget to a different sensor if needed.
-   **Label**: Toggle visibility, set custom text.
-   **Unit**: Toggle visibility, set custom unit text.
-   **Value Display**: Toggle visibility of the sensor value.
-   **Gauge-Specific Settings**: Each gauge type has unique options (e.g., colors, ranges, animation styles for Image Sequence, metrics for System Status).
-   **Style Settings**: Background color, border, shadow, opacity, font.
-   **Animation Settings**: Configure how the widget animates or transitions.

### Widget Locking and Grouping

-   **Locking**: Prevent accidental changes to a widget's position or size. Access this via the widget's context menu (right-click on widget) or controls within the `WidgetInspector`.
-   **Grouping**: Select multiple widgets (Ctrl+Click or Shift+Click). Use the `WidgetGroupManager` in the Left Sidebar or context menu options to group them. Grouped widgets can be moved and managed as a single unit.

## 4. Available Widget Types

### Text Gauge
Displays sensor data as plain text.
-   **Configuration**: Font size, color, custom label, unit.
-   **Use Case**: Simple, direct display of sensor values like temperatures, clock speeds.

### Radial Gauge
Visualizes data using a circular, arc-style gauge.
-   **Configuration**: Min/max values, start/end angles, inner radius, primary/secondary colors, stroke width, glow effect.
-   **Use Case**: CPU/GPU utilization, fan speeds, progress-like metrics.

### Linear Gauge
Shows data as a horizontal or vertical bar.
-   **Configuration**: Min/max values, orientation, bar color, background color, scale visibility, gradient options.
-   **Use Case**: Memory usage, disk space, temperature bars.

### Graph Gauge
Plots sensor data over time as a line graph.
-   **Configuration**: Time range, line color, fill area, point visibility, grid visibility, entry animation.
-   **Use Case**: Tracking sensor trends, identifying spikes or drops in performance.

### Image Sequence Gauge
Displays sensor values by cycling through a user-uploaded sequence of images.
-   **Configuration**: Upload images via `ImageUploadManager`, define value ranges for each image in the sequence, set animation speed between frames.
-   **Use Case**: Highly custom visual feedback, e.g., an engine RPM gauge that visually "heats up" or changes appearance based on load.

### Glassmorphic Gauge
A modern gauge with a frosted glass effect, can be radial, linear, or ring-styled.
-   **Configuration**: Style (radial, linear, ring), glow intensity, blur level, transparency, colors.
-   **Use Case**: Visually appealing display for key metrics, fitting modern UI aesthetics.

### System Status Widget
Provides a compact, multi-metric display for an overview of system health.
-   **Configuration**:
-   **Layout**: `compact`, `detailed`, or `minimal`.
-   **Columns**: Number of columns for metrics (1-4).
-   **Metrics**: Add multiple system metrics, each linked to a sensor. For each metric:
    -   Select sensor.
    -   Set custom label and icon (emoji).
    -   Choose display format (number, percentage, temperature, frequency, bytes).
    -   Define warning/critical thresholds for color coding.
-   **Visuals**: Toggle icons, labels, values, units. Enable status colors.
-   **Animation**: Animate changes with fade, slide, or pulse effects.
-   **Use Case**: At-a-glance system health check (CPU temp, GPU load, RAM usage, etc., all in one widget).

## 5. Advanced Layout Tools

### Grid System
Enable an underlying grid on the `DashboardCanvas` for precise widget placement. Configure grid size, visibility, and snap-to-grid behavior in the `VisualDimensionsPanel` or global application settings.

### Snap Guides
Dynamic alignment lines (SnapGuides) appear when moving or resizing widgets, helping you align them precisely with other widgets or the grid lines.

### Alignment Tools
Select multiple widgets. Use alignment tools (available via context menu or potentially a dedicated `AlignmentTools` panel in the Left Sidebar) to align tops, bottoms, centers, or distribute spacing evenly.

## 6. Managing Sensor Sources

The backend application (Python/FastAPI) automatically detects available hardware sensors using libraries like LibreHardwareMonitor. The `SensorSourceList` in the Left Sidebar displays these detected sources and their individual sensors.
-   **Connection Status**: A `ConnectionStatus` indicator shows if the frontend is successfully connected to the backend WebSocket for real-time data.
-   **Troubleshooting**: If a sensor is not appearing, ensure the backend is running correctly and has the necessary permissions. Refer to the [Troubleshooting Guide](TROUBLESHOOTING.md).

## 7. Themes and Appearance

### Applying Pre-built Themes (ThemeGallery)
Access the `ThemeGallery` from the Top Bar. Browse and apply pre-built themes to instantly change the overall look and feel of your dashboard, including colors, fonts, and visual effects.

### Customizing Visual Dimensions (VisualDimensionsPanel)
Open the `VisualDimensionsPanel` from the Right Sidebar to fine-tune the visual environment:
-   **Materiality**: Adjusts the perceived depth and texture of UI elements.
-   **Information Density**: Controls spacing and size of elements.
-   **Animation Level**: Modifies the intensity and frequency of animations.
-   **Color Scheme**: Select base schemes (dark/light) and customize individual colors (primary, accent, background, etc.).
-   **Typography**: Change font family and scale.
-   **Effects**: Toggle blur, shadows, gradients, and reduce motion for accessibility.
-   **Grid Settings**: Configure grid size, visibility, and snapping.
-   **Border Radius**: Adjust default roundness of corners.
You can save your custom settings as a new theme preset.

## 8. Image Upload Manager

Accessible from the Left Sidebar, especially when an `ImageSequenceGauge` is selected or being configured.
-   Upload JPG, PNG, or GIF files.
-   Organize images into named sets (e.g., "CPU Load Animation").
-   Preview image sequences to ensure they animate as expected.
-   Assign these image sets to `ImageSequenceGauge` widgets.

## 9. Sharing and Importing Creations (ShareCreationModal)

Access the `ShareCreationModal` from the Top Bar to manage dashboard configurations.

### Exporting Dashboard Presets
Save your entire dashboard layout, all widget configurations, widget group definitions, and current visual/theme settings as a single JSON file (`DashboardPreset`). This allows you to back up your setup or share it with others.

### Importing Dashboard Presets
Load a previously exported `DashboardPreset` JSON file to restore a complete dashboard configuration. This will overwrite your current layout.

## 10. Troubleshooting

Refer to the dedicated [Troubleshooting Guide](TROUBLESHOOTING.md) for common issues, solutions, and tips for diagnosing problems with sensor detection, backend connection, or widget display.

---

Thank you for using Ultimate Sensor Monitor! We hope you enjoy creating your personalized hardware dashboards.
