<!-- DataTable.svelte -->
<script lang="ts">
  import { fade } from 'svelte/transition';
  import LoadingState from '../../ui/common/LoadingState.svelte';
  import type { SensorData } from '$lib/types';

  let {
    data = [],
    loading = false,
    error = null,
    pageSize = 10,
    sortable = true,
    filterable = true,
    className = ''
  } = $props();

  let currentPage = $state(1);
  let sortColumn = $state<keyof SensorData | null>(null);
  let sortDirection = $state<'asc' | 'desc'>('asc');
  let filterValue = $state('');

  let filteredData = $derived((data as any[]).filter((item: any) => {
    if (!filterValue) return true;
    const searchStr = Object.values(item).join(' ').toLowerCase();
    return searchStr.includes(filterValue.toLowerCase());
  }));

  let sortedData = $derived(sortColumn
    ? [...filteredData].sort((a, b) => {
        const aVal = a[sortColumn!];
        const bVal = b[sortColumn!];
        const modifier = sortDirection === 'asc' ? 1 : -1;
        
        if (aVal == null && bVal == null) return 0;
        if (aVal == null) return -1 * modifier;
        if (bVal == null) return 1 * modifier;
        
        return aVal < bVal ? -1 * modifier : aVal > bVal ? 1 * modifier : 0;
      })
    : filteredData);

  let paginatedData = $derived(sortedData.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize
  ));

  let totalPages = $derived(Math.ceil(filteredData.length / pageSize));

  function handleSort(column: keyof SensorData) {
    if (!sortable) return;
    if (sortColumn === column) {
      sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      sortColumn = column;
      sortDirection = 'asc';
    }
  }

  function handleFilter(event: Event) {
    const target = event.target as HTMLInputElement;
    filterValue = target.value;
    currentPage = 1;
  }

  function handlePageChange(page: number) {
    currentPage = page;
  }
</script>

<div class="data-table component-base {className}">
  {#if filterable}
    <div class="table-filter">
      <input
        type="text"
        placeholder="Filter data..."
        value={filterValue}
        oninput={handleFilter}
        class="input-base"
      />
    </div>
  {/if}

  {#if loading}
    <div class="table-loading flex-center" transition:fade>
      <LoadingState variant="spinner" size="lg" />
    </div>
  {:else if error}
    <div class="table-error" transition:fade>
      <div class="error-message">
        <i class="fas fa-exclamation-circle"></i>
        <span>{error}</span>
      </div>
    </div>
  {:else}
    <div class="table-container custom-scrollbar">
      <table>
        <thead>
          <tr>
            {#each Object.keys((data as any[])[0] || {}) as column}
              <th
                class:sortable
                onclick={() => handleSort(column as keyof SensorData)}
              >
                {column}
                {#if sortColumn === column}
                  <i
                    class="fas fa-sort-{sortDirection === 'asc' ? 'up' : 'down'}"
                  ></i>
                {/if}
              </th>
            {/each}
          </tr>
        </thead>
        <tbody>
          {#each paginatedData as row}
            <tr>
              {#each Object.values(row) as cell}
                <td>{cell}</td>
              {/each}
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    {#if totalPages > 1}
      <div class="table-pagination">
        <button
          class="btn btn-secondary"
          disabled={currentPage === 1}
          onclick={() => handlePageChange(currentPage - 1)}
          aria-label="Previous page"
        >
          <i class="fas fa-chevron-left"></i>
        </button>
        <span class="page-info">
          Page {currentPage} of {totalPages}
        </span>
        <button
          class="btn btn-secondary"
          disabled={currentPage === totalPages}
          onclick={() => handlePageChange(currentPage + 1)}
          aria-label="Next page"
        >
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    {/if}
  {/if}
</div>

<style>
  .data-table {
    @apply flex flex-col gap-4;
  }

  .table-filter {
    @apply mb-4;
  }

  .table-container {
    @apply overflow-x-auto;
    max-height: 500px;
  }

  table {
    @apply w-full border-collapse;
  }

  th,
  td {
    @apply px-4 py-2 text-left border-b border-border;
  }

  th {
    @apply bg-surface-elevated font-medium sticky top-0;
  }

  th.sortable {
    @apply cursor-pointer hover:bg-surface-hover;
  }

  tbody tr {
    @apply hover:bg-surface-hover transition-colors;
  }

  .table-loading {
    @apply absolute inset-0 bg-gray-100 bg-opacity-50 backdrop-blur-sm;
  }

  .table-error {
    @apply p-4 bg-error-100 text-error-700 rounded-md;
  }

  .error-message {
    @apply flex items-center gap-2;
  }

  .table-pagination {
    @apply flex items-center justify-center gap-4 mt-4;
  }

  .page-info {
    @apply text-text-muted;
  }

  /* Responsive adjustments */
  @media (max-width: 640px) {
    .table-container {
      max-height: 300px;
    }

    th,
    td {
      @apply px-2 py-1 text-sm;
    }
  }
</style> 