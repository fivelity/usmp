<script lang="ts">
  import type { SensorReading } from '$lib/types/sensors';
  import { sidebarStore } from '$lib/stores/ui.svelte';
  import SensorItem from './SensorItem.svelte';

  let { category, sensors }: { category: string; sensors: SensorReading[] } = $props();

  const isExpanded = $derived(sidebarStore.expandedCategories.has(category));

  function toggle() {
    sidebarStore.toggleCategory(category);
  }

  // A simple mapping of category names to emojis.
  const categoryIcons: Record<string, string> = {
    temperature: '🌡️',
    usage: '📊',
    load: '⚡',
    power: '🔌',
    frequency: '💻',
    clock: '⏰',
    fan: '🌪️',
    voltage: '⚡',
    memory: '💾',
    throughput: '📈',
    default: '⚙️'
  };

  const icon = $derived(categoryIcons[category.toLowerCase()] || categoryIcons.default);

</script>

<div class="border-b border-(--theme-border)">
  <button
    class="w-full p-4 flex items-center gap-3 hover:bg-(--theme-background) transition-colors text-left"
    onclick={toggle}
  >
    <span class="transition-transform duration-200" class:rotate-90={isExpanded}>
      ▶
    </span>
    <span class="text-lg">{icon}</span>
    <h3 class="font-medium text-(--theme-text) capitalize flex-1">
      {category.replace(/_/g, ' ')}
    </h3>
    <span class="text-sm text-(--theme-text-muted)">
      ({sensors.length})
    </span>
  </button>

  {#if isExpanded}
    <div class="px-4 pb-4 space-y-2">
      {#each sensors as sensor (sensor.id)}
        <SensorItem {sensor} />
      {/each}
    </div>
  {/if}
</div> 