<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { sensorDataStore } from '$lib/stores/data/sensors';
  import type { WidgetConfig, SensorData } from '$lib/types';
  import * as d3 from 'd3';

  export let widget: WidgetConfig;
  export let sensorData: SensorData | undefined;

  let svgElement: SVGElement;
  let dataHistory: { timestamp: Date; value: number }[] = [];
  let unsubscribe: (() => void) | null = null;

  // Graph settings with defaults
  $: timeRange = widget.gauge_settings?.time_range || 60; // seconds
  $: lineColor = widget.gauge_settings?.line_color || '#3b82f6';
  $: fillArea = widget.gauge_settings?.fill_area || false;
  $: showPoints = widget.gauge_settings?.show_points || false;
  $: showGrid = widget.gauge_settings?.show_grid ?? true;
  $: animateEntry = widget.gauge_settings?.animate_entry ?? true;

  // Responsive dimensions
  $: width = widget.width - 32;
  $: height = widget.height - 64;
  $: sensorName = widget.custom_label || sensorData?.name || 'Unknown Sensor';
  $: unit = widget.custom_unit || sensorData?.unit || '';

  // Current value for display
  $: currentValue = typeof sensorData?.value === 'number' ? sensorData.value : null;
  $: formattedValue = currentValue !== null ? 
    (Number.isInteger(currentValue) ? currentValue.toString() : currentValue.toFixed(1)) : '--';

  function updateGraph() {
    if (!svgElement || dataHistory.length === 0 || width <= 0 || height <= 0) return;

    const svg = d3.select(svgElement);
    svg.selectAll('*').remove();

    const margin = { top: 10, right: 15, bottom: 25, left: 40 };
    const innerWidth = Math.max(width - margin.left - margin.right, 0);
    const innerHeight = Math.max(height - margin.top - margin.bottom, 0);

    if (innerWidth <= 0 || innerHeight <= 0) return;

    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Scales
    const xScale = d3.scaleTime()
      .domain(d3.extent(dataHistory, d => d.timestamp) as [Date, Date])
      .range([0, innerWidth]);

    const yExtent = d3.extent(dataHistory, d => d.value) as [number, number];
    const yPadding = (yExtent[1] - yExtent[0]) * 0.1 || 1;
    const yScale = d3.scaleLinear()
      .domain([yExtent[0] - yPadding, yExtent[1] + yPadding])
      .nice()
      .range([innerHeight, 0]);

    // Grid lines
    if (showGrid) {
      // Horizontal grid lines
      g.selectAll('.grid-line-y')
        .data(yScale.ticks(4))
        .enter().append('line')
        .attr('class', 'grid-line-y')
        .attr('x1', 0)
        .attr('x2', innerWidth)
        .attr('y1', d => yScale(d))
        .attr('y2', d => yScale(d))
        .style('stroke', '#e5e7eb')
        .style('stroke-width', 1)
        .style('opacity', 0.5);

      // Vertical grid lines
      g.selectAll('.grid-line-x')
        .data(xScale.ticks(4))
        .enter().append('line')
        .attr('class', 'grid-line-x')
        .attr('x1', d => xScale(d))
        .attr('x2', d => xScale(d))
        .attr('y1', 0)
        .attr('y2', innerHeight)
        .style('stroke', '#e5e7eb')
        .style('stroke-width', 1)
        .style('opacity', 0.5);
    }

    // Line and area generators
    const line = d3.line<{ timestamp: Date; value: number }>()
      .x(d => xScale(d.timestamp))
      .y(d => yScale(d.value))
      .curve(d3.curveMonotoneX);

    const area = d3.area<{ timestamp: Date; value: number }>()
      .x(d => xScale(d.timestamp))
      .y0(innerHeight)
      .y1(d => yScale(d.value))
      .curve(d3.curveMonotoneX);

    // Add fill area if enabled
    if (fillArea) {
      const areaPath = g.append('path')
        .datum(dataHistory)
        .attr('fill', lineColor)
        .attr('opacity', 0.2)
        .attr('d', area);

      if (animateEntry) {
        const totalLength = areaPath.node()?.getTotalLength() || 0;
        areaPath
          .attr('stroke-dasharray', totalLength + ' ' + totalLength)
          .attr('stroke-dashoffset', totalLength)
          .transition()
          .duration(1000)
          .ease(d3.easeLinear)
          .attr('stroke-dashoffset', 0);
      }
    }

    // Add the line
    const linePath = g.append('path')
      .datum(dataHistory)
      .attr('fill', 'none')
      .attr('stroke', lineColor)
      .attr('stroke-width', 2)
      .attr('d', line);

    if (animateEntry) {
      const totalLength = linePath.node()?.getTotalLength() || 0;
      linePath
        .attr('stroke-dasharray', totalLength + ' ' + totalLength)
        .attr('stroke-dashoffset', totalLength)
        .transition()
        .duration(1000)
        .ease(d3.easeLinear)
        .attr('stroke-dashoffset', 0);
    }

    // Add points if enabled
    if (showPoints) {
      const points = g.selectAll('.dot')
        .data(dataHistory)
        .enter().append('circle')
        .attr('class', 'dot')
        .attr('cx', d => xScale(d.timestamp))
        .attr('cy', d => yScale(d.value))
        .attr('r', 3)
        .attr('fill', lineColor)
        .attr('stroke', 'white')
        .attr('stroke-width', 1);

      if (animateEntry) {
        points
          .attr('r', 0)
          .transition()
          .duration(1000)
          .delay((d, i) => i * 50)
          .attr('r', 3);
      }
    }

    // Add axes
    g.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(xScale)
        .tickFormat(d3.timeFormat('%H:%M'))
        .ticks(4))
      .selectAll('text')
      .style('font-size', '11px')
      .style('fill', '#6b7280');

    g.append('g')
      .call(d3.axisLeft(yScale)
        .ticks(4))
      .selectAll('text')
      .style('font-size', '11px')
      .style('fill', '#6b7280');

    // Style axes
    g.selectAll('.domain, .tick line')
      .style('stroke', '#d1d5db');
  }

  onMount(() => {
    // Subscribe to sensor data updates
    if (widget.sensor_id) {
      unsubscribe = sensorDataStore.subscribe(widget.sensor_id, (data) => {
        if (data && typeof data.value === 'number') {
          const now = new Date();
          dataHistory.push({
            timestamp: now,
            value: data.value
          });

          // Remove old data points outside the time range
          const cutoffTime = new Date(now.getTime() - timeRange * 1000);
          dataHistory = dataHistory.filter(d => d.timestamp >= cutoffTime);

          // Limit data points for performance
          if (dataHistory.length > 200) {
            dataHistory = dataHistory.slice(-200);
          }

          updateGraph();
        }
      });
    }

    // Add initial data point if available
    if (currentValue !== null) {
      dataHistory.push({
        timestamp: new Date(),
        value: currentValue
      });
      updateGraph();
    }
  });

  onDestroy(() => {
    if (unsubscribe) {
      unsubscribe();
    }
  });

  // Update graph when widget size changes
  $: if (width > 0 && height > 0) {
    updateGraph();
  }
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
