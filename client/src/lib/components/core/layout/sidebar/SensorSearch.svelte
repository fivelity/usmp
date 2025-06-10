<script lang="ts">
  import { sidebarSearchTerm } from '$lib/stores/ui.svelte';

  let searchTerm = $state('');

  $effect(() => {
    sidebarSearchTerm.set(searchTerm);
  });
</script>

<div class="p-2">
  <input
    type="text"
    bind:value={searchTerm}
    placeholder="Search sensors..."
    class="w-full px-3 py-2 text-sm bg-[var(--theme-background)] border border-[var(--theme-border)] rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--theme-primary)] transition-colors"
  />
</div> 