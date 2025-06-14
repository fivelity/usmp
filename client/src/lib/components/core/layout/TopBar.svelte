<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { 
    widgets, 
    widgetGroups, 
    visualSettings, 
    dashboardLayout
  } from '$lib/stores';
  import { Download, Upload, Save, FolderOpen, Eye, Edit3, Grid3X3, Settings, RotateCcw, RotateCw } from '@lucide/svelte';
  import type { DashboardPreset } from '$lib/types/index';
  import { historyStore } from '$lib/stores/history';
  import { get } from 'svelte/store';
  import { uiUtils, getEditMode, getSelectedWidgets } from '$lib/stores/core/ui.svelte';
  import { visualUtils } from '$lib/stores/core/visual.svelte';
  import { addWidget, addWidgetGroup, widgetUtils } from '$lib/stores/data/widgets';

  const dispatch = createEventDispatcher();

  // Svelte 5 runes mode: use $props()
  const { showLeftSidebar, showRightSidebar } = $props<{ showLeftSidebar: boolean; showRightSidebar: boolean }>();

  let fileInput: HTMLInputElement;

  // History state
  let canUndo = $derived($historyStore.currentIndex >= 0);
  let canRedo = $derived($historyStore.currentIndex < $historyStore.commands.length - 1);

  function toggleEditMode() {
    uiUtils.toggleEditMode();
  }

  function toggleLeftSidebar() {
    dispatch('toggle-left-sidebar');
  }

  function toggleRightSidebar() {
    dispatch('toggle-right-sidebar');
  }

  // Enhanced preset management
  function exportPreset() {
    const preset: DashboardPreset = {
      id: crypto.randomUUID(),
      name: `Dashboard_${new Date().toISOString().split('T')[0]}`,
      description: 'Exported dashboard preset',
      widgets: Object.values(widgets),
      widget_groups: Object.values(widgetGroups),
      layout: get(dashboardLayout),
      visual_settings: visualSettings,
      created_at: new Date().toISOString(),
      version: '1.0'
    };

    const dataStr = JSON.stringify(preset, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `${preset.name}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }

  function triggerImport() {
    fileInput.click();
  }

  function handleFileImport(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const preset = JSON.parse(e.target?.result as string) as DashboardPreset;
        importPreset(preset);
      } catch (error) {
        console.error('Failed to import preset:', error);
        alert('Failed to import preset. Please check the file format.');
      }
    };
    reader.readAsText(file);
  }

  function importPreset(preset: DashboardPreset) {
    // Clear current widgets and groups
    widgetUtils.clearAllWidgets();
    widgetUtils.clearAllGroups();
    
    // Import widgets
    preset.widgets.forEach(widget => {
      addWidget(widget);
    });
    
    // Import groups
    preset.widget_groups.forEach(group => {
      addWidgetGroup(group);
    });
    
    // Update visual settings
    visualUtils.updateSettings(preset.visual_settings);
    
    // Update layout
    dashboardLayout.set(preset.layout);
    
    console.log('Successfully imported preset:', preset.name);
  }

  function savePresetToLocal() {
    const preset: DashboardPreset = {
      id: crypto.randomUUID(),
      name: `Local_${Date.now()}`,
      description: 'Local saved preset',
      widgets: Object.values(widgets),
      widget_groups: Object.values(widgetGroups),
      layout: get(dashboardLayout),
      visual_settings: visualSettings,
      created_at: new Date().toISOString(),
      version: '1.0'
    };

    const savedPresets = JSON.parse(localStorage.getItem('ultimon_presets') || '[]');
    savedPresets.push(preset);
    localStorage.setItem('ultimon_presets', JSON.stringify(savedPresets));
    
    console.log('Preset saved locally');
  }

  function loadPresetFromLocal() {
    const savedPresets = JSON.parse(localStorage.getItem('ultimon_presets') || '[]');
    if (savedPresets.length > 0) {
      // For now, load the most recent preset
      const latestPreset = savedPresets[savedPresets.length - 1];
      importPreset(latestPreset);
      console.log('Loaded latest local preset');
    } else {
      alert('No local presets found');
    }
  }
</script>

<div class="flex items-center justify-between px-4 py-2 bg-[var(--theme-surface)] border-b border-[var(--theme-border)]">
  <!-- Left section -->
  <div class="flex items-center space-x-2">
    <!-- Logo/Title -->
    <div class="text-lg font-bold text-[var(--theme-text)]">
      Ultimon
    </div>
    
    <div class="h-6 border-l border-[var(--theme-border)]"></div>
    
    <!-- Edit/View Mode Toggle -->
    <div class="flex items-center space-x-2">
      <button
        onclick={toggleEditMode}
        class="flex items-center gap-2 px-3 py-2 rounded-md transition-all duration-200"
        class:bg-blue-500={editMode}
        class:text-white={editMode}
        class:shadow-md={editMode}
        class:bg-gray-100={!editMode}
        class:text-gray-700={!editMode}
        class:hover:bg-blue-600={editMode}
        class:hover:bg-gray-200={!editMode}
        title={editMode ? 'Switch to View Mode' : 'Switch to Edit Mode'}
      >
        {#if getEditMode()}
          <Edit3 size={16} />
          <span class="text-sm font-medium">Editing</span>
          <span class="text-xs opacity-75">(Click to View)</span>
        {:else}
          <Eye size={16} />
          <span class="text-sm font-medium">Viewing</span>
          <span class="text-xs opacity-75">(Click to Edit)</span>
        {/if}
      </button>
    </div>

    <!-- Preset Management -->
    <div class="flex items-center space-x-1">
      <button
        onclick={savePresetToLocal}
        class="p-2 rounded-md hover:bg-[var(--theme-background)] text-[var(--theme-text)] transition-colors"
        title="Save Preset Locally"
      >
        <Save size={16} />
      </button>
      
      <button
        onclick={loadPresetFromLocal}
        class="p-2 rounded-md hover:bg-[var(--theme-background)] text-[var(--theme-text)] transition-colors"
        title="Load Local Preset"
      >
        <FolderOpen size={16} />
      </button>
      
      <button
        onclick={exportPreset}
        class="p-2 rounded-md hover:bg-[var(--theme-background)] text-[var(--theme-text)] transition-colors"
        title="Export Preset"
      >
        <Download size={16} />
      </button>
      
      <button
        onclick={triggerImport}
        class="p-2 rounded-md hover:bg-[var(--theme-background)] text-[var(--theme-text)] transition-colors"
        title="Import Preset"
      >
        <Upload size={16} />
      </button>
    </div>

    <!-- Undo/Redo Controls -->
    {#if getEditMode()}
      <div class="h-6 border-l border-[var(--theme-border)]"></div>
      
      <div class="flex items-center space-x-1">
        <button
          onclick={() => historyStore.undo()}
          disabled={!canUndo}
          class="p-2 rounded-md hover:bg-[var(--theme-background)] text-[var(--theme-text)] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          title="Undo (Ctrl+Z)"
        >
          <RotateCcw size={16} />
        </button>
        
        <button
          onclick={() => historyStore.redo()}
          disabled={!canRedo}
          class="p-2 rounded-md hover:bg-[var(--theme-background)] text-[var(--theme-text)] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          title="Redo (Ctrl+Y)"
        >
          <RotateCw size={16} />
        </button>
      </div>
    {/if}
  </div>

  <!-- Center section -->
  <div class="flex items-center space-x-4">
    {#if getEditMode() && getSelectedWidgets().size > 0}
      <div class="text-sm text-[var(--theme-text-muted)]">
        {getSelectedWidgets().size} widget{getSelectedWidgets().size === 1 ? '' : 's'} selected
      </div>
    {/if}
  </div>

  <!-- Right section -->
  <div class="flex items-center space-x-2">
    <!-- Grid toggle -->
    {#if getEditMode()}
      <button
        onclick={() => visualUtils.updateSettings({ show_grid: !visualSettings.show_grid })}
        class="p-2 rounded-md hover:bg-[var(--theme-background)] text-[var(--theme-text)] transition-colors"
        class:bg-blue-500={visualSettings.show_grid}
        class:text-white={visualSettings.show_grid}
        title="Toggle Grid"
      >
        <Grid3X3 size={16} />
      </button>
    {/if}
    
    <!-- Sidebar toggles -->
    <button
      onclick={toggleLeftSidebar}
      class="p-2 rounded-md hover:bg-[var(--theme-background)] text-[var(--theme-text)] transition-colors"
      class:bg-[var(--theme-primary)]={showLeftSidebar}
      class:text-white={showLeftSidebar}
      title="Toggle Sensor Panel"
    >
      <span class="text-sm font-medium">Sensors</span>
    </button>
    
    <button
      onclick={toggleRightSidebar}
      class="p-2 rounded-md hover:bg-[var(--theme-background)] text-[var(--theme-text)] transition-colors"
      class:bg-[var(--theme-primary)]={showRightSidebar}
      class:text-white={showRightSidebar}
      title="Toggle Inspector Panel"
    >
      <Settings size={16} />
    </button>
  </div>
</div>

<!-- Hidden file input for import -->
<input
  bind:this={fileInput}
  type="file"
  accept=".json"
  onchange={handleFileImport}
  class="hidden"
/>

<style>
  /* Add any additional styling here */
</style>
