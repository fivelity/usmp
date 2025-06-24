<script lang="ts">
  interface Props {
    onclose?: () => void;
  }

  let { onclose }: Props = $props();
</script>

<div class="flex items-center justify-between p-4 border-b border-(--theme-border)">
  <h2 class="font-semibold text-(--theme-text)">Sensors</h2>
  <button
    class="p-1 rounded hover:bg-(--theme-border) transition-colors"
    onclick={() => onclose?.()}
    title="Close panel"
  >
    ✕
  </button>
</div> 