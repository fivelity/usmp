<script lang="ts">
  import { sensors } from '$lib/stores/data/sensors.svelte';
  import type { SensorReading } from '$lib/types/sensors';

  import SidebarHeader from './sidebar/SidebarHeader.svelte';
  import SensorSearch from './sidebar/SensorSearch.svelte';
  import SensorCategory from './sidebar/SensorCategory.svelte';
  import LoadingSpinner from '$lib/components/ui/common/LoadingSpinner.svelte';

  let { onclose }: { onclose: () => void } = $props();
  let searchTerm = $state('');

  // By extracting the rune here, we ensure consistent usage within the derived computations.
  const available = sensors.available;

  const filteredSensors = $derived(() => {
    if (!searchTerm) return available;
    const lowerCaseSearch = searchTerm.toLowerCase();
    return available.filter(
      (sensor: SensorReading) =>
        sensor.name.toLowerCase().includes(lowerCaseSearch) ||
        sensor.id.toLowerCase().includes(lowerCaseSearch)
    );
  });

  const sensorsByCategory = $derived(() => {
    return filteredSensors.reduce(
      (acc: Record<string, SensorReading[]>, sensor: SensorReading) => {
        const categoryKey = sensor.category || 'Other';
        if (!acc[categoryKey]) {
          acc[categoryKey] = [];
        }
        acc[categoryKey].push(sensor);
        return acc;
      },
      {} as Record<string, SensorReading[]>
    );
  });

  const categories = $derived(Object.entries(sensorsByCategory));
</script>

<div class="sidebar-content h-full flex flex-col bg-(--theme-surface) text-(--theme-text)">
  <SidebarHeader {onclose} />
  <SensorSearch bind:searchTerm />

  <div class="flex-1 overflow-y-auto">
    {#if sensors.available.length === 0}
      <div class="flex flex-col items-center justify-center h-full p-8 text-center text-(--theme-text-muted)">
        <LoadingSpinner />
        <p class="mt-4">Loading sensors...</p>
      </div>
    {:else if categories.length === 0}
      <div class="p-8 text-center text-(--theme-text-muted)">
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