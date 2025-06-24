<script lang="ts">
  import { browser } from '$app/environment';
  import { ui } from '$lib/stores/core/ui.svelte';
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
    {#if ui.leftSidebarVisible}
      <aside class="w-80 h-full overflow-y-auto border-r border-(--theme-border) bg-(--theme-surface)">
        <LeftSidebar onclose={() => ui.toggleLeftSidebar()} />
      </aside>
    {/if}

    <main class="flex-1 overflow-auto">
      <DashboardCanvas />
    </main>

    {#if ui.rightSidebarVisible}
      <aside class="w-96 h-full overflow-y-auto border-l border-(--theme-border) bg-(--theme-surface)">
        <RightSidebar onclose={() => ui.toggleRightSidebar()} />
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
