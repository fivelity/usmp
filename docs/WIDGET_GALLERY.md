# Widget Gallery & Examples

## Overview
This gallery showcases all available widgets in the Ultimate Sensor Monitor, including built-in widgets and custom examples. Each widget includes configuration examples, use cases, and best practices.

## Built-in Widgets

### Text Display Widget
**Purpose**: Simple text value display with optional labels and units
**Best for**: Quick status indicators, simple metrics

\`\`\`typescript
const textWidget: WidgetConfig = {
  gauge_type: 'text',
  gauge_settings: {
    show_label: true,
    show_unit: true,
    font_size: 'large',
    text_align: 'center',
    color_scheme: 'auto'
  }
}
\`\`\`

**Use Cases**:
- CPU/GPU names and models
- Current time and date
- System uptime
- Simple status messages

### Radial Gauge Widget
**Purpose**: Circular progress indicator with customizable ranges
**Best for**: Percentage values, temperature monitoring, load indicators

\`\`\`typescript
const radialWidget: WidgetConfig = {
  gauge_type: 'radial',
  gauge_settings: {
    start_angle: -90,
    end_angle: 270,
    stroke_width: 12,
    show_glow: true,
    gradient_colors: ['#00ff00', '#ffff00', '#ff0000'],
    show_value: true,
    show_label: true
  }
}
\`\`\`

**Use Cases**:
- CPU/GPU usage percentages
- Temperature monitoring
- Memory usage
- Fan speed indicators

### Linear Bar Widget
**Purpose**: Horizontal or vertical progress bars
**Best for**: Memory usage, storage capacity, network throughput

\`\`\`typescript
const linearWidget: WidgetConfig = {
  gauge_type: 'linear',
  gauge_settings: {
    orientation: 'horizontal',
    show_scale: true,
    show_gradient: true,
    bar_height: 20,
    corner_radius: 10,
    background_opacity: 0.3
  }
}
\`\`\`

**Use Cases**:
- RAM usage bars
- Storage capacity indicators
- Network bandwidth meters
- Battery level indicators

### Time Graph Widget
**Purpose**: Historical data visualization with time series
**Best for**: Trend analysis, performance monitoring over time

\`\`\`typescript
const graphWidget: WidgetConfig = {
  gauge_type: 'graph',
  gauge_settings: {
    time_range: 300, // 5 minutes
    show_grid: true,
    line_color: '#3b82f6',
    fill_area: true,
    show_points: false,
    animate_entry: true,
    y_axis_auto_scale: true
  }
}
\`\`\`

**Use Cases**:
- CPU temperature over time
- Memory usage trends
- Network activity graphs
- Performance monitoring

### Image Sequence Widget
**Purpose**: Custom animations based on sensor values
**Best for**: Creative visualizations, themed dashboards

\`\`\`typescript
const imageWidget: WidgetConfig = {
  gauge_type: 'image',
  gauge_settings: {
    image_sequence: [
      '/images/cpu_cold.png',
      '/images/cpu_warm.png',
      '/images/cpu_hot.png'
    ],
    animation_speed: 500,
    value_ranges: [0, 50, 80, 100],
    smooth_transitions: true
  }
}
\`\`\`

**Use Cases**:
- Animated CPU cooler based on temperature
- RGB lighting effects
- Custom gaming-themed indicators
- Brand-specific visualizations

### Glassmorphic Widget
**Purpose**: Modern glass effect gauges with blur and transparency
**Best for**: Premium aesthetics, modern UI themes

\`\`\`typescript
const glassWidget: WidgetConfig = {
  gauge_type: 'glassmorphic',
  gauge_settings: {
    style: 'radial',
    glow_intensity: 0.5,
    blur_level: 0.3,
    transparency: 0.8,
    border_gradient: true,
    shadow_depth: 'medium'
  }
}
\`\`\`

**Use Cases**:
- High-end gaming setups
- Professional workstation monitoring
- Modern minimalist dashboards
- Premium brand presentations

## Custom Widgets

### System Status Widget
**Purpose**: Multi-metric overview with configurable layout
**Best for**: Dashboard overviews, system health monitoring

\`\`\`typescript
const systemStatusWidget: WidgetConfig = {
  gauge_type: 'system_status',
  gauge_settings: {
    layout: 'compact',
    columns: 2,
    metrics: [
      {
        id: 'cpu_usage',
        sensor_id: 'cpu_load',
        label: 'CPU Usage',
        icon: '🔥',
        format: 'percentage',
        warning_threshold: 75,
        critical_threshold: 90
      },
      {
        id: 'gpu_temp',
        sensor_id: 'gpu_temperature',
        label: 'GPU Temp',
        icon: '🌡️',
        format: 'temperature',
        warning_threshold: 70,
        critical_threshold: 85
      },
      {
        id: 'memory_usage',
        sensor_id: 'memory_used',
        label: 'Memory',
        icon: '💾',
        format: 'bytes',
        warning_threshold: 80,
        critical_threshold: 95
      },
      {
        id: 'network_speed',
        sensor_id: 'network_download',
        label: 'Network',
        icon: '🌐',
        format: 'bytes',
        unit: 'MB/s'
      }
    ],
    show_icons: true,
    show_labels: true,
    use_status_colors: true,
    animate_changes: true,
    update_animation: 'fade'
  }
}
\`\`\`

**Configuration Options**:
- **Layout**: Compact, detailed, or minimal
- **Columns**: 1-4 columns for metric arrangement
- **Status Colors**: Automatic color coding based on thresholds
- **Animations**: Smooth transitions for value changes
- **Custom Icons**: Emoji or custom icons for each metric

**Use Cases**:
- System overview dashboards
- Server monitoring panels
- Gaming PC status displays
- Workstation health monitoring

## Widget Combinations & Layouts

### Gaming Setup Dashboard
\`\`\`typescript
const gamingDashboard = [
  // Large CPU temperature graph
  {
    gauge_type: 'graph',
    pos_x: 0, pos_y: 0,
    width: 400, height: 200,
    sensor_id: 'cpu_temperature'
  },
  
  // GPU radial gauge
  {
    gauge_type: 'radial',
    pos_x: 420, pos_y: 0,
    width: 180, height: 180,
    sensor_id: 'gpu_usage'
  },
  
  // System status overview
  {
    gauge_type: 'system_status',
    pos_x: 0, pos_y: 220,
    width: 300, height: 150,
    gauge_settings: {
      layout: 'compact',
      columns: 2,
      metrics: [/* CPU, GPU, RAM, Storage */]
    }
  },
  
  // Animated RGB lighting
  {
    gauge_type: 'image',
    pos_x: 320, pos_y: 220,
    width: 280, height: 150,
    sensor_id: 'cpu_temperature',
    gauge_settings: {
      image_sequence: [/* RGB animation frames */]
    }
  }
]
\`\`\`

### Professional Workstation
\`\`\`typescript
const professionalDashboard = [
  // Clean linear bars for system metrics
  {
    gauge_type: 'linear',
    sensor_id: 'cpu_usage',
    gauge_settings: {
      orientation: 'horizontal',
      show_scale: true,
      color_scheme: 'professional'
    }
  },
  
  // Minimal text displays for specifications
  {
    gauge_type: 'text',
    sensor_id: 'cpu_name',
    gauge_settings: {
      show_label: false,
      font_size: 'small',
      text_align: 'left'
    }
  },
  
  // Time series for performance monitoring
  {
    gauge_type: 'graph',
    sensor_id: 'memory_usage',
    gauge_settings: {
      time_range: 600,
      show_grid: true,
      line_color: '#374151',
      fill_area: false
    }
  }
]
\`\`\`

### Server Monitoring Dashboard
\`\`\`typescript
const serverDashboard = [
  // System status with detailed metrics
  {
    gauge_type: 'system_status',
    gauge_settings: {
      layout: 'detailed',
      columns: 3,
      metrics: [
        { sensor_id: 'cpu_usage', label: 'CPU Load', format: 'percentage' },
        { sensor_id: 'memory_usage', label: 'Memory', format: 'percentage' },
        { sensor_id: 'disk_usage', label: 'Storage', format: 'percentage' },
        { sensor_id: 'network_in', label: 'Network In', format: 'bytes' },
        { sensor_id: 'network_out', label: 'Network Out', format: 'bytes' },
        { sensor_id: 'uptime', label: 'Uptime', format: 'number' }
      ],
      use_status_colors: true,
      warning_threshold: 70,
      critical_threshold: 90
    }
  },
  
  // Historical performance graphs
  {
    gauge_type: 'graph',
    sensor_id: 'cpu_usage',
    gauge_settings: {
      time_range: 3600, // 1 hour
      show_grid: true,
      y_axis_auto_scale: true
    }
  }
]
\`\`\`

## Widget Themes & Styling

### Gaming Themes
- **Cyberpunk**: Neon colors, glow effects, dark backgrounds
- **RGB**: Dynamic color changes, rainbow gradients
- **Retro**: 80s-inspired colors, scanline effects
- **Minimalist Gaming**: Clean lines with accent colors

### Professional Themes
- **Corporate**: Neutral colors, clean typography
- **Dieter Rams**: Minimal design, functional aesthetics
- **High Contrast**: Accessibility-focused, clear visibility
- **Monochrome**: Black and white with subtle accents

### Specialized Themes
- **Military/FUI**: Green monochrome, tactical aesthetics
- **Medical**: Clean whites and blues, clinical appearance
- **Industrial**: Robust design, warning colors
- **Scientific**: Data-focused, precise measurements

## Performance Considerations

### Widget Optimization
1. **Update Frequency**: Match widget update rates to sensor refresh rates
2. **Animation Performance**: Use CSS transforms for smooth animations
3. **Memory Usage**: Limit historical data retention for graphs
4. **Rendering Efficiency**: Use virtual scrolling for large widget lists

### Best Practices
1. **Sensor Selection**: Choose appropriate sensors for each widget type
2. **Layout Planning**: Consider screen real estate and information hierarchy
3. **Color Coding**: Use consistent color schemes across related widgets
4. **Responsive Design**: Ensure widgets work on different screen sizes

## Accessibility Features

### Screen Reader Support
- Proper ARIA labels for all interactive elements
- Descriptive text for visual indicators
- Keyboard navigation support

### Visual Accessibility
- High contrast mode support
- Customizable font sizes
- Color blind friendly palettes
- Reduced motion options

### Motor Accessibility
- Large click targets
- Keyboard shortcuts
- Voice control compatibility
- Touch-friendly interfaces

This widget gallery provides comprehensive examples and guidance for creating effective monitoring dashboards with the Ultimate Sensor Monitor platform.
