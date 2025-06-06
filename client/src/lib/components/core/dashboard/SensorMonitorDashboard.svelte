<script lang="ts">
  import { onMount, onDestroy } from 'svelte'
  import { sensorService } from '$lib/services/sensorService'
  import SensorConfiguration from '../../ui/modals/SensorConfiguration.svelte'
  import { Button, LoadingSpinner } from '../../ui'
  import type { SensorReading } from '$lib/types/sensors'

  // State management using Svelte 5 runes
  let showConfiguration = $state(false)
  let isLoading = $state(true)
  let error = $state<string | null>(null)
  
  // Sensor data state
  let sensorData = $state<Record<string, SensorReading>>({})
  let connectionStatus = $state({ status: 'disconnected' })
  
  // Group sensors by category for display
  let sensorsByCategory = $derived(() => {
    const categories: Record<string, SensorReading[]> = {}
    
    Object.values(sensorData).forEach(sensor => {
      const category = sensor.category || 'uncategorized'
      if (!categories[category]) {
        categories[category] = []
      }
      categories[category].push(sensor)
    })
    
    return categories
  })

  onMount(async () => {
    try {
      await sensorService.initializeService()
      isLoading = false
    } catch (err) {
      error = err instanceof Error ? err.message : 'Failed to initialize sensor service'
      isLoading = false
    }
  })

  onDestroy(() => {
    sensorService.destroy()
  })

  function formatValue(value: number, unit: string): string {
    if (typeof value !== 'number') return 'N/A'
    
    // Format based on unit type
    if (unit === '°C' || unit === '°F') {
      return `${value.toFixed(1)}${unit}`
    } else if (unit === '%') {
      return `${value.toFixed(0)}${unit}`
    } else if (unit === 'MHz' || unit === 'RPM') {
      return `${value.toFixed(0)} ${unit}`
    } else if (unit === 'V') {
      return `${value.toFixed(2)} ${unit}`
    } else if (unit === 'W') {
      return `${value.toFixed(1)} ${unit}`
    } else {
      return `${value.toFixed(2)} ${unit}`
    }
  }

  function getStatusColor(status: string): string {
    switch (status) {
      case 'connected': return 'text-green-600'
      case 'connecting': return 'text-yellow-600'
      case 'disconnected': return 'text-gray-600'
      case 'error': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  function getCategoryIcon(category: string): string {
    switch (category) {
      case 'temperature': return '🌡️'
      case 'voltage': return '⚡'
      case 'clock': return '⏱️'
      case 'load': return '📊'
      case 'fan': return '🌀'
      case 'power': return '🔋'
      case 'memory': return '💾'
      default: return '📈'
    }
  }

  function getCategoryColor(category: string): string {
    switch (category) {
      case 'temperature': return 'border-red-200 bg-red-50'
      case 'voltage': return 'border-yellow-200 bg-yellow-50'
      case 'clock': return 'border-blue-200 bg-blue-50'
      case 'load': return 'border-green-200 bg-green-50'
      case 'fan': return 'border-purple-200 bg-purple-50'
      case 'power': return 'border-orange-200 bg-orange-50'
      default: return 'border-gray-200 bg-gray-50'
    }
  }

  function handleRefresh() {
    sensorService.refreshSensorData()
  }

  function handleConfigure() {
    showConfiguration = true
  }

  function handleRetry() {
    window.location.reload()
  }

  function handleCloseModal() {
    showConfiguration = false
  }

  function handleModalKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      showConfiguration = false
    }
  }

  function handleModalClick(event: MouseEvent) {
    event.stopPropagation()
  }
</script>

