<!-- ChartContainer.svelte -->
<script lang="ts">
  import { fade } from 'svelte/transition';
  import LoadingState from '../../ui/common/LoadingState.svelte';

  let {
    title,
    loading = false,
    error = $bindable(null),
    height = '300px',
    showLegend = true,
    showTooltip = true,
    className = '',
    data = [],
    onRefresh,
    refreshInterval = undefined
  } = $props<{
    title: string;
    loading?: boolean;
    error?: string | null;
    height?: string;
    showLegend?: boolean;
    showTooltip?: boolean;
    className?: string;
    data?: any[];
    onRefresh?: () => void;
    refreshInterval?: number;
  }>();

  let refreshTimer: NodeJS.Timeout | undefined;

  $effect(() => {
    if (refreshInterval && onRefresh) {
      if (refreshTimer) clearInterval(refreshTimer);
      refreshTimer = setInterval(onRefresh, refreshInterval);
    }
    return () => {
      if (refreshTimer) clearInterval(refreshTimer);
    };
  });

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
>
  <div class="chart-header flex-between">
    <h3 class="text-heading">{title}</h3>
    {#if onRefresh}
      <button
        class="btn btn-secondary"
        onclick={handleRefresh}
        aria-label="Refresh chart data"
      >
        <i class="fas fa-sync-alt"></i>
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
        <i class="fas fa-exclamation-circle"></i>
        <span>{error}</span>
      </div>
      <button
        class="btn btn-secondary"
        onclick={handleErrorDismiss}
        aria-label="Dismiss error"
      >
        <i class="fas fa-times"></i>
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
    position: relative;
    display: flex;
    flex-direction: column;
    min-height: 200px;
  }

  .chart-header {
    margin-bottom: 1rem;
  }

  .chart-content {
    flex: 1;
    position: relative;
  }

  .chart-loading {
    position: absolute;
    inset: 0;
    background-color: rgba(156, 163, 175, 0.5);
    backdrop-filter: blur(4px);
  }

  .chart-error {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--color-error-100);
  }

  .error-message {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--color-error);
  }

  .chart-legend {
    margin-top: 1rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .chart-tooltip {
    position: absolute;
    pointer-events: none;
    background-color: var(--color-surface-elevated);
    border: 1px solid var(--color-border);
    border-radius: 0.375rem;
    padding: 0.5rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
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
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }

    .chart-legend {
      justify-content: flex-start;
    }
  }
</style> 