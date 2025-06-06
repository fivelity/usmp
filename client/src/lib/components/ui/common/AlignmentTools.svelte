<script lang="ts">
  import { selectedWidgets } from '$lib/stores/core/ui';
  import { widgetUtils } from '$lib/stores/data/widgets';
  import { widgets } from '$lib/stores/data/widgets';
  import { Button } from './ui';

  // Alignment functions
  function alignLeft() {
    if ($selectedWidgets.type !== 'widget' || $selectedWidgets.ids.length < 2) return;
    
    const selectedWidgetConfigs = $selectedWidgets.ids.map(id => $widgets[id]).filter(Boolean);
    const leftmost = Math.min(...selectedWidgetConfigs.map(w => w.pos_x));
    
    selectedWidgetConfigs.forEach(widget => {
      widgetUtils.updateWidget(widget.id, { pos_x: leftmost });
    });
  }

  function alignRight() {
    if ($selectedWidgets.type !== 'widget' || $selectedWidgets.ids.length < 2) return;
    
    const selectedWidgetConfigs = $selectedWidgets.ids.map(id => $widgets[id]).filter(Boolean);
    const rightmost = Math.max(...selectedWidgetConfigs.map(w => w.pos_x + w.width));
    
    selectedWidgetConfigs.forEach(widget => {
      widgetUtils.updateWidget(widget.id, { pos_x: rightmost - widget.width });
    });
  }

  function alignTop() {
    if ($selectedWidgets.type !== 'widget' || $selectedWidgets.ids.length < 2) return;
    
    const selectedWidgetConfigs = $selectedWidgets.ids.map(id => $widgets[id]).filter(Boolean);
    const topmost = Math.min(...selectedWidgetConfigs.map(w => w.pos_y));
    
    selectedWidgetConfigs.forEach(widget => {
      widgetUtils.updateWidget(widget.id, { pos_y: topmost });
    });
  }

  function alignBottom() {
    if ($selectedWidgets.type !== 'widget' || $selectedWidgets.ids.length < 2) return;
    
    const selectedWidgetConfigs = $selectedWidgets.ids.map(id => $widgets[id]).filter(Boolean);
    const bottommost = Math.max(...selectedWidgetConfigs.map(w => w.pos_y + w.height));
    
    selectedWidgetConfigs.forEach(widget => {
      widgetUtils.updateWidget(widget.id, { pos_y: bottommost - widget.height });
    });
  }

  function alignCenterHorizontal() {
    if ($selectedWidgets.type !== 'widget' || $selectedWidgets.ids.length < 2) return;
    
    const selectedWidgetConfigs = $selectedWidgets.ids.map(id => $widgets[id]).filter(Boolean);
    const leftmost = Math.min(...selectedWidgetConfigs.map(w => w.pos_x));
    const rightmost = Math.max(...selectedWidgetConfigs.map(w => w.pos_x + w.width));
    const centerX = (leftmost + rightmost) / 2;
    
    selectedWidgetConfigs.forEach(widget => {
      widgetUtils.updateWidget(widget.id, { pos_x: centerX - widget.width / 2 });
    });
  }

  function alignCenterVertical() {
    if ($selectedWidgets.type !== 'widget' || $selectedWidgets.ids.length < 2) return;
    
    const selectedWidgetConfigs = $selectedWidgets.ids.map(id => $widgets[id]).filter(Boolean);
    const topmost = Math.min(...selectedWidgetConfigs.map(w => w.pos_y));
    const bottommost = Math.max(...selectedWidgetConfigs.map(w => w.pos_y + w.height));
    const centerY = (topmost + bottommost) / 2;
    
    selectedWidgetConfigs.forEach(widget => {
      widgetUtils.updateWidget(widget.id, { pos_y: centerY - widget.height / 2 });
    });
  }

  function distributeHorizontally() {
    if ($selectedWidgets.type !== 'widget' || $selectedWidgets.ids.length < 3) return;
    
    const selectedWidgetConfigs = $selectedWidgets.ids.map(id => $widgets[id]).filter(Boolean);
    selectedWidgetConfigs.sort((a, b) => a.pos_x - b.pos_x);
    
    const leftmost = selectedWidgetConfigs[0].pos_x;
    const rightmost = selectedWidgetConfigs[selectedWidgetConfigs.length - 1].pos_x + selectedWidgetConfigs[selectedWidgetConfigs.length - 1].width;
    const totalWidth = selectedWidgetConfigs.reduce((sum, w) => sum + w.width, 0);
    const spacing = (rightmost - leftmost - totalWidth) / (selectedWidgetConfigs.length - 1);
    
    let currentX = leftmost;
    selectedWidgetConfigs.forEach(widget => {
      widgetUtils.updateWidget(widget.id, { pos_x: currentX });
      currentX += widget.width + spacing;
    });
  }

  function distributeVertically() {
    if ($selectedWidgets.type !== 'widget' || $selectedWidgets.ids.length < 3) return;
    
    const selectedWidgetConfigs = $selectedWidgets.ids.map(id => $widgets[id]).filter(Boolean);
    selectedWidgetConfigs.sort((a, b) => a.pos_y - b.pos_y);
    
    const topmost = selectedWidgetConfigs[0].pos_y;
    const bottommost = selectedWidgetConfigs[selectedWidgetConfigs.length - 1].pos_y + selectedWidgetConfigs[selectedWidgetConfigs.length - 1].height;
    const totalHeight = selectedWidgetConfigs.reduce((sum, w) => sum + w.height, 0);
    const spacing = (bottommost - topmost - totalHeight) / (selectedWidgetConfigs.length - 1);
    
    let currentY = topmost;
    selectedWidgetConfigs.forEach(widget => {
      widgetUtils.updateWidget(widget.id, { pos_y: currentY });
      currentY += widget.height + spacing;
    });
  }

  function matchWidth() {
    if ($selectedWidgets.type !== 'widget' || $selectedWidgets.ids.length < 2) return;
    
    const selectedWidgetConfigs = $selectedWidgets.ids.map(id => $widgets[id]).filter(Boolean);
    const referenceWidth = selectedWidgetConfigs[0].width;
    
    selectedWidgetConfigs.slice(1).forEach(widget => {
      widgetUtils.updateWidget(widget.id, { width: referenceWidth });
    });
  }

  function matchHeight() {
    if ($selectedWidgets.type !== 'widget' || $selectedWidgets.ids.length < 2) return;
    
    const selectedWidgetConfigs = $selectedWidgets.ids.map(id => $widgets[id]).filter(Boolean);
    const referenceHeight = selectedWidgetConfigs[0].height;
    
    selectedWidgetConfigs.slice(1).forEach(widget => {
      widgetUtils.updateWidget(widget.id, { height: referenceHeight });
    });
  }

  function matchSize() {
    if ($selectedWidgets.type !== 'widget' || $selectedWidgets.ids.length < 2) return;
    
    const selectedWidgetConfigs = $selectedWidgets.ids.map(id => $widgets[id]).filter(Boolean);
    const reference = selectedWidgetConfigs[0];
    
    selectedWidgetConfigs.slice(1).forEach(widget => {
      widgetUtils.updateWidget(widget.id, { 
        width: reference.width,
        height: reference.height 
      });
    });
  }

  let hasSelection = $derived($selectedWidgets.type === 'widget' && $selectedWidgets.ids.length > 0);
  let hasMultipleSelection = $derived($selectedWidgets.type === 'widget' && $selectedWidgets.ids.length > 1);
  let hasDistributionSelection = $derived($selectedWidgets.type === 'widget' && $selectedWidgets.ids.length > 2);
