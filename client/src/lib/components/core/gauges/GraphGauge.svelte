<script lang="ts">
  import { sensorDataManager } from '$lib/stores/sensorData.svelte';
  import type { WidgetConfig, SensorReading } from '$lib/types'; 
  import * as d3 from 'd3';
  import { get } from 'svelte/store';

  let { widget } = $props<{ widget: WidgetConfig }>();

  let svgElement: SVGElement;
  let dataHistory = $state<{ timestamp: Date; value: number }[]>([]);

  // Graph settings with defaults
  const timeRange = $derived(widget.gauge_settings?.time_range || 60);
  const lineColor = $derived(widget.gauge_settings?.line_color || '#3b82f6');
  const fillArea = $derived(widget.gauge_settings?.fill_area || false);
  const showPoints = $derived(widget.gauge_settings?.show_points || false);
  const showGrid = $derived(widget.gauge_settings?.show_grid ?? true);
  const animateEntry = $derived(widget.gauge_settings?.animate_entry ?? true);

  // Derived state for the specific sensor reading this gauge is interested in
  // $derived will subscribe to sensorDataManager.sensorDataStore and give us its value
  const _allSensorDataMap: Record<string, SensorReading> = $derived(get(sensorDataManager.sensorDataStore));
  const currentSensorReading = $derived(
    widget.sensor_id ? _allSensorDataMap[widget.sensor_id] : undefined
  );

  // Responsive dimensions
  const width = $derived(widget.width - 32);
  const height = $derived(widget.height - 64);

  // Updated derived states using currentSensorReading
  const sensorName = $derived(widget.custom_label || currentSensorReading?.name || 'Unknown Sensor');
  const unit = $derived(widget.custom_unit || currentSensorReading?.unit || '');
  const currentValue = $derived(typeof currentSensorReading?.value === 'number' ? currentSensorReading.value : null);
  const formattedValue = $derived(currentValue !== null ? 
    (Number.isInteger(currentValue) ? currentValue.toString() : currentValue.toFixed(1)) : '--');

  // Effect to update dataHistory when currentSensorReading changes
  $effect(() => {
    if (currentSensorReading && typeof currentSensorReading.value === 'number') {
      const now = new Date();
      const newPoint = { timestamp: now, value: currentSensorReading.value };
      
      // Create new array for $state update, add new point, then filter and slice
      let updatedHistory = [...dataHistory, newPoint];

      const cutoffTime = new Date(now.getTime() - timeRange * 1000);
      updatedHistory = updatedHistory.filter(d => d.timestamp >= cutoffTime);

      if (updatedHistory.length > 200) {
        updatedHistory = updatedHistory.slice(-200);
      }
      dataHistory = updatedHistory; // Assign to $state variable
    }
  });
  
  function updateGraph() {
    // Read dataHistory reactively here if needed, or ensure it's passed if it's not a closure
    const currentDataHistory = dataHistory; // Ensure we are using the reactive value
    if (!svgElement || currentDataHistory.length === 0 || width <= 0 || height <= 0) {
        // If graph should be cleared when dataHistory is empty
        if (svgElement && currentDataHistory.length === 0) {
            const svgClear = d3.select(svgElement);
            svgClear.selectAll('*').remove();
        }
        return;
    }

    const svg = d3.select(svgElement);
    svg.selectAll('*').remove(); // Clear previous graph elements

    const margin = { top: 10, right: 15, bottom: 25, left: 40 };
    const innerWidth = Math.max(width - margin.left - margin.right, 0);
    const innerHeight = Math.max(height - margin.top - margin.bottom, 0);

    if (innerWidth <= 0 || innerHeight <= 0) return;

    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const xScale = d3.scaleTime()
      .domain(d3.extent(currentDataHistory, d => d.timestamp) as [Date, Date])
      .range([0, innerWidth]);

    const yExtent = d3.extent(currentDataHistory, d => d.value) as [number, number];
    const yPadding = (yExtent[1] - yExtent[0]) * 0.1 || 1; // Add small padding or 1 if flat
    const yScale = d3.scaleLinear()
      .domain([yExtent[0] - yPadding, yExtent[1] + yPadding])
      .nice()
      .range([innerHeight, 0]);

    if (showGrid) {
      g.selectAll('.grid-line-y')
        .data(yScale.ticks(4))
        .enter().append('line')
        .attr('class', 'grid-line-y')
        .attr('x1', 0).attr('x2', innerWidth)
        .attr('y1', d => yScale(d)).attr('y2', d => yScale(d))
        .style('stroke', '#e5e7eb').style('stroke-width', 1).style('opacity', 0.5);

      g.selectAll('.grid-line-x')
        .data(xScale.ticks(4))
        .enter().append('line')
        .attr('class', 'grid-line-x')
        .attr('x1', d => xScale(d)).attr('x2', d => xScale(d))
        .attr('y1', 0).attr('y2', innerHeight)
        .style('stroke', '#e5e7eb').style('stroke-width', 1).style('opacity', 0.5);
    }

    const line = d3.line<{ timestamp: Date; value: number }>()
      .x(d => xScale(d.timestamp))
      .y(d => yScale(d.value))
      .curve(d3.curveMonotoneX);

    const area = d3.area<{ timestamp: Date; value: number }>()
      .x(d => xScale(d.timestamp))
      .y0(innerHeight)
      .y1(d => yScale(d.value))
      .curve(d3.curveMonotoneX);

    if (fillArea) {
      const areaPath = g.append('path').datum(currentDataHistory)
        .attr('fill', lineColor).attr('opacity', 0.2).attr('d', area);
      if (animateEntry) {
        const totalLength = areaPath.node()?.getTotalLength() || 0;
        areaPath.attr('stroke-dasharray', `${totalLength} ${totalLength}`)
          .attr('stroke-dashoffset', totalLength)
          .transition().duration(1000).ease(d3.easeLinear).attr('stroke-dashoffset', 0);
      }
    }

    const linePath = g.append('path').datum(currentDataHistory)
      .attr('fill', 'none').attr('stroke', lineColor).attr('stroke-width', 2).attr('d', line);
    if (animateEntry) {
      const totalLength = linePath.node()?.getTotalLength() || 0;
      linePath.attr('stroke-dasharray', `${totalLength} ${totalLength}`)
        .attr('stroke-dashoffset', totalLength)
        .transition().duration(1000).ease(d3.easeLinear).attr('stroke-dashoffset', 0);
    }

    if (showPoints) {
      const points = g.selectAll('.dot').data(currentDataHistory).enter().append('circle')
        .attr('class', 'dot')
        .attr('cx', d => xScale(d.timestamp)).attr('cy', d => yScale(d.value))
        .attr('r', 3).attr('fill', lineColor).attr('stroke', 'white').attr('stroke-width', 1);
      if (animateEntry) {
        points.attr('r', 0).transition().duration(1000).delay((_d, i) => i * 50).attr('r', 3);
      }
    }

    g.append('g').attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom<Date>(xScale).tickFormat(d3.timeFormat('%H:%M')).ticks(4))
      .selectAll('text').style('font-size', '11px').style('fill', '#6b7280');

    g.append('g').call(d3.axisLeft(yScale).ticks(4))
      .selectAll('text').style('font-size', '11px').style('fill', '#6b7280');

    g.selectAll('.domain, .tick line').style('stroke', '#d1d5db');
  }

  // Effect to update graph when dataHistory, width, or height change
  $effect(() => {
    // Reading dataHistory, width, height makes this effect dependent on them.
    if (width > 0 && height > 0) { // width and height are reactive from widget props
      updateGraph(); 
    }
  });
