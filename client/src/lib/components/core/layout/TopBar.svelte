<script lang="ts">
  import { browser } from '$app/environment';
  import { historyStore as history } from '$lib/stores/history.svelte';
  import { ui } from '$lib/stores/core/ui.svelte';
  import { widgets as widgetStore } from '$lib/stores/data/widgets.svelte';
  import { dashboard as dashboardStore } from '$lib/stores/data/dashboard.svelte';
  import { firebase } from '$lib/services/firebase.svelte';
  import { visualSettings, visualUtils } from '$lib/stores/core/visual.svelte';

  import type { Preset } from '$lib/types/presets';
  import Button from '$lib/components/ui/common/Button.svelte';
  import Dropdown from '$lib/components/ui/common/Dropdown.svelte';
  import {
    PanelLeft,
    PanelRight,
    Pencil,
    Eye,
    Undo,
    Redo,
    Download,
    Upload,
    Save,
    Cloud,
    LogIn,
    LogOut,
    User as UserIcon,
    Loader2,
    Trash2,
    Sun,
    Moon
  } from 'lucide-svelte';
  
  let presets = $state<Preset[]>([]);
  let isLoadingPresets = $state(false);

  function handleExport() {
    if (!browser) return;

    const preset = {
      layout: dashboardStore.layout,
      widgets: widgetStore.widgetMap,
      version: '1.0.0',
      createdAt: new Date().toISOString()
    };

    const blob = new Blob([JSON.stringify(preset, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `usm-preset-${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    console.log('Exporting preset...', preset);
  }

  function handleImport() {
    if (!browser) return;
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'application/json';
    input.onchange = (event) => {
      const file = (event.target as HTMLInputElement).files?.[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          try {
            const preset = JSON.parse(e.target?.result as string);
            if (preset.layout && preset.widgets) {
              dashboardStore.setLayout(preset.layout);
              const widgetsArray = Array.isArray(preset.widgets)
                ? preset.widgets
                : Object.values(preset.widgets);
              widgetStore.setWidgets(widgetsArray);
              console.log('Preset imported successfully.');
            } else {
              console.error('Invalid preset file format.');
            }
          } catch (error) {
            console.error('Error parsing preset file:', error);
          }
        };
        reader.readAsText(file);
      }
    };
    input.click();
  }
  
  async function handleSaveToCloud() {
    if (!firebase.isAuthenticated) {
      alert('Please sign in to save presets to the cloud.');
      return;
    }
    const name = prompt('Enter a name for your preset:');
    if (name) {
      await firebase.savePreset(name, dashboardStore.layout, widgetStore.widgetMap);
      await handleLoadFromCloud();
    }
  }

  async function handleLoadFromCloud() {
    if (!firebase.isAuthenticated) {
      return;
    }
    isLoadingPresets = true;
    presets = await firebase.loadPresets();
    isLoadingPresets = false;
  }
  
  function applyPreset(preset: Preset) {
    if (preset.layout && preset.widgets) {
      dashboardStore.setLayout(preset.layout);
      widgetStore.setWidgets(Object.values(preset.widgets));
      console.log(`Preset "${preset.name}" applied.`);
    } else {
      console.error('Invalid preset data in cloud object.');
    }
  }

  async function handleDeletePreset(presetId: string) {
    if (!confirm('Are you sure you want to delete this preset?')) return;
    await firebase.deletePreset(presetId);
    await handleLoadFromCloud();
  }

  // Effect for keyboard shortcuts
  $effect(() => {
    if (browser) {
      const handleKeydown = (event: KeyboardEvent) => {
        if ((event.ctrlKey || event.metaKey) && event.key === 'e') {
          event.preventDefault();
          ui.toggleEditMode();
        }
        if (event.key === 'Escape') {
          ui.clearSelection();
        }
      };
      
      window.addEventListener('keydown', handleKeydown);
      return () => window.removeEventListener('keydown', handleKeydown);
    }
    return () => {};
  });
</script>

<header class="flex h-16 items-center justify-between gap-4 border-b bg-[var(--theme-surface)] px-4 shadow-sm">
  <div class="flex items-center gap-2">
    <Button variant="ghost" size="icon" onClick={ui.toggleLeftSidebar} title="Toggle Sensor Panel">
      <PanelLeft class="h-5 w-5" />
    </Button>
    <h1 class="text-lg font-semibold">Ultimate Sensor Monitor</h1>
  </div>

  <div class="flex items-center gap-2">
    <Button
      variant={ui.editMode === 'edit' ? 'primary' : 'outline'}
      onClick={ui.toggleEditMode}
      title="Toggle Edit Mode (Ctrl+E)"
    >
      {#if ui.editMode === 'edit'}
        <Pencil class="mr-2 h-4 w-4" />
        <span>Edit Mode</span>
      {:else}
        <Eye class="mr-2 h-4 w-4" />
        <span>View Mode</span>
      {/if}
    </Button>

    <div class="h-8 border-l border-[var(--theme-border)]"></div>
    
    <Button variant="ghost" size="icon" onClick={history.undo} disabled={!history.canUndo} title="Undo">
      <Undo class="h-5 w-5" />
    </Button>
    <Button variant="ghost" size="icon" onClick={history.redo} disabled={!history.canRedo} title="Redo">
      <Redo class="h-5 w-5" />
    </Button>
    
    <div class="h-8 border-l border-[var(--theme-border)]"></div>

    <Button variant="ghost" size="icon" onClick={visualUtils.toggleTheme} title="Toggle Theme">
      {#if visualSettings.theme === 'dark'}
        <Sun class="h-5 w-5" />
      {:else}
        <Moon class="h-5 w-5" />
      {/if}
    </Button>

    <div class="h-8 border-l border-[var(--theme-border)]"></div>

    <Dropdown position="bottom" align="end">
      <div slot="trigger">
        <Button variant="outline">
          File
        </Button>
      </div>
      <div class="w-56 p-2 flex flex-col gap-1 bg-[var(--theme-surface-overlay)] rounded-lg shadow-lg border-[var(--theme-border)]">
        <Button variant="ghost" onClick={handleImport}>
          <Upload class="mr-2 h-4 w-4" />
          Import from File
        </Button>
        <Button variant="ghost" onClick={handleExport}>
          <Download class="mr-2 h-4 w-4" />
          Export to File
        </Button>
      </div>
    </Dropdown>

    {#if firebase.isAuthenticated}
    <Dropdown position="bottom" align="end">
        <div 
          slot="trigger" 
          onmousedown={handleLoadFromCloud}
          role="button"
          tabindex="0"
          onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') handleLoadFromCloud(); }}
        >
            <Button variant="outline">
                <Cloud class="mr-2 h-4 w-4" />
                Cloud Presets
            </Button>
        </div>
        <div class="w-64 p-2 flex flex-col gap-1 bg-[var(--theme-surface-overlay)] rounded-lg shadow-lg border-[var(--theme-border)]">
            <Button variant="ghost" onClick={handleSaveToCloud}>
              <Save class="mr-2 h-4 w-4" />
              Save Current to Cloud
            </Button>
            <div class="my-1 h-px bg-[var(--theme-border)]"></div>
            <h3 class="px-2 py-1 text-sm font-semibold text-[var(--theme-text-muted)]">Your Presets</h3>
            {#if isLoadingPresets}
              <div class="flex items-center justify-center p-4">
                <Loader2 class="h-6 w-6 animate-spin text-[var(--theme-text-muted)]" />
              </div>
            {:else if presets.length === 0}
              <p class="px-2 py-1 text-sm text-[var(--theme-text-muted)]">No presets found.</p>
            {:else}
              {#each presets as preset (preset.id)}
                <div class="flex items-center justify-between rounded-md hover:bg-[var(--theme-surface-hover)]">
                  <Button variant="ghost" className="flex-grow justify-start text-left" onClick={() => applyPreset(preset)}>
                    {preset.name}
                  </Button>
                  <Button variant="ghost" size="icon" className="text-red-500 hover:bg-red-500/10" onClick={() => handleDeletePreset(preset.id)} title="Delete Preset">
                    <Trash2 class="h-4 w-4" />
                  </Button>
                </div>
              {/each}
            {/if}
        </div>
      </Dropdown>
    {/if}

    <div class="h-8 border-l border-[var(--theme-border)]"></div>

    {#if firebase.user}
      <Dropdown position="bottom" align="end">
        <div slot="trigger">
            <Button variant="ghost" size="icon">
                {#if firebase.user.photoURL}
                    <img src={firebase.user.photoURL} alt="User" class="h-8 w-8 rounded-full" />
                {:else}
                    <UserIcon class="h-5 w-5" />
                {/if}
            </Button>
        </div>
        <div class="w-48 p-2 flex flex-col gap-1 bg-[var(--theme-surface-overlay)] rounded-lg shadow-lg border-[var(--theme-border)]">
          <div class="px-2 py-1 text-sm text-center text-[var(--theme-text-muted)] border-b border-[var(--theme-border)] mb-1">
            {firebase.user.displayName || 'User'}
          </div>
          <Button variant="ghost" onClick={firebase.signOut}>
            <LogOut class="mr-2 h-4 w-4" />
            Sign Out
          </Button>
        </div>
      </Dropdown>
    {:else}
      <Button variant="outline" onClick={firebase.signInWithGoogle}>
        <LogIn class="mr-2 h-4 w-4" />
        Sign In
      </Button>
    {/if}
    
    <Button variant="ghost" size="icon" onClick={ui.toggleRightSidebar} title="Toggle Inspector Panel">
      <PanelRight class="h-5 w-5" />
    </Button>
  </div>
</header>

<style>
  /* Add any additional styling here */
</style>
