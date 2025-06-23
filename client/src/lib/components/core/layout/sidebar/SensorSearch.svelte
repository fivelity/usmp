<script lang="ts">
  let { searchTerm = $bindable('') } = $props<{
    searchTerm?: string;
  }>();
</script>

<div class="p-4">
  <input
    type="text"
    bind:value={searchTerm}
    placeholder="Search sensors..."
    class="w-full px-3 py-2 text-sm bg-[var(--theme-background)] border border-[var(--theme-border)] rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--theme-primary)] transition-colors"
  />
</div>
