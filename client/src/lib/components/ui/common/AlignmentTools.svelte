<script lang="ts">
  import { selectedWidgets } from '$lib/stores/core/ui.svelte';
  import { widgetUtils } from '$lib/stores/data/widgets';
  import { widgets } from '$lib/stores/data/widgets';
  import { Button } from '../index';
  import type { Widget } from '$lib/types';

  // Store subscriptions at the top level
  let hasMultipleSelection = $derived($selectedWidgets.size > 1);
  let hasDistributionSelection = $derived($selectedWidgets.size > 2);

  // Helper function to get selected widgets
  function getSelectedWidgets(): Widget[] {
    const selectedIds = Array.from($selectedWidgets);
    return selectedIds
      .map(id => $widgets[id])
      .filter((w): w is Widget => Boolean(w));
  }

  // Alignment functions
  function alignLeft() {
    if (!hasMultipleSelection) return;
    
    const selectedWidgets = getSelectedWidgets();
    if (selectedWidgets.length < 2) return;
    
    const leftmost = Math.min(...selectedWidgets.map(w => w.x));
    selectedWidgets.forEach(widget => {
      widgetUtils.updateWidget(widget.id, { pos_x: leftmost });
    });
  }

  function alignRight() {
    if (!hasMultipleSelection) return;
    
    const selectedWidgets = getSelectedWidgets();
    if (selectedWidgets.length < 2) return;
    
    const rightmost = Math.max(...selectedWidgets.map(w => w.x + w.width));
    selectedWidgets.forEach(widget => {
      widgetUtils.updateWidget(widget.id, { pos_x: rightmost - widget.width });
    });
  }

  function alignTop() {
    if (!hasMultipleSelection) return;
    
    const selectedWidgets = getSelectedWidgets();
    if (selectedWidgets.length < 2) return;
    
    const topmost = Math.min(...selectedWidgets.map(w => w.y));
    selectedWidgets.forEach(widget => {
      widgetUtils.updateWidget(widget.id, { pos_y: topmost });
    });
  }

  function alignBottom() {
    if (!hasMultipleSelection) return;
    
    const selectedWidgets = getSelectedWidgets();
    if (selectedWidgets.length < 2) return;
    
    const bottommost = Math.max(...selectedWidgets.map(w => w.y + w.height));
    selectedWidgets.forEach(widget => {
      widgetUtils.updateWidget(widget.id, { pos_y: bottommost - widget.height });
    });
  }

  function alignCenterHorizontal() {
    if (!hasMultipleSelection) return;
    
    const selectedWidgets = getSelectedWidgets();
    if (selectedWidgets.length < 2) return;
    
    const leftmost = Math.min(...selectedWidgets.map(w => w.x));
    const rightmost = Math.max(...selectedWidgets.map(w => w.x + w.width));
    const centerX = (leftmost + rightmost) / 2;
    
    selectedWidgets.forEach(widget => {
      widgetUtils.updateWidget(widget.id, { pos_x: centerX - widget.width / 2 });
    });
  }

  function alignCenterVertical() {
    if (!hasMultipleSelection) return;
    
    const selectedWidgets = getSelectedWidgets();
    if (selectedWidgets.length < 2) return;
    
    const topmost = Math.min(...selectedWidgets.map(w => w.y));
    const bottommost = Math.max(...selectedWidgets.map(w => w.y + w.height));
    const centerY = (topmost + bottommost) / 2;
    
    selectedWidgets.forEach(widget => {
      widgetUtils.updateWidget(widget.id, { pos_y: centerY - widget.height / 2 });
    });
  }

  function distributeHorizontally() {
    if (!hasDistributionSelection) return;
    
    const selectedWidgets = getSelectedWidgets();
    if (selectedWidgets.length < 3) return;
    
    selectedWidgets.sort((a, b) => a.x - b.x);
    const firstWidget = selectedWidgets[0];
    const lastWidget = selectedWidgets[selectedWidgets.length - 1];
    
    if (!firstWidget || !lastWidget) return;
    
    const leftmost = firstWidget.x;
    const rightmost = lastWidget.x + lastWidget.width;
    const totalWidth = selectedWidgets.reduce((sum, w) => sum + w.width, 0);
    const spacing = selectedWidgets.length > 1 ? (rightmost - leftmost - totalWidth) / (selectedWidgets.length - 1) : 0;
    
    let currentX = leftmost;
    selectedWidgets.forEach(widget => {
      widgetUtils.updateWidget(widget.id, { pos_x: currentX });
      currentX += widget.width + spacing;
    });
  }

  function distributeVertically() {
    if (!hasDistributionSelection) return;
    
    const selectedWidgets = getSelectedWidgets();
    if (selectedWidgets.length < 3) return;
    
    selectedWidgets.sort((a, b) => a.y - b.y);
    const firstWidget = selectedWidgets[0];
    const lastWidget = selectedWidgets[selectedWidgets.length - 1];
    
    if (!firstWidget || !lastWidget) return;
    
    const topmost = firstWidget.y;
    const bottommost = lastWidget.y + lastWidget.height;
    const totalHeight = selectedWidgets.reduce((sum, w) => sum + w.height, 0);
    const spacing = selectedWidgets.length > 1 ? (bottommost - topmost - totalHeight) / (selectedWidgets.length - 1) : 0;
    
    let currentY = topmost;
    selectedWidgets.forEach(widget => {
      widgetUtils.updateWidget(widget.id, { pos_y: currentY });
      currentY += widget.height + spacing;
    });
  }

  function matchWidth() {
    if (!hasMultipleSelection) return;
    
    const selectedWidgets = getSelectedWidgets();
    if (selectedWidgets.length < 1) return;
    
    const referenceWidget = selectedWidgets[0];
    if (!referenceWidget) return;
    
    selectedWidgets.slice(1).forEach(widget => {
      widgetUtils.updateWidget(widget.id, { width: referenceWidget.width });
    });
  }

  function matchHeight() {
    if (!hasMultipleSelection) return;
    
    const selectedWidgets = getSelectedWidgets();
    if (selectedWidgets.length < 1) return;
    
    const referenceWidget = selectedWidgets[0];
    if (!referenceWidget) return;
    
    selectedWidgets.slice(1).forEach(widget => {
      widgetUtils.updateWidget(widget.id, { height: referenceWidget.height });
    });
  }

  function matchSize() {
    if (!hasMultipleSelection) return;
    
    const selectedWidgets = getSelectedWidgets();
    if (selectedWidgets.length < 1) return;
    
    const referenceWidget = selectedWidgets[0];
    if (!referenceWidget) return;
    
    selectedWidgets.slice(1).forEach(widget => {
      widgetUtils.updateWidget(widget.id, { 
        width: referenceWidget.width,
        height: referenceWidget.height 
      });
    });
  }
