<!-- Tabs.svelte -->
<script lang="ts">
  import { fade } from 'svelte/transition';

  export let tabs: { id: string; label: string; icon?: string }[] = [];
  export let activeTab = tabs[0]?.id;
  export let variant: 'line' | 'pill' = 'line';
  export let className = '';
  export let onchange: ((tabId: string) => void) | undefined = undefined;

  function handleTabClick(tabId: string) {
    activeTab = tabId;
    onchange?.(tabId);
  }

  function handleKeydown(event: KeyboardEvent, tabId: string) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleTabClick(tabId);
    }
  }

  $: variantClasses = {
    line: 'border-b border-gray-200 dark:border-gray-700',
    pill: 'bg-gray-100 dark:bg-gray-800 p-1 rounded-lg'
  }[variant];

  $: tabClasses = {
    line: 'border-b-2 border-transparent hover:border-blue-400',
    pill: 'rounded-md hover:bg-gray-200 dark:hover:bg-gray-700'
  }[variant];

  $: activeClasses = {
    line: 'border-blue-500 text-blue-600',
    pill: 'bg-white dark:bg-gray-900 text-blue-600 dark:text-blue-400'
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
          <i class="fas {tab.icon}"></i>
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
        <slot />
      {/if}
    </div>
  {/each}
</div> 