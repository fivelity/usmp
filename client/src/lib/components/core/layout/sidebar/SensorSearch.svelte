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
    class="w-full px-3 py-2 text-sm bg-(--theme-background) border border-(--theme-border) rounded-lg focus:outline-none focus:ring-2 focus:ring-(--theme-primary) transition-colors"
  />
</div>