</script>

<div class="alignment-tools">
  <div class="tool-section">
    <h4>Align</h4>
    <div class="tool-grid">
      <Button 
        variant="outline" 
        size="sm" 
        onclick={alignLeft}
        disabled={!hasMultipleSelection}
        title="Align Left"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8M4 18h16" />
        </svg>
      </Button>
      
      <Button 
        variant="outline" 
        size="sm" 
        onclick={alignCenterHorizontal}
        disabled={!hasMultipleSelection}
        title="Align Center Horizontal"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M8 12h8M4 18h16" />
        </svg>
      </Button>
      
      <Button 
        variant="outline" 
        size="sm" 
        onclick={alignRight}
        disabled={!hasMultipleSelection}
        title="Align Right"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M12 12h8M4 18h16" />
        </svg>
      </Button>
      
      <Button 
        variant="outline" 
        size="sm" 
        onclick={alignTop}
        disabled={!hasMultipleSelection}
        title="Align Top"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 2v20M2 12h20" />
        </svg>
      </Button>
      
      <Button 
        variant="outline" 
        size="sm" 
        onclick={alignCenterVertical}
        disabled={!hasMultipleSelection}
        title="Align Center Vertical"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 2v20M6 12h12" />
        </svg>
      </Button>
      
      <Button 
        variant="outline" 
        size="sm" 
        onclick={alignBottom}
        disabled={!hasMultipleSelection}
        title="Align Bottom"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 2v20M2 12h20" />
        </svg>
      </Button>
    </div>
  </div>

  <div class="tool-section">
    <h4>Distribute</h4>
    <div class="tool-row">
      <Button 
        variant="outline" 
        size="sm" 
        onclick={distributeHorizontally}
        disabled={!hasDistributionSelection}
        title="Distribute Horizontally"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l4-4 4 4m0 6l-4 4-4-4" />
        </svg>
        Horizontal
      </Button>
      
      <Button 
        variant="outline" 
        size="sm" 
        onclick={distributeVertically}
        disabled={!hasDistributionSelection}
        title="Distribute Vertically"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 8l-4-4-4 4m0 8l4 4 4-4" />
        </svg>
        Vertical
      </Button>
    </div>
  </div>

  <div class="tool-section">
    <h4>Match Size</h4>
    <div class="tool-row">
      <Button 
        variant="outline" 
        size="sm" 
        onclick={matchWidth}
        disabled={!hasMultipleSelection}
        title="Match Width"
      >
        Width
      </Button>
      
      <Button 
        variant="outline" 
        size="sm" 
        onclick={matchHeight}
        disabled={!hasMultipleSelection}
        title="Match Height"
      >
        Height
      </Button>
      
      <Button 
        variant="outline" 
        size="sm" 
        onclick={matchSize}
        disabled={!hasMultipleSelection}
        title="Match Size"
      >
        Both
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

  .tool-section h4 {
    margin: 0 0 0.75rem 0;
    font-size: 0.875rem;
    font-weight: 600;
    color: #374151;
  }

  .tool-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
  }

  .tool-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .tool-row :global(.btn) {
    flex: 1;
    min-width: 0;
  }
</style>
