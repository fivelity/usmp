<script lang="ts">
  import { ui } from '$lib/stores/core/ui.svelte';
  import WidgetInspector from '../dashboard/WidgetInspector.svelte';
  import VisualDimensionsPanel from '../dashboard/VisualDimensionsPanel.svelte';
  import WidgetGroupManager from '../dashboard/WidgetGroupManager.svelte';

  let { onclose }: { onclose: () => void } = $props();

  let activeTab = $state<'inspector' | 'visual' | 'groups'>('inspector');

  // Auto-switch to inspector when widgets are selected
  $effect(() => {
    if (ui.selectedWidgetCount > 0) {
      activeTab = 'inspector';
    }
  });
</script>

<div class="h-full flex flex-col bg-(--theme-surface) border-l border-(--theme-border)">
  <!-- Header -->
  <div class="flex items-center justify-between p-4 border-b border-(--theme-border)">
    <h2 class="text-lg font-semibold text-(--theme-text)">Properties</h2>
    <button
      onclick={onclose}
      class="p-1 rounded hover:bg-(--theme-background) text-(--theme-text-muted) hover:text-(--theme-text)"
      title="Close Properties Panel" aria-label="Close Properties Panel"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>
  </div>

  <!-- Tab Navigation -->
  <div class="flex border-b border-(--theme-border)">
    <button
      class="flex-1 px-3 py-2 text-xs font-medium transition-colors"
      class:active={activeTab === 'inspector'}
      class:inactive={activeTab !== 'inspector'}
      onclick={() => activeTab = 'inspector'}
    >
      Inspector
    </button>
    <button
      class="flex-1 px-3 py-2 text-xs font-medium transition-colors"
      class:active={activeTab === 'visual'}
      class:inactive={activeTab !== 'visual'}
      onclick={() => activeTab = 'visual'}
    >
      Visual
    </button>
    <button
      class="flex-1 px-3 py-2 text-xs font-medium transition-colors"
      class:active={activeTab === 'groups'}
      class:inactive={activeTab !== 'groups'}
      onclick={() => activeTab = 'groups'}
    >
      Groups
    </button>
  </div>

  <!-- Tab Content -->
  <div class="flex-1 overflow-y-auto sidebar-content p-4">
    {#if activeTab === 'inspector'}
      <WidgetInspector />
    {:else if activeTab === 'visual'}
      <VisualDimensionsPanel />
    {:else if activeTab === 'groups'}
      <WidgetGroupManager />
    {/if}
  </div>
</div>

<style>
  .active {
    background-color: var(--theme-background);
    color: var(--theme-text);
    border-bottom: 2px solid var(--theme-primary, #3b82f6);
  }

  .inactive {
    background-color: transparent;
    color: var(--theme-text-muted);
  }

  .inactive:hover {
    background-color: var(--theme-background);
    color: var(--theme-text);
  }
</style>
