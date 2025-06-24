<script lang="ts">
  import { run } from 'svelte/legacy';
  import { visualSettings } from '$lib/stores/core/visual.svelte';
  import { getEditMode } from '$lib/stores/core/ui.svelte';
  import { onMount } from 'svelte';

  interface Props {
    canvasWidth?: number;
    canvasHeight?: number;
  }

  let { canvasWidth = 1920, canvasHeight = 1080 }: Props = $props();

  let gridCanvas = $state<HTMLCanvasElement>();
  let ctx = $state<CanvasRenderingContext2D>();

  function getGridStyle(size: number) {
    if (size <= 5) return 'dots';
    if (size <= 10) return 'fine-lines';
    if (size <= 20) return 'lines';
    return 'bold-lines';
  }

  function drawGrid() {
    if (!ctx || !showGrid) return;

    ctx.clearRect(0, 0, canvasWidth, canvasHeight);
    
    // Set grid appearance based on theme and style
    const isDark = document.documentElement.classList.contains('dark');
    const baseColor = isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
    const accentColor = isDark ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.2)';

    switch (gridStyle) {
      case 'dots':
        drawDotGrid(baseColor);
        break;
      case 'fine-lines':
        drawLineGrid(baseColor, 0.5);
        break;
      case 'lines':
        drawLineGrid(baseColor, 1);
        break;
      case 'bold-lines':
        drawLineGrid(baseColor, 1);
        drawMajorGrid(accentColor);
        break;
    }
  }

  function drawDotGrid(color: string) {
    if (!ctx) return;
    ctx.fillStyle = color;
    for (let x = 0; x <= canvasWidth; x += gridSize) {
      for (let y = 0; y <= canvasHeight; y += gridSize) {
        ctx.beginPath();
        ctx.arc(x, y, 0.5, 0, 2 * Math.PI);
        ctx.fill();
      }
    }
  }

  function drawLineGrid(color: string, lineWidth: number) {
    if (!ctx) return;
    ctx.strokeStyle = color;
    ctx.lineWidth = lineWidth;
    ctx.beginPath();

    // Vertical lines
    for (let x = 0; x <= canvasWidth; x += gridSize) {
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvasHeight);
    }

    // Horizontal lines
    for (let y = 0; y <= canvasHeight; y += gridSize) {
      ctx.moveTo(0, y);
      ctx.lineTo(canvasWidth, y);
    }

    ctx.stroke();
  }

  function drawMajorGrid(color: string) {
    if (!ctx) return;
    const majorGridSize = gridSize * 5;
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.beginPath();

    // Major vertical lines
    for (let x = 0; x <= canvasWidth; x += majorGridSize) {
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvasHeight);
    }

    // Major horizontal lines
    for (let y = 0; y <= canvasHeight; y += majorGridSize) {
      ctx.moveTo(0, y);
      ctx.lineTo(canvasWidth, y);
    }

    ctx.stroke();
  }

  // Snap position to grid
  export function snapToGridPosition(x: number, y: number): { x: number; y: number } {
    if (!snapToGrid) return { x, y };
    
    return {
      x: Math.round(x / gridSize) * gridSize,
      y: Math.round(y / gridSize) * gridSize
    };
  }

  // Snap size to grid
  export function snapToGridSize(width: number, height: number): { width: number; height: number } {
    if (!snapToGrid) return { width, height };
    
    return {
      width: Math.max(gridSize, Math.round(width / gridSize) * gridSize),
      height: Math.max(gridSize, Math.round(height / gridSize) * gridSize)
    };
  }

  onMount(() => {
    if (gridCanvas) {
      ctx = gridCanvas.getContext('2d')!;
      drawGrid();
    }
  });

  // Grid configuration
  let gridSize = $derived(visualSettings.grid_size);
  let showGrid = $derived(visualSettings.show_grid && getEditMode() === 'edit');
  let snapToGrid = $derived(visualSettings.snap_to_grid);
  // Grid styles based on size
  let gridStyle = $derived(getGridStyle(gridSize));
  // Redraw when settings change
  run(() => {
    if (ctx) {
      drawGrid();
    }
  });
</script>

{#if showGrid}
  <canvas
    bind:this={gridCanvas}
    width={canvasWidth}
    height={canvasHeight}
    class="grid-canvas absolute inset-0 pointer-events-none"
    style="z-index: 1;"
  ></canvas>
{/if}

<style>
  .grid-canvas {
    image-rendering: pixelated;
    image-rendering: -moz-crisp-edges;
    image-rendering: crisp-edges;
  }
</style> 