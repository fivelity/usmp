<!-- Tabs.svelte -->
<script lang="ts">
  import { fade } from 'svelte/transition';
  import { createEventDispatcher } from 'svelte';

  export let tabs: { id: string; label: string; icon?: string }[] = [];
  export let activeTab = tabs[0]?.id;
  export let variant: 'line' | 'pill' = 'line';
  export let className = '';

  const dispatch = createEventDispatcher<{
    change: { tabId: string };
  }>();

  function handleTabClick(tabId: string) {
    activeTab = tabId;
    dispatch('change', { tabId });
  }

  function handleKeydown(event: KeyboardEvent, tabId: string) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleTabClick(tabId);
    }
  }

  $: variantClasses = {
    line: 'border-b border-border',
    pill: 'bg-surface-elevated p-1 rounded-lg'
  }[variant];

  $: tabClasses = {
    line: 'border-b-2 border-transparent hover:border-primary/50',
    pill: 'rounded-md hover:bg-surface-hover'
  }[variant];

  $: activeClasses = {
    line: 'border-primary text-primary',
    pill: 'bg-surface text-primary'
  }[variant];
</script>

<div class="tabs {variantClasses} {className}">
  <div class="tabs-list" role="tablist">
    {#each tabs as tab}
      <button
        class="tab {tabClasses} {activeTab === tab.id ? activeClasses : ''}"
        role="tab"
        aria-selected={activeTab === tab.id}
        aria-controls="tabpanel-{tab.id}"
        tabindex={activeTab === tab.id ? 0 : -1}
        on:click={() => handleTabClick(tab.id)}
        on:keydown={(e) => handleKeydown(e, tab.id)}
      >
        {#if tab.icon}
          <i class="fas {tab.icon}" />
        {/if}
        <span>{tab.label}</span>
      </button>
    {/each}
  </div>

  {#each tabs as tab}
    <div
      class="tab-panel"
      role="tabpanel"
      id="tabpanel-{tab.id}"
      aria-labelledby="tab-{tab.id}"
      hidden={activeTab !== tab.id}
      transition:fade
    >
      {#if activeTab === tab.id}
        <slot name={tab.id} />
      {/if}
    </div>
  {/each}
</div>

<style>
  .tabs {
    @apply w-full;
  }

  .tabs-list {
    @apply flex gap-2;
  }

  .tab {
    @apply px-4 py-2 font-medium text-text-muted transition-colors;
  }

  .tab-panel {
    @apply mt-4;
  }

  /* Responsive adjustments */
  @media (max-width: 640px) {
    .tabs-list {
      @apply overflow-x-auto pb-2;
    }

    .tab {
      @apply whitespace-nowrap;
    }
  }
</style> 