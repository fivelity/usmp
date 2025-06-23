<script lang="ts">
  import { sensorService, sensorSources, sensorConnectionStatus, sensorPerformanceMetrics } from '$lib/services/sensorService'
  import { Button, RangeSlider, ToggleSwitch, Modal } from '../index';
  import type { SensorSource } from '$lib/types/sensors'
  import { writable } from 'svelte/store'

  let showConfigModal = writable(false)
  let config = writable(sensorService.getConfiguration())
  let selectedSource = writable<SensorSource | null>(null)
  let showSourceConfig = writable(false)

  const sources = $derived(sensorSources)
  const connectionStatus = $derived(sensorConnectionStatus)
  const performanceMetrics = $derived(sensorPerformanceMetrics)

  async function updateConfiguration() {
    try {
      await sensorService.updateConfiguration($config)
      $showConfigModal = false
    } catch (error) {
      console.error('Failed to update configuration:', error)
    }
  }

  async function refreshSensors() {
    try {
      await sensorService.refreshSensorData()
    } catch (error) {
      console.error('Failed to refresh sensors:', error)
    }
  }

  async function toggleSource(source: SensorSource) {
    try {
      await sensorService.toggleSensorSource(source.id, !source.active)
    } catch (error) {
      console.error('Failed to toggle source:', error)
    }
  }

  function openSourceConfig(source: SensorSource) {
    $selectedSource = source
    $showSourceConfig = true
  }

  async function updateSourceConfig() {
    if (!$selectedSource) return
    
    try {
      // Implementation would depend on specific source configuration options
      $showSourceConfig = false
      $selectedSource = null
    } catch (error) {
      console.error('Failed to update source configuration:', error)
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

  function getStatusIcon(status: string): string {
    switch (status) {
      case 'connected': return '●'
      case 'connecting': return '◐'
      case 'disconnected': return '○'
      case 'error': return '✕'
      default: return '?'
    }
  }
</script>

<div class="sensor-config-container">
  <!-- Header -->
  <div class="config-header">
    <div class="header-info">
      <h2>Sensor Configuration</h2>
      <div class="connection-status">
        <span class={`status-indicator ${getStatusColor($connectionStatus.status)}`}>
          {getStatusIcon($connectionStatus.status)}
        </span>
        <span class="status-text">{$connectionStatus.status}</span>
      </div>
    </div>
    
    <div class="header-actions">
      <Button variant="outline" onclick={refreshSensors}>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        Refresh
      </Button>
      
      <Button onclick={() => $showConfigModal = true}>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        Configure
      </Button>
    </div>
  </div>

  <!-- Performance Metrics -->
  <div class="metrics-section">
    <h3>Performance Metrics</h3>
    <div class="metrics-grid">
      <div class="metric-card">
        <div class="metric-label">Update Latency</div>
        <div class="metric-value">{$performanceMetrics.update_latency}ms</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Queue Size</div>
        <div class="metric-value">{$performanceMetrics.queue_size}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">CPU Usage</div>
        <div class="metric-value">{$performanceMetrics.cpu_usage.toFixed(1)}%</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Memory Usage</div>
        <div class="metric-value">{$performanceMetrics.memory_usage.toFixed(1)}%</div>
      </div>
    </div>
  </div>

  <!-- Sensor Sources -->
  <div class="sources-section">
    <h3>Sensor Sources</h3>
    <div class="sources-list">
      {#each $sources as source}
        <div class="source-card">
          <div class="source-header">
            <div class="source-info">
              <div class="source-name">{source.name}</div>
              <div class="source-description">{source.description}</div>
            </div>
            <div class="source-status">
              <span class={`status-indicator ${getStatusColor(source.connection_status)}`}>
                {getStatusIcon(source.connection_status)}
              </span>
              <ToggleSwitch
                checked={source.active}
                onchange={() => toggleSource(source)}
                size="sm"
              />
            </div>
          </div>
          
          <div class="source-stats">
            <div class="stat">
              <span class="stat-label">Sensors:</span>
              <span class="stat-value">{source.statistics.active_sensors}/{source.statistics.total_sensors}</span>
            </div>
            <div class="stat">
              <span class="stat-label">Updates:</span>
              <span class="stat-value">{source.statistics.update_count}</span>
            </div>
            <div class="stat">
              <span class="stat-label">Errors:</span>
              <span class="stat-value">{source.statistics.error_count}</span>
            </div>
          </div>
          
          <div class="source-actions">
            <Button variant="outline" size="sm" onclick={() => openSourceConfig(source)}>
              Configure
            </Button>
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>

<!-- Configuration Modal -->
<Modal isOpen={$showConfigModal} title="Real-Time Configuration" onClose={() => $showConfigModal = false}>
  <div class="config-form">
    <div class="form-section">
      <h4>Polling Settings</h4>
      
      <div class="form-group">
        <RangeSlider
          label="Polling Rate"
          min={500}
          max={10000}
          step={100}
          value={$config.polling_rate}
          onchange={(value) => config.update(c => ({ ...c, polling_rate: value }))}
          unit="ms"
        />
        <div class="form-help">How often to fetch sensor data (lower = more responsive, higher CPU usage)</div>
      </div>

      <div class="form-group">
        <ToggleSwitch
          label="Adaptive Polling"
          checked={$config.adaptive_polling}
          onchange={(value) => config.update(c => ({ ...c, adaptive_polling: value }))}
          description="Automatically adjust polling rate based on system load"
        />
      </div>

      <div class="form-group">
        <ToggleSwitch
          label="Burst Mode"
          checked={$config.burst_mode}
          onchange={(value) => config.update(c => ({ ...c, burst_mode: value }))}
          description="Use faster polling for priority sensors"
        />
      </div>
    </div>

    <div class="form-section">
      <h4>Connection Settings</h4>
      
      <div class="form-group">
        <RangeSlider
          label="Connection Timeout"
          min={1000}
          max={30000}
          step={1000}
          value={$config.connection_timeout}
          onchange={(value) => config.update(c => ({ ...c, connection_timeout: value }))}
          unit="ms"
        />
      </div>

      <div class="form-group">
        <RangeSlider
          label="Reconnect Interval"
          min={1000}
          max={30000}
          step={1000}
          value={$config.reconnect_interval}
          onchange={(value) => config.update(c => ({ ...c, reconnect_interval: value }))}
          unit="ms"
        />
      </div>

      <div class="form-group">
        <RangeSlider
          label="Max Reconnect Attempts"
          min={1}
          max={20}
          step={1}
          value={$config.max_reconnect_attempts}
          onchange={(value) => config.update(c => ({ ...c, max_reconnect_attempts: value }))}
        />
      </div>
    </div>

    <div class="form-section">
      <h4>Performance Settings</h4>
      
      <div class="form-group">
        <RangeSlider
          label="Batch Size"
          min={10}
          max={200}
          step={10}
          value={$config.batch_size}
          onchange={(value) => config.update(c => ({ ...c, batch_size: value }))}
          unit="sensors"
        />
        <div class="form-help">Number of sensors to process in each batch</div>
      </div>

      <div class="form-group">
        <ToggleSwitch
          label="Background Polling"
          checked={$config.background_polling}
          onchange={(value) => config.update(c => ({ ...c, background_polling: value }))}
          description="Continue polling when window is not focused"
        />
      </div>

      <div class="form-group">
        <ToggleSwitch
          label="Offline Caching"
          checked={$config.offline_caching}
          onchange={(value) => config.update(c => ({ ...c, offline_caching: value }))}
          description="Cache sensor data when connection is lost"
        />
      </div>

      <div class="form-group">
        <ToggleSwitch
          label="Compression"
          checked={$config.compression}
          onchange={(value) => config.update(c => ({ ...c, compression: value }))}
          description="Compress data transmission to reduce bandwidth"
        />
      </div>
    </div>
  </div>

  {#snippet footer()}
    <div  class="modal-footer">
      <Button variant="outline" onclick={() => $showConfigModal = false}>
        Cancel
      </Button>
      <Button onclick={updateConfiguration}>
        Save Configuration
      </Button>
    </div>
  {/snippet}
</Modal>

<!-- Source Configuration Modal -->
<Modal isOpen={$showSourceConfig} title="Source Configuration" onClose={() => $showSourceConfig = false}>
  {#if $selectedSource}
    <div class="source-config-form">
      <h4>{$selectedSource.name} Configuration</h4>
      <p>Source-specific configuration options would go here.</p>
      <!-- Implementation would depend on specific source capabilities -->
    </div>

    <div class="modal-footer">
      <Button variant="outline" onclick={() => $showSourceConfig = false}>
        Cancel
      </Button>
      <Button onclick={updateSourceConfig}>
        Save
      </Button>
    </div>
  {/if}
</Modal>

<style>
  .sensor-config-container {
    padding: 1.5rem;
    max-width: 1200px;
    margin: 0 auto;
  }

  .config-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e2e8f0;
  }

  .header-info h2 {
    margin: 0 0 0.5rem 0;
    font-size: 1.5rem;
    font-weight: 700;
    color: #1e293b;
  }

  .connection-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
  }

  .status-indicator {
    font-size: 1rem;
    font-weight: bold;
  }

  .header-actions {
    display: flex;
    gap: 0.75rem;
  }

  .metrics-section {
    margin-bottom: 2rem;
  }

  .metrics-section h3 {
    margin: 0 0 1rem 0;
    font-size: 1.125rem;
    font-weight: 600;
    color: #374151;
  }

  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }

  .metric-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 0.5rem;
    padding: 1rem;
    text-align: center;
  }

  .metric-label {
    font-size: 0.75rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
  }

  .metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1e293b;
  }

  .sources-section h3 {
    margin: 0 0 1rem 0;
    font-size: 1.125rem;
    font-weight: 600;
    color: #374151;
  }

  .sources-list {
    display: grid;
    gap: 1rem;
  }

  .source-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 0.75rem;
    padding: 1.5rem;
  }

  .source-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
  }

  .source-name {
    font-size: 1rem;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 0.25rem;
  }

  .source-description {
    font-size: 0.875rem;
    color: #6b7280;
  }

  .source-status {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .source-stats {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 1rem;
    padding: 0.75rem 0;
    border-top: 1px solid #f1f5f9;
    border-bottom: 1px solid #f1f5f9;
  }

  .stat {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .stat-label {
    font-size: 0.75rem;
    color: #6b7280;
  }

  .stat-value {
    font-size: 0.875rem;
    font-weight: 600;
    color: #1e293b;
  }

  .source-actions {
    display: flex;
    justify-content: flex-end;
  }

  .config-form {
    max-height: 60vh;
    overflow-y: auto;
  }

  .form-section {
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #f1f5f9;
  }

  .form-section:last-child {
    border-bottom: none;
    margin-bottom: 0;
  }

  .form-section h4 {
    margin: 0 0 1rem 0;
    font-size: 1rem;
    font-weight: 600;
    color: #374151;
  }

  .form-group {
    margin-bottom: 1.5rem;
  }

  .form-help {
    margin-top: 0.25rem;
    font-size: 0.75rem;
    color: #6b7280;
  }

  .modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 0.75rem;
    padding-top: 1rem;
    border-top: 1px solid #e2e8f0;
  }

  .source-config-form {
    padding: 1rem 0;
  }

  .source-config-form h4 {
    margin: 0 0 0.5rem 0;
    font-size: 1rem;
    font-weight: 600;
    color: #374151;
  }
</style>
