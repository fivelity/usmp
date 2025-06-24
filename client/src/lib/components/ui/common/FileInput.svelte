<script lang="ts">
  import type { BaseComponentProps } from '$lib/types';
  import Button from './Button.svelte';

  interface Props extends BaseComponentProps {
    accept?: string;
    multiple?: boolean;
    disabled?: boolean;
    size?: 'sm' | 'md' | 'lg';
    variant?: 'primary' | 'secondary' | 'ghost';
    onchange?: (event: Event) => void;
  }

  let {
    accept = '*',
    multiple = false,
    disabled = false,
    size = 'md',
    variant = 'primary',
    class: className = '',
    onchange
  }: Props = $props();

  let fileInput = $state<HTMLInputElement | null>(null);
  let dragActive = $state(false);

  function handleFileSelect(event: Event) {
    if (onchange) {
      onchange(event);
    }
  }

  function handleDrop(event: DragEvent) {
    event.preventDefault();
    dragActive = false;
    
    if (event.dataTransfer?.files && fileInput) {
      fileInput.files = event.dataTransfer.files;
      handleFileSelect(new Event('change', { bubbles: true }));
    }
  }

  function handleDragOver(event: DragEvent) {
    event.preventDefault();
    dragActive = true;
  }

  function handleDragLeave(event: DragEvent) {
    event.preventDefault();
    dragActive = false;
  }

  function triggerFileInput() {
    fileInput?.click();
  }
</script>

<div
  class="file-input-container {className}"
  class:drag-active={dragActive}
  class:disabled
  role="button"
  tabindex="0"
  ondrop={handleDrop}
  ondragover={handleDragOver}
  ondragleave={handleDragLeave}
  onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); triggerFileInput(); } }}
>
  <input
    bind:this={fileInput}
    type="file"
    {accept}
    {multiple}
    {disabled}
    class="hidden"
    onchange={handleFileSelect}
  />
  
  <Button
    {size}
    {variant}
    {disabled}
    onClick={triggerFileInput}
  >
    <slot>Choose Files</slot>
  </Button>
</div>

<style>
  .file-input-container {
    position: relative;
    display: inline-block;
  }

  .file-input-container.drag-active {
    background-color: rgba(59, 130, 246, 0.1);
    border: 2px dashed #3b82f6;
  }

  .file-input-container.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style> 