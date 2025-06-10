<script lang="ts">
  import { sidebarStore } from '$lib/stores/ui.svelte';
</script>

<div class="p-4">
  <input
    type="text"
    value={sidebarStore.searchTerm}
    oninput={(e) => sidebarStore.setSearchTerm(e.currentTarget.value)}
    placeholder="Search sensors..."
    class="w-full px-3 py-2 text-sm bg-[var(--theme-background)] border border-[var(--theme-border)] rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--theme-primary)] transition-colors"
  />
</div> 