</script>

<div class="alignment-tools">
  <div class="flex flex-col gap-2 p-2">
    <div class="flex gap-2">
      <Button
        variant="ghost"
        size="sm"
        leftIcon="M4 6h16M4 12h16M4 18h16"
        disabled={!hasMultipleSelection}
        onClick={alignLeft}
      >
        Align Left
      </Button>
      <Button
        variant="ghost"
        size="sm"
        leftIcon="M4 6h16M4 12h16M4 18h16"
        disabled={!hasMultipleSelection}
        onClick={alignCenterHorizontal}
      >
        Center
      </Button>
      <Button
        variant="ghost"
        size="sm"
        leftIcon="M4 6h16M4 12h16M4 18h16"
        disabled={!hasMultipleSelection}
        onClick={alignRight}
      >
        Align Right
      </Button>
    </div>
    <div class="flex gap-2">
      <Button
        variant="ghost"
        size="sm"
        leftIcon="M4 6h16M4 12h16M4 18h16"
        disabled={!hasMultipleSelection}
        onClick={alignTop}
      >
        Align Top
      </Button>
      <Button
        variant="ghost"
        size="sm"
        leftIcon="M4 6h16M4 12h16M4 18h16"
        disabled={!hasMultipleSelection}
        onClick={alignCenterVertical}
      >
        Center
      </Button>
      <Button
        variant="ghost"
        size="sm"
        leftIcon="M4 6h16M4 12h16M4 18h16"
        disabled={!hasMultipleSelection}
        onClick={alignBottom}
      >
        Align Bottom
      </Button>
    </div>
    <div class="flex gap-2">
      <Button
        variant="ghost"
        size="sm"
        leftIcon="M4 6h16M4 12h16M4 18h16"
        disabled={!hasDistributionSelection}
        onClick={distributeHorizontally}
      >
        Distribute Horizontally
      </Button>
      <Button
        variant="ghost"
        size="sm"
        leftIcon="M4 6h16M4 12h16M4 18h16"
        disabled={!hasDistributionSelection}
        onClick={distributeVertically}
      >
        Distribute Vertically
      </Button>
    </div>
    <div class="flex gap-2">
      <Button
        variant="ghost"
        size="sm"
        leftIcon="M4 6h16M4 12h16M4 18h16"
        disabled={!hasMultipleSelection}
        onClick={matchWidth}
      >
        Match Width
      </Button>
      <Button
        variant="ghost"
        size="sm"
        leftIcon="M4 6h16M4 12h16M4 18h16"
        disabled={!hasMultipleSelection}
        onClick={matchHeight}
      >
        Match Height
      </Button>
      <Button
        variant="ghost"
        size="sm"
        leftIcon="M4 6h16M4 12h16M4 18h16"
        disabled={!hasMultipleSelection}
        onClick={matchSize}
      >
        Match Size
      </Button>
    </div>
  </div>
</div>

<style>
  .alignment-tools {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
    background: white;
    border-radius: 0.75rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  }

  /* Removed unused CSS selectors */
</style>