</script>

<div class="gauge-container">
  <!-- Header with current value -->
  <div class="flex justify-between items-center mb-3">
    {#if widget.show_label}
      <div class="text-sm font-medium text-gray-700 truncate flex-1">
        {sensorName}
      </div>
    {/if}
    <div class="text-right">
      <div class="text-lg font-bold text-gray-900">
        {formattedValue}
        {#if widget.show_unit && unit}
          <span class="text-sm text-gray-500 font-normal">{unit}</span>
        {/if}
      </div>
      <div class="text-xs text-gray-500">
        {dataHistory.length} points
      </div>
    </div>
  </div>

  <!-- SVG Graph -->
  <div class="graph-area bg-white rounded-lg border border-gray-200 p-2">
    <svg 
      bind:this={svgElement}
      {width}
      {height}
      viewBox="0 0 {width} {height}"
      class="block w-full h-full"
    ></svg>
  </div>

  <!-- Time range indicator -->
  <div class="text-center text-xs text-gray-500 mt-2">
    Last {timeRange}s
  </div>
</div>

<style>
  .gauge-container {
    width: 100%;
    height: 100%;
    padding: 16px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    display: flex;
    flex-direction: column;
  }

  .graph-area {
    flex: 1;
    min-height: 0;
  }
</style>
