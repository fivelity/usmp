<script lang="ts">
  import { browser } from '$app/environment';
  import { uiState } from '$lib/stores/uiState.svelte';
  import TopBar from '$lib/components/core/layout/TopBar.svelte';
  import LeftSidebar from '$lib/components/core/layout/LeftSidebar.svelte';
  import RightSidebar from '$lib/components/core/layout/RightSidebar.svelte';
  import DashboardCanvas from '$lib/components/core/dashboard/DashboardCanvas.svelte';
  import SplashScreen from '$lib/components/core/layout/SplashScreen.svelte';

  // Control loading state
  let isLoading = $state(true);

  // Simulate initialization
  if (browser) {
    setTimeout(() => {
      isLoading = false;
    }, 1500);
  } else {
    isLoading = false;
  }
</script>

<svelte:head>
  <title>Ultimate Sensor Monitor</title>
</svelte:head>

{#if isLoading}
  <SplashScreen />
{/if}

<div class="flex h-screen w-full flex-col">
  <TopBar />
  <div class="flex flex-1 overflow-hidden">
    {#if uiState.leftSidebarVisible}
      <aside class="w-80 h-full overflow-y-auto border-r border-[var(--theme-border)] bg-[var(--theme-surface)]">
        <LeftSidebar onclose={() => uiState.toggleLeftSidebar()} />
      </aside>
    {/if}

    <main class="flex-1 overflow-auto">
      <DashboardCanvas />
    </main>

    {#if uiState.rightSidebarVisible}
      <aside class="w-96 h-full overflow-y-auto border-l border-[var(--theme-border)] bg-[var(--theme-surface)]">
        <RightSidebar onclose={() => uiState.toggleRightSidebar()} />
      </aside>
    {/if}
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    overflow: hidden;
  }
</style>
