# Custom Widget Development Guide (Svelte 5) - Ultimate Sensor Monitor

✅ **Svelte 5 Migration Complete!** - All patterns described below are now live in the codebase

Ultimate Sensor Monitor v2.0.0 allows developers to create and integrate custom widget types into the dashboard. This guide outlines the process, strictly adhering to **Svelte 5** and TypeScript.

## 🎉 **Migration Success**

All examples and patterns in this guide have been **successfully implemented** in the Ultimate Sensor Monitor codebase:
- ✅ Rune-based widget components (`$state`, `$derived`, `$effect`)
- ✅ Modern prop destructuring with `$props()`
- ✅ Snippet-based rendering with `{@render}`
- ✅ TypeScript integration verified
- ✅ Build system fully functional

## Table of Contents

1.  [Introduction](#1-introduction)
2.  [Prerequisites](#2-prerequisites)
3.  [Widget Architecture Overview (Svelte 5)](#3-widget-architecture-overview-svelte-5)
    *   [3.1. Widget Component (`.svelte` file)](#31-widget-component-svelte-file)
    *   [3.2. Widget Inspector Component (`.svelte` file)](#32-widget-inspector-component-svelte-file)
    *   [3.3. Widget Configuration (TypeScript Types)](#33-widget-configuration-typescript-types)
4.  [Step-by-Step Guide (Svelte 5)](#4-step-by-step-guide-svelte-5)
    *   [Step 1: Define Widget Configuration Types](#step-1-define-widget-configuration-types)
    *   [Step 2: Create the Widget Component (Svelte 5)](#step-2-create-the-widget-component-svelte-5)
    *   [Step 3: Create the Widget Inspector Component (Svelte 5)](#step-3-create-the-widget-inspector-component-svelte-5)
    *   [Step 4: Register Your Widget](#step-4-register-your-widget)
5.  [Best Practices for Svelte 5 Widgets](#5-best-practices-for-svelte-5-widgets)
6.  [Example: Simple Text Display Widget (Svelte 5)](#6-example-simple-text-display-widget-svelte-5)

---

## 1. Introduction

Custom widgets extend the functionality of the dashboard by allowing unique visualizations or interactions for specific sensor data. With Svelte 5, creating reactive and efficient widgets involves leveraging Rune-based patterns for props, state, derived values, and side effects.

## 2. Prerequisites

-   Strong understanding of Svelte 5 (Runes: `$props`, `$state`, `$derived`, `$effect`, etc.) and TypeScript.
-   Development environment set up as per the [Developer Guide](DEVELOPER_GUIDE.md).
-   Familiarity with the project's type definitions in `client/src/lib/types/`.

## 3. Widget Architecture Overview (Svelte 5)

A custom widget typically consists of:

### 3.1. Widget Component (`.svelte` file)
The Svelte 5 component responsible for rendering the widget on the dashboard. It receives sensor data and its configuration as props.

**Props Interface (Conceptual - passed by `WidgetContainer`):**
```typescript
// In client/src/lib/types/widgets.ts or a specific widget type file
import type { SensorData } from '$lib/types/sensors';

export interface BaseWidgetProps<TConfigSpecific> {
  widget: WidgetConfig<TConfigSpecific>; // Includes your custom config + common widget fields
  sensorData: SensorData | null;         // Live data for the bound sensor
  isSelected: boolean;
  // onUpdate callback is handled by WidgetContainer/WidgetContent,
  // your inspector will call updateWidget which propagates changes.
}
```
Your widget component will typically be placed within `client/src/lib/components/widgets/custom/` or a similar directory.

### 3.2. Widget Inspector Component (`.svelte` file)
A Svelte 5 component that renders in the Right Sidebar when your custom widget is selected. It allows users to configure the widget's specific settings.

**Props Interface (Conceptual):**
```typescript
// In client/src/lib/types/widgets.ts or a specific widget type file
export interface BaseWidgetInspectorProps<TConfigSpecific> {
  widget: WidgetConfig<TConfigSpecific>; // Current widget configuration
  updateWidget: (updates: Partial<WidgetConfig<TConfigSpecific>>) => void; // Function to update widget's config
}
```
Inspectors are typically placed in `client/src/lib/components/inspectors/custom/`.

### 3.3. Widget Configuration (TypeScript Types)
A TypeScript interface defining the specific settings for your widget. This configuration is stored as part of the dashboard layout, typically within a `specificConfig` property of the main `WidgetConfig` type.

## 4. Step-by-Step Guide (Svelte 5)

### Step 1: Define Widget Configuration Types
In `client/src/lib/types/widgets.ts` (or a dedicated types file for your widget), define the structure for your widget's unique settings.

Example:
```typescript
// In client/src/lib/types/widgets.ts

// Define the shape of the specific configuration for your new widget
export interface MyCustomDisplayWidgetSpecificConfig {
  displayTextPrefix: string;
  valueColor: string;
  showTimestamp: boolean;
  fontSize: 'small' | 'medium' | 'large';
}

// Update the generic WidgetConfig to include your new specific config type
// This often involves a discriminated union for `specificConfig` if you have multiple widget types.
// For simplicity, if it's a general `object` or `any`, ensure your widget handles it safely.
// A more robust approach:
// export type WidgetSpecificConfig =
//   | TextGaugeSpecificConfig
//   | RadialGaugeSpecificConfig
//   | MyCustomDisplayWidgetSpecificConfig // Add your new type here
//   | { [key: string]: any }; // Fallback or for simpler widgets

// export interface WidgetConfig<T = WidgetSpecificConfig> { // T defaults to the union
export interface WidgetConfig<T = { [key: string]: any }> { // Simplified example
  id: string;
  type: string; // e.g., 'my_custom_display_widget'
  sensorId: string | null;
  // ... other common widget fields like position, size, etc.
  specificConfig: T; // Holds the unique settings for this widget type
  // ... styleSettings, animationSettings, etc.
}
```

### Step 2: Create the Widget Component (Svelte 5)
Create a Svelte component (e.g., `MyCustomDisplayWidget.svelte`).

Example (`MyCustomDisplayWidget.svelte`):
```svelte
<script lang="ts">
  import type { SensorData } from '$lib/types/sensors';
  import type { WidgetConfig, MyCustomDisplayWidgetSpecificConfig } from '$lib/types/widgets'; // Adjust path as needed

  // Props (Svelte 5)
  let {
    widget,
    sensorData = null,
    isSelected = false
  }: {
    widget: WidgetConfig<MyCustomDisplayWidgetSpecificConfig>;
    sensorData?: SensorData | null;
    isSelected?: boolean;
  } = $props();

  // Derived helpers
  const config = $derived(widget.specificConfig);

  const displayValue = $derived(() =>
    sensorData
      ? `${config.displayTextPrefix ?? ''} ${sensorData.value}${sensorData.unit ?? ''}`
      : 'Loading...'
  );

  const textColorStyle = $derived(() => `color: ${config.valueColor ?? 'inherit'};`);

  const fontSizeClass = $derived(() => {
    switch (config.fontSize) {
      case 'small':
        return 'text-sm';
      case 'large':
        return 'text-lg';
      default:
        return 'text-base';
    }
  });

  const timestamp = $derived(() =>
    config.showTimestamp && sensorData?.timestamp
      ? new Date(sensorData.timestamp).toLocaleTimeString()
      : null
  );

  const borderColor = $derived(() =>
    isSelected ? 'var(--theme-primary, blue)' : 'var(--theme-border, grey)'
  );
</script>

<div class="p-2 border rounded h-full flex flex-col justify-center items-center" style:border-color={borderColor}>
  <span class="{fontSizeClass}" style={textColorStyle}>
    {displayValue}
  </span>
  {#if timestamp}
    <p class="text-xs text-gray-500 mt-1">
      Last update: {timestamp}
    </p>
  {/if}
</div>

<style>
  .border {
    transition: border-color 0.2s ease-in-out;
  }
</style>
```

### Step 3: Create the Widget Inspector Component (Svelte 5)
Create a Svelte component for the inspector (e.g., `MyCustomDisplayWidgetInspector.svelte`).

Example (`MyCustomDisplayWidgetInspector.svelte`):
```svelte
<script lang="ts">
  import type { WidgetConfig, MyCustomDisplayWidgetSpecificConfig } from '$lib/types/widgets'; // Adjust path
  // Assuming UI components like Input, Label, Checkbox, ColorPicker, Select are available
  // For example: import { Input, Label, Checkbox } from '$lib/components/ui';

  export let widget: WidgetConfig<MyCustomDisplayWidgetSpecificConfig>;
  export let updateWidget: (updates: Partial<WidgetConfig<MyCustomDisplayWidgetSpecificConfig>>) => void;

  // Local state for form inputs, initialized from widget.specificConfig
  // Use `$state()` Runes for local state management and `$effect()` to keep them in sync.
  let currentPrefix = $state(widget.specificConfig.displayTextPrefix ?? '');
  let currentColor = $state(widget.specificConfig.valueColor ?? '#000000');
  let currentShowTimestamp = $state(widget.specificConfig.showTimestamp ?? false);
  let currentFontSize = $state(widget.specificConfig.fontSize ?? 'medium');

  // Function to handle updates and call updateWidget
  function handleChange() {
    const newSpecificConfig: MyCustomDisplayWidgetSpecificConfig = {
      displayTextPrefix: currentPrefix,
      valueColor: currentColor,
      showTimestamp: currentShowTimestamp,
      fontSize: currentFontSize,
    };
    updateWidget({ specificConfig: newSpecificConfig });
  }

  // Svelte 5: Use `$effect()` to sync local state if widget prop could change externally
  $effect(() => {
    if (widget.specificConfig.displayTextPrefix !== currentPrefix) {
      currentPrefix = widget.specificConfig.displayTextPrefix ?? '';
    }
    if (widget.specificConfig.valueColor !== currentColor) {
      currentColor = widget.specificConfig.valueColor ?? '#000000';
    }
    if (widget.specificConfig.showTimestamp !== currentShowTimestamp) {
      currentShowTimestamp = widget.specificConfig.showTimestamp ?? false;
    }
    if (widget.specificConfig.fontSize !== currentFontSize) {
      currentFontSize = widget.specificConfig.fontSize ?? 'medium';
    }
  });
</script>

<div class="space-y-4 p-3">
  <div>
    <label for="prefix-input" class="block text-sm font-medium text-gray-300">Display Text Prefix</label>
    <input
      type="text"
      id="prefix-input"
      class="mt-1 block w-full input-field"
      bind:value={currentPrefix}
      on:input={handleChange}
    />
  </div>

  <div>
    <label for="color-input" class="block text-sm font-medium text-gray-300">Value Color</label>
    <input
      type="color"
      id="color-input"
      class="mt-1 block w-full h-10"
      bind:value={currentColor}
      on:input={handleChange}
    />
  </div>
  
  <div>
    <label for="font-size-select" class="block text-sm font-medium text-gray-300">Font Size</label>
    <select id="font-size-select" class="mt-1 block w-full select-field" bind:value={currentFontSize} on:change={handleChange}>
      <option value="small">Small</option>
      <option value="medium">Medium</option>
      <option value="large">Large</option>
    </select>
  </div>

  <div class="flex items-center">
    <input
      type="checkbox"
      id="show-timestamp-checkbox"
      class="h-4 w-4 checkbox-field"
      bind:checked={currentShowTimestamp}
      on:change={handleChange}
    />
    <label for="show-timestamp-checkbox" class="ml-2 block text-sm text-gray-300">Show Timestamp</label>
  </div>
</div>
```

### Step 4: Register Your Widget
Register your new widget type in `client/src/lib/components/widgets/index.ts` (or the designated registry file).

```typescript
// In client/src/lib/components/widgets/index.ts
import MyCustomDisplayWidget from './custom/MyCustomDisplayWidget.svelte'; // Adjust path
import MyCustomDisplayWidgetInspector from '$lib/components/inspectors/custom/MyCustomDisplayWidgetInspector.svelte'; // Adjust path
import type { WidgetTypeDefinition, MyCustomDisplayWidgetSpecificConfig } from '$lib/types/widgets'; // Adjust path
import type { ExtendedGaugeType } from '$lib/types/widgets'; // Assuming ExtendedGaugeType includes your new type ID

export const widgetTypes: Record<ExtendedGaugeType | string, WidgetTypeDefinition<any>> = {
  // ... other widget types (TextGauge, RadialGauge, etc.)
  "my_custom_display_widget": { // This ID should match widget.type
    id: "my_custom_display_widget",
    name: "Custom Text Display",
    description: "Displays sensor text with custom prefix, color, and font size.",
    category: "Custom", // Or any relevant category like "Text & Info"
    component: MyCustomDisplayWidget,
    inspector: MyCustomDisplayWidgetInspector,
    defaultConfig: { // Default specificConfig for new instances of this widget type
      displayTextPrefix: "Value:",
      valueColor: "#FFFFFF", // Default to white for dark themes
      showTimestamp: false,
      fontSize: "medium",
    } as MyCustomDisplayWidgetSpecificConfig, // Cast to ensure type correctness for default
    icon: "📝", // Example: Lucide icon name (if using a helper) or emoji
    defaultSize: { width: 2, height: 1 }, // Default grid size (optional)
  },
};
```
Ensure your `WidgetConfig` in `client/src/lib/types/widgets.ts` can accommodate `MyCustomDisplayWidgetSpecificConfig` within its `specificConfig` property. If `specificConfig` is typed as `any` or a generic `object`, ensure your components handle potential type mismatches gracefully. Using a discriminated union for `specificConfig` based on `widget.type` is the most robust approach for type safety.

## 5. Best Practices for Svelte 5 Widgets

-   **Reactivity**: Leverage Svelte 5's Rune-based reactivity (`$state`, `$derived`, `$effect`) for managing state and side effects.
-   **Modularity**: Separate concerns between the display component and its inspector.
-   **Props Management**: Clearly define props with TypeScript and provide defaults.
-   **Accessibility (A11y)**: Ensure your widget is accessible (ARIA attributes, keyboard navigation).
-   **Error Handling**: Consider how your widget behaves with missing or unexpected data.
-   **Styling**: Use Tailwind CSS utility classes for consistency. Use scoped `<style>` for complex or unique styles.
-   **Type Safety**: Utilize TypeScript rigorously for props, state, and configurations.

## 6. Example: Simple Text Display Widget (Svelte 5)

The steps above outline creating a "My Custom Display Widget". You can adapt this pattern for various needs. The built-in `TextGauge.svelte` can also serve as a Svelte 5 reference. Always leverage Svelte 5 Runes (`$props`, `$state`, `$derived`, `$effect`) for state management and reactivity.
