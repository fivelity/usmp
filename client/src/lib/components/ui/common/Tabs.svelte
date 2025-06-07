<!-- Tabs.svelte -->
<script lang="ts">
  import { fade } from 'svelte/transition';

  let {
    tabs = [],
    activeTab = $bindable(tabs[0]?.id),
    variant = 'line',
    className = '',
    onchange = undefined,
    children
  } = $props<{
    tabs?: { id: string; label: string; icon?: string }[];
    activeTab?: string;
    variant?: 'line' | 'pill';
    className?: string;
    onchange?: ((tabId: string) => void) | undefined;
    children?: any;
  }>();

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

  const variantClasses = $derived((() => {
    const classes = {
      line: 'border-b border-gray-200 dark:border-gray-700',
      pill: 'bg-gray-100 dark:bg-gray-800 p-1 rounded-lg'
    } as const;
    return classes[variant as keyof typeof classes];
  })());

  const tabClasses = $derived((() => {
    const classes = {
      line: 'border-b-2 border-transparent hover:border-blue-400',
      pill: 'rounded-md hover:bg-gray-200 dark:hover:bg-gray-700'
    } as const;
    return classes[variant as keyof typeof classes];
  })());

  const activeClasses = $derived((() => {
    const classes = {
      line: 'border-blue-500 text-blue-600',
      pill: 'bg-white dark:bg-gray-900 text-blue-600 dark:text-blue-400'
    } as const;
    return classes[variant as keyof typeof classes];
  })());
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
        onclick={() => handleTabClick(tab.id)}
        onkeydown={(e) => handleKeydown(e, tab.id)}
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
        {@render children()}
      {/if}
    </div>
  {/each}
</div> 