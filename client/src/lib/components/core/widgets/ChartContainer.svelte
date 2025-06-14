<!-- ChartContainer.svelte -->
<script lang="ts">
  import { fade } from 'svelte/transition';
  import LoadingState from '../../ui/common/LoadingState.svelte';
  import type { SensorData } from '$lib/types/sensor';

  export let title: string;
  export let loading = false;
  export let error: string | null = null;
  export let height = '300px';
  export let showLegend = true;
  export let showTooltip = true;
  export let className = '';
  export let data: SensorData[] = [];
  export let onRefresh: (() => void) | undefined = undefined;
  export let refreshInterval: number | undefined = undefined;

  let chartContainer: HTMLDivElement;
  let refreshTimer: NodeJS.Timeout | undefined;

  $: if (refreshInterval && onRefresh) {
    if (refreshTimer) clearInterval(refreshTimer);
    refreshTimer = setInterval(onRefresh, refreshInterval);
  }

  function handleRefresh() {
    if (onRefresh) {
      onRefresh();
    }
  }

  function handleErrorDismiss() {
    error = null;
  }
</script>

<div
  class="chart-container component-base {className}"
  style="height: {height}"
  bind:this={chartContainer}
>
  <div class="chart-header flex-between">
    <h3 class="text-heading">{title}</h3>
    {#if onRefresh}
      <button
        class="btn btn-secondary"
        on:click={handleRefresh}
        aria-label="Refresh chart data"
      >
        <i class="fas fa-sync-alt" />
      </button>
    {/if}
  </div>

  {#if loading}
    <div class="chart-loading flex-center" transition:fade>
      <LoadingState variant="spinner" size="lg" />
    </div>
  {:else if error}
    <div class="chart-error" transition:fade>
      <div class="error-message">
        <i class="fas fa-exclamation-circle" />
        <span>{error}</span>
      </div>
      <button
        class="btn btn-secondary"
        on:click={handleErrorDismiss}
        aria-label="Dismiss error"
      >
        <i class="fas fa-times" />
      </button>
    </div>
  {:else}
    <div class="chart-content" transition:fade>
      <slot {data} />
    </div>
  {/if}

  {#if showLegend}
    <div class="chart-legend">
      <slot name="legend" />
    </div>
  {/if}

  {#if showTooltip}
    <div class="chart-tooltip" role="tooltip">
      <slot name="tooltip" />
    </div>
  {/if}
</div>

<style>
  .chart-container {
    @apply relative flex flex-col;
    min-height: 200px;
  }

  .chart-header {
    @apply mb-4;
  }

  .chart-content {
    @apply flex-1 relative;
  }

  .chart-loading {
    @apply absolute inset-0 bg-surface/50 backdrop-blur-sm;
  }

  .chart-error {
    @apply absolute inset-0 flex items-center justify-center bg-error/10;
  }

  .error-message {
    @apply flex items-center gap-2 text-error;
  }

  .chart-legend {
    @apply mt-4 flex flex-wrap gap-2;
  }

  .chart-tooltip {
    @apply absolute pointer-events-none bg-surface-elevated border border-border rounded-md p-2 shadow-lg;
    transform: translate(-50%, -100%);
    opacity: 0;
    transition: opacity var(--transition-normal);
  }

  .chart-tooltip:not(:empty) {
    opacity: 1;
  }

  /* Responsive adjustments */
  @media (max-width: 640px) {
    .chart-header {
      @apply flex-col items-start gap-2;
    }

    .chart-legend {
      @apply justify-start;
    }
  }
</style> 