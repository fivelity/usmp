<script lang="ts">
  import { availableSensors as availableSensorsStore } from '$lib/stores/sensorData.svelte';
  import { sidebarStore } from '$lib/stores/ui.svelte';
  import type { SensorReading } from '$lib/types/sensors';

  import SidebarHeader from './sidebar/SidebarHeader.svelte';
  import SensorSearch from './sidebar/SensorSearch.svelte';
  import SensorCategory from './sidebar/SensorCategory.svelte';
  import LoadingSpinner from '$lib/components/ui/common/LoadingSpinner.svelte';

  interface Props {
    onclose?: () => void;
  }

  let { onclose }: Props = $props();

  // Get reactive values from stores
  const searchTerm = $derived(sidebarStore.searchTerm);
  const availableSensors = $derived(availableSensorsStore);

  // Derived state for filtered and categorized sensors
  const sensorsByCategory = $derived.by(() => {
    if (!availableSensors) return {};

    const filtered = availableSensors.filter((sensor: SensorReading) =>
      sensor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      sensor.id.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return filtered.reduce((acc: Record<string, SensorReading[]>, sensor: SensorReading) => {
      const categoryKey = sensor.category || 'Other';
      if (!acc[categoryKey]) {
        acc[categoryKey] = [];
      }
      acc[categoryKey].push(sensor);
      return acc;
    }, {});
  });

  const categories = $derived(Object.entries(sensorsByCategory));
</script>

<div class="sidebar-content h-full flex flex-col bg-[var(--theme-surface)] text-[var(--theme-text)]">
  <SidebarHeader {onclose} />
  <SensorSearch />

  <div class="flex-1 overflow-y-auto">
    {#if availableSensors === undefined}
      <div class="flex flex-col items-center justify-center h-full p-8 text-center text-[var(--theme-text-muted)]">
        <LoadingSpinner />
        <p class="mt-4">Loading sensors...</p>
      </div>
    {:else if categories.length === 0}
      <div class="p-8 text-center text-[var(--theme-text-muted)]">
        <div class="text-5xl mb-4 opacity-50">🤷</div>
        <p>No sensors found</p>
        {#if searchTerm}
          <p class="text-sm mt-2">Try adjusting your search.</p>
        {:else}
          <p class="text-sm mt-2">Check connection to the server.</p>
        {/if}
      </div>
    {:else}
      {#each categories as [category, sensorList] (category)}
        <SensorCategory category={category} sensors={sensorList} />
      {/each}
    {/if}
  </div>
</div> 