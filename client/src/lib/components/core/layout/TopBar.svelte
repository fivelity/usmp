<script lang="ts">
  import { browser } from '$app/environment';
  import { historyStore, type HistoryState } from '$lib/stores/history';
  import { uiState } from '$lib/stores/uiState.svelte';
  import { storeUtils } from '$lib/stores';

  import Button from '$lib/components/ui/common/Button.svelte';
  import Dropdown from '$lib/components/ui/common/Dropdown.svelte';
  import { PanelLeft, PanelRight, Pencil, Eye, Undo, Redo, Download, Upload, Save } from 'lucide-svelte';

  const history: HistoryState = $derived(historyStore);
  const canUndo = $derived(history.currentIndex > -1);
  const canRedo = $derived(history.currentIndex < history.commands.length - 1);

  function handleExport() {
    // Placeholder for export logic
    console.log('Exporting preset...');
  }

  function handleImport() {
    // Placeholder for import logic
    console.log('Importing preset...');
  }

  // Effect for keyboard shortcuts
  $effect(() => {
    if (browser) {
      const handleKeydown = (event: KeyboardEvent) => {
        if ((event.ctrlKey || event.metaKey) && event.key === 'e') {
          event.preventDefault();
          uiState.toggleEditMode();
        }
        if (event.key === 'Escape') {
          storeUtils.clearSelection();
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
    <Button variant="ghost" size="icon" onClick={uiState.toggleLeftSidebar} title="Toggle Sensor Panel">
      <PanelLeft class="h-5 w-5" />
    </Button>
    <h1 class="text-lg font-semibold">Ultimate Sensor Monitor</h1>
  </div>

  <div class="flex items-center gap-2">
    <Button
      variant={uiState.editMode === 'edit' ? 'primary' : 'outline'}
      onClick={uiState.toggleEditMode}
      title="Toggle Edit Mode (Ctrl+E)"
    >
      {#if uiState.editMode === 'edit'}
        <Pencil class="mr-2 h-4 w-4" />
        <span>Edit Mode</span>
      {:else}
        <Eye class="mr-2 h-4 w-4" />
        <span>View Mode</span>
      {/if}
    </Button>

    <div class="h-8 border-l border-[var(--theme-border)]"></div>
    
    <Button variant="ghost" size="icon" onClick={() => historyStore.undo()} disabled={!canUndo} title="Undo">
      <Undo class="h-5 w-5" />
    </Button>
    <Button variant="ghost" size="icon" onClick={() => historyStore.redo()} disabled={!canRedo} title="Redo">
      <Redo class="h-5 w-5" />
    </Button>
    
    <div class="h-8 border-l border-[var(--theme-border)]"></div>

    <Dropdown position="bottom" align="end">
      <div slot="trigger">
        <Button variant="outline">
          File
        </Button>
      </div>
      <div class="w-48 p-2 flex flex-col gap-1 bg-[var(--theme-surface-overlay)] rounded-lg shadow-lg border-[var(--theme-border)]">
        <Button variant="ghost" onClick={handleImport}>
          <Upload class="mr-2 h-4 w-4" />
          Import Preset
        </Button>
        <Button variant="ghost" onClick={handleExport}>
          <Download class="mr-2 h-4 w-4" />
          Export Preset
        </Button>
        <Button variant="ghost" onClick={() => {}}>
          <Save class="mr-2 h-4 w-4" />
          Save to Cloud
        </Button>
      </div>
    </Dropdown>
    
    <Button variant="ghost" size="icon" onClick={uiState.toggleRightSidebar} title="Toggle Inspector Panel">
      <PanelRight class="h-5 w-5" />
    </Button>
  </div>
</header>

<style>
  /* Add any additional styling here */
</style>