<div class="sensor-dashboard" role="main">
  <!-- Header -->
  <div class="dashboard-header">
    <div class="header-info">
      <h1>Sensor Monitor Dashboard</h1>
      <div class="connection-info">
        <span class={`connection-status ${getStatusColor(connectionStatus.status)}`}>
          ● {connectionStatus.status}
        </span>
        <span class="sensor-count">
          {Object.keys(sensorData).length} sensors active
        </span>
      </div>
    </div>
    
    <div class="header-actions">
      <Button 
        variant="outline" 
        onClick={handleRefresh}
        disabled={connectionStatus.status !== 'connected'}
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        Refresh
      </Button>
      
      <Button onClick={handleConfigure}>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        Configure
      </Button>
    </div>
  </div>

  <!-- Loading State -->
  {#if isLoading}
    <div class="loading-container">
      <LoadingSpinner size="lg" />
      <p>Initializing sensor monitoring...</p>
    </div>
  
  <!-- Error State -->
  {:else if error}
    <div class="error-container">
      <div class="error-icon">⚠️</div>
      <h3>Sensor Initialization Failed</h3>
      <p>{error}</p>
      <Button onClick={handleRetry}>
        Retry
      </Button>
    </div>
  
  <!-- Main Content -->
  {:else}
    <div class="dashboard-content">
      {#if Object.keys(sensorsByCategory).length === 0}
        <div class="empty-state">
          <div class="empty-icon">📊</div>
          <h3>No Sensor Data Available</h3>
          <p>Check your sensor configuration and connection status.</p>
          <Button onClick={handleConfigure}>
            Open Configuration
          </Button>
        </div>
      {:else}
        <div class="sensor-categories">
          {#each Object.entries(sensorsByCategory) as [category, sensors]}
            <div class={`category-section ${getCategoryColor(category)}`}>
              <div class="category-header">
                <span class="category-icon">{getCategoryIcon(category)}</span>
                <h3 class="category-title">{category.charAt(0).toUpperCase() + category.slice(1)}</h3>
                <span class="sensor-count-badge">{sensors.length}</span>
              </div>
              
              <div class="sensors-grid">
                {#each sensors as sensor}
                  <div class="sensor-card">
                    <div class="sensor-header">
                      <div class="sensor-name" title={sensor.name}>
                        {sensor.name}
                      </div>
                      <div class="sensor-source">
                        {sensor.source}
                      </div>
                    </div>
                    
                    <div class="sensor-value">
                      {formatValue(sensor.value, sensor.unit)}
                    </div>
                    
                    {#if sensor.min_value !== undefined && sensor.max_value !== undefined}
                      <div class="sensor-range">
                        <div class="range-bar">
                          <div 
                            class="range-fill"
                            style="width: {((sensor.value - sensor.min_value) / (sensor.max_value - sensor.min_value)) * 100}%"
                          ></div>
                        </div>
                        <div class="range-labels">
                          <span>{formatValue(sensor.min_value, sensor.unit)}</span>
                          <span>{formatValue(sensor.max_value, sensor.unit)}</span>
                        </div>
                      </div>
                    {/if}
                    
                    <div class="sensor-meta">
                      <span class="hardware-type">{sensor.hardware_type}</span>
                      <span class="quality-indicator quality-{sensor.quality}">
                        {sensor.quality}
                      </span>
                    </div>
                  </div>
                {/each}
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  {/if}

  <!-- Configuration Modal -->
  {#if showConfiguration}
    <div 
      class="modal-overlay" 
      role="button" 
      tabindex="0" 
      aria-label="Close configuration modal" 
      onkeydown={handleModalKeydown}
      onclick={handleCloseModal}
    >
      <div 
        class="modal-content" 
        role="dialog" 
        aria-modal="true" 
        aria-labelledby="configuration-modal-title" 
        onclick={handleModalClick}
      >
        <SensorConfiguration />
        <div class="modal-footer">
          <Button variant="outline" onClick={handleCloseModal}>
            Close
          </Button>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .sensor-dashboard {
    min-height: 100vh;
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    padding: 1.5rem;
  }

  .dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    background: white;
    padding: 1.5rem;
    border-radius: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  }

  .header-info h1 {
    margin: 0 0 0.5rem 0;
    font-size: 1.75rem;
    font-weight: 700;
    color: #1e293b;
  }

  .connection-info {
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 0.875rem;
  }

  .connection-status {
    font-weight: 600;
  }

  .sensor-count {
    color: #64748b;
  }

  .header-actions {
    display: flex;
    gap: 0.75rem;
  }

  .loading-container,
  .error-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    text-align: center;
    background: white;
    border-radius: 1rem;
    padding: 3rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  }

  .error-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
  }

  .error-container h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #dc2626;
  }

  .error-container p {
    margin: 0 0 1.5rem 0;
    color: #64748b;
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    text-align: center;
    background: white;
    border-radius: 1rem;
    padding: 3rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  }

  .empty-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    opacity: 0.5;
  }

  .empty-state h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #374151;
  }

  .empty-state p {
    margin: 0 0 1.5rem 0;
    color: #64748b;
  }

  .sensor-categories {
    display: grid;
    gap: 2rem;
  }

  .category-section {
    background: white;
    border-radius: 1rem;
    padding: 1.5rem;
    border: 2px solid;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  }

  .category-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  }

  .category-icon {
    font-size: 1.5rem;
  }

  .category-title {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #1e293b;
    flex: 1;
  }

  .sensor-count-badge {
    background: rgba(0, 0, 0, 0.1);
    color: #374151;
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.75rem;
    font-weight: 600;
  }

  .sensors-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1rem;
  }

  .sensor-card {
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 0.75rem;
    padding: 1rem;
    transition: all 0.2s ease;
  }

  .sensor-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  }

  .sensor-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.75rem;
  }

  .sensor-name {
    font-weight: 600;
    color: #1e293b;
    font-size: 0.875rem;
    line-height: 1.2;
    max-width: 70%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .sensor-source {
    font-size: 0.75rem;
    color: #64748b;
    background: #f1f5f9;
    padding: 0.125rem 0.5rem;
    border-radius: 0.375rem;
  }

  .sensor-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 0.75rem;
  }

  .sensor-range {
    margin-bottom: 0.75rem;
  }

  .range-bar {
    height: 4px;
    background: rgba(0, 0, 0, 0.1);
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 0.25rem;
  }

  .range-fill {
    height: 100%;
    background: linear-gradient(90deg, #10b981, #3b82f6, #f59e0b, #ef4444);
    border-radius: 2px;
    transition: width 0.3s ease;
  }

  .range-labels {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: #64748b;
  }

  .sensor-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.75rem;
  }

  .hardware-type {
    color: #64748b;
    text-transform: capitalize;
  }

  .quality-indicator {
    padding: 0.125rem 0.5rem;
    border-radius: 0.375rem;
    font-weight: 500;
    text-transform: capitalize;
  }

  .quality-excellent {
    background: #dcfce7;
    color: #166534;
  }

  .quality-good {
    background: #dbeafe;
    color: #1d4ed8;
  }

  .quality-fair {
    background: #fef3c7;
    color: #92400e;
  }

  .quality-poor {
    background: #fee2e2;
    color: #dc2626;
  }

  .quality-unknown {
    background: #f1f5f9;
    color: #64748b;
  }

  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 1rem;
  }

  .modal-content {
    background: white;
    border-radius: 1rem;
    max-width: 800px;
    width: 100%;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
  }

  .modal-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid #e2e8f0;
    display: flex;
    justify-content: flex-end;
  }

  @media (max-width: 768px) {
    .sensor-dashboard {
      padding: 1rem;
    }

    .dashboard-header {
      flex-direction: column;
      gap: 1rem;
      align-items: stretch;
    }

    .header-actions {
      justify-content: center;
    }

    .sensors-grid {
      grid-template-columns: 1fr;
    }

    .modal-content {
      margin: 0;
      border-radius: 0;
      max-height: 100vh;
    }
  }
</style>
