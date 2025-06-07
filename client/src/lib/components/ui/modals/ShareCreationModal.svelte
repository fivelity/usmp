<script lang="ts">
  import Button from '$lib/components/ui/common/Button.svelte';
  import Modal from '$lib/components/ui/common/Modal.svelte';
  import { get } from 'svelte/store';
  import { widgets, widgetGroups, dashboardLayout } from '$lib/stores';
import { visualSettingsOriginal as visualSettings } from '$lib/stores/core/visual.svelte';
  import { currentTheme } from '$lib/stores/themes';

  type ExportFormat = 'json' | 'url' | 'qr';

  interface ShareCreationContent {
    widgets?: unknown; // Replace 'unknown' with actual WidgetConfig[] type if available
    widget_groups?: unknown; // Replace 'unknown' with actual WidgetGroup[] type if available
    layout?: unknown; // Replace 'unknown' with actual Layout type if available
    visual_settings?: unknown; // Replace 'unknown' with actual VisualSettings type if available
    current_theme?: string;
  }

  interface ShareCreation {
    version: string;
    type: 'dashboard_snapshot';
    content: ShareCreationContent;
    timestamp: string;
    metadata?: Record<string, unknown>;
  }

  let { open = false, foo = () => {} } = $props(); // Use Svelte 5 syntax for component props

  let shareData = {
    name: '',
    description: '',
    author: '',
    tags: '',
    includeWidgets: true,
    includeLayout: true,
    includeTheme: true,
    includeImages: false,
    isPublic: true
  };

  // Local state for the modal using Svelte 5 runes
  let exportFormat = $state<ExportFormat>('json');
  let generatedCode = $state('');
  let shareUrl = $state('');
  let qrCodeUrl = $state('');
  let copying = $state(false);

  // Generate shareable creation
  function generateShare() {
    const creation: ShareCreation = {
      version: '1.0', // Moved from metadata
      type: 'dashboard_snapshot', // Corrected type as per interface, moved from metadata
      timestamp: new Date().toISOString(), // Added timestamp
      metadata: {
        name: shareData.name,
        description: shareData.description,
        author: shareData.author,
        tags: shareData.tags.split(',').map(t => t.trim()).filter(Boolean),
        // created_at can be part of metadata or covered by the main timestamp
      },
      content: {} as ShareCreationContent
    };

    if (shareData.includeWidgets) {
      creation.content.widgets = widgets; // Use globalThis to reference global variables
      creation.content.widget_groups = widgetGroups;
    }

    if (shareData.includeLayout) {
      creation.content.layout = dashboardLayout;
    }

    if (shareData.includeTheme) {
      creation.content.visual_settings = get(visualSettings);
      creation.content.current_theme = get(currentTheme);
    }

    return creation;
  }

  function handleExport() {
    const creation = generateShare();

    switch (exportFormat) {
      case 'json':
        generatedCode = JSON.stringify(creation, null, 2);
        break;
      case 'url': {
        const encoded = btoa(JSON.stringify(creation));
        shareUrl = `${window.location.origin}/import?data=${encoded}`;
        generatedCode = shareUrl;
        break;
      }
      case 'qr': {
        const qrData = btoa(JSON.stringify(creation));
        qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(`${window.location.origin}/import?data=${qrData}`)}`;
        break;
      }
    }
  }

  async function copyToClipboard() {
    if (!generatedCode) return;
    
    copying = true;
    try {
      await navigator.clipboard.writeText(generatedCode);
      // Show success feedback
      setTimeout(() => copying = false, 1000);
    } catch (error) {
      console.error('Failed to copy:', error);
      copying = false;
    }
  }

  function downloadFile() {
    if (!generatedCode) return;

    const blob = new Blob([generatedCode], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${shareData.name || 'ultimon-creation'}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function handleClose() {
    open = false;
    generatedCode = '';
    shareUrl = '';
    qrCodeUrl = '';
    foo(); // Use callback prop to close the modal
  }

  // Auto-generate when format changes
  $effect(() => {
    if (exportFormat && shareData.name) {
      handleExport();
    }
  });
</script>

<Modal isOpen={open} title="Create Shareable Snapshot" on:close={handleClose} size="lg">
  <div class="share-modal">
    <!-- Creation Details -->
    <div class="section">
      <h3>Creation Details</h3>
      
      <div class="form-grid">
        <div class="form-group">
          <label for="creation-name">Name *</label>
          <input
            id="creation-name"
            type="text"
            bind:value={shareData.name}
            placeholder="My Awesome Dashboard"
            class="form-input"
            required
          />
        </div>

        <div class="form-group">
          <label for="creation-author">Author</label>
          <input
            id="creation-author"
            type="text"
            bind:value={shareData.author}
            placeholder="Your name"
            class="form-input"
          />
        </div>

        <div class="form-group full-width">
          <label for="creation-description">Description</label>
          <textarea
            id="creation-description"
            bind:value={shareData.description}
            placeholder="Describe your creation..."
            class="form-textarea"
            rows="3"
          ></textarea>
        </div>

        <div class="form-group full-width">
          <label for="creation-tags">Tags</label>
          <input
            id="creation-tags"
            type="text"
            bind:value={shareData.tags}
            placeholder="gaming, rgb, minimal (comma separated)"
            class="form-input"
          />
        </div>
      </div>
    </div>

    <!-- What to Include -->
    <div class="section">
      <h3>What to Include</h3>
      
      <div class="checkbox-grid">
        <label class="checkbox-item">
          <input type="checkbox" bind:checked={shareData.includeWidgets} />
          <span class="checkbox-label">
            <strong>Widgets & Layout</strong>
            <small>All widgets and their positions</small>
          </span>
        </label>

        <label class="checkbox-item">
          <input type="checkbox" bind:checked={shareData.includeLayout} />
          <span class="checkbox-label">
            <strong>Canvas Settings</strong>
            <small>Background and canvas configuration</small>
          </span>
        </label>

        <label class="checkbox-item">
          <input type="checkbox" bind:checked={shareData.includeTheme} />
          <span class="checkbox-label">
            <strong>Theme & Styling</strong>
            <small>Colors, fonts, and visual settings</small>
          </span>
        </label>

        <label class="checkbox-item">
          <input type="checkbox" bind:checked={shareData.includeImages} />
          <span class="checkbox-label">
            <strong>Custom Images</strong>
            <small>Background and gauge images (larger file)</small>
          </span>
        </label>
      </div>
    </div>

    <!-- Export Format -->
    <div class="section">
      <h3>Export Format</h3>
      
      <div class="format-options">
        <label class="format-option" class:active={exportFormat === 'json'}>
          <input type="radio" bind:group={exportFormat} value="json" />
          <div class="format-content">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <div>
              <strong>JSON File</strong>
              <small>Download as .json file for manual sharing</small>
            </div>
          </div>
        </label>

        <label class="format-option" class:active={exportFormat === 'url'}>
          <input type="radio" bind:group={exportFormat} value="url" />
          <div class="format-content">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
            </svg>
            <div>
              <strong>Share URL</strong>
              <small>Generate a link to share directly</small>
            </div>
          </div>
        </label>

        <label class="format-option" class:active={exportFormat === 'qr'}>
          <input type="radio" bind:group={exportFormat} value="qr" />
          <div class="format-content">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1v-2a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1z" />
            </svg>
            <div>
              <strong>QR Code</strong>
              <small>Generate QR code for mobile sharing</small>
            </div>
          </div>
        </label>
      </div>
    </div>

    <!-- Generated Output -->
    {#if generatedCode || qrCodeUrl}
      <div class="section">
        <h3>Generated Share</h3>
        
        {#if exportFormat === 'qr' && qrCodeUrl}
          <div class="qr-container">
            <img src={qrCodeUrl || "/placeholder.svg"} alt="QR Code" class="qr-code" />
            <p>Scan with your phone to import this creation</p>
          </div>
        {:else if generatedCode}
          <div class="code-container">
            <div class="code-header">
              <span class="code-label">
                {exportFormat === 'url' ? 'Share URL' : 'JSON Data'}
              </span>
              <div class="code-actions">
                <Button variant="secondary" onClick={copyToClipboard} disabled={!generatedCode || copying}>
                  {#if copying}
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    Copied!
                  {:else}
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                    Copy
                  {/if}
                </Button>
                
                {#if exportFormat === 'json'}
                  <Button variant="secondary" onClick={downloadFile}>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Download
                  </Button>
                {/if}
              </div>
            </div>
            
            <textarea
              class="code-output"
              readonly
              bind:value={generatedCode}
              rows={exportFormat === 'url' ? 3 : 10}
            ></textarea>
          </div>
        {/if}
      </div>
    {/if}

    <!-- Actions -->
    <div class="modal-actions">
      <Button variant="secondary" onClick={handleClose}>Close</Button>
      <Button variant="primary" onClick={handleExport} disabled={!shareData.name}>
        Generate Share
      </Button>
    </div>
  </div>
</Modal>

<style>
  .share-modal {
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  .section {
    background: #f8fafc;
    padding: 1.5rem;
    border-radius: 0.75rem;
    border: 1px solid #e2e8f0;
  }

  .section h3 {
    margin: 0 0 1rem 0;
    font-size: 1.125rem;
    font-weight: 600;
    color: #1e293b;
  }

  .form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }

  .form-group {
    display: flex;
    flex-direction: column;
  }

  .form-group.full-width {
    grid-column: 1 / -1;
  }

  .form-group label {
    font-size: 0.875rem;
    font-weight: 500;
    color: #374151;
    margin-bottom: 0.5rem;
  }

  .form-input,
  .form-textarea {
    padding: 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    transition: border-color 0.2s;
  }

  .form-input:focus,
  .form-textarea:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  .checkbox-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }

  .checkbox-item {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 1rem;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.2s;
  }

  .checkbox-item:hover {
    border-color: #3b82f6;
    background: #f8fafc;
  }

  .checkbox-item input[type="checkbox"] {
    margin-top: 0.125rem;
  }

  .checkbox-label {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .checkbox-label strong {
    font-size: 0.875rem;
    color: #1e293b;
  }

  .checkbox-label small {
    font-size: 0.75rem;
    color: #64748b;
  }

  .format-options {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .format-option {
    display: flex;
    align-items: center;
    padding: 1rem;
    background: white;
    border: 2px solid #e2e8f0;
    border-radius: 0.75rem;
    cursor: pointer;
    transition: all 0.2s;
  }

  .format-option:hover {
    border-color: #3b82f6;
  }

  .format-option.active {
    border-color: #3b82f6;
    background: #eff6ff;
  }

  .format-option input[type="radio"] {
    margin-right: 1rem;
  }

  .format-content {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .format-content svg {
    color: #6b7280;
  }

  .format-option.active .format-content svg {
    color: #3b82f6;
  }

  .format-content div {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .format-content strong {
    font-size: 0.875rem;
    color: #1e293b;
  }

  .format-content small {
    font-size: 0.75rem;
    color: #64748b;
  }

  .qr-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    padding: 2rem;
    background: white;
    border-radius: 0.75rem;
    border: 1px solid #e2e8f0;
  }

  .qr-code {
    width: 200px;
    height: 200px;
    border-radius: 0.5rem;
  }

  .qr-container p {
    margin: 0;
    font-size: 0.875rem;
    color: #64748b;
    text-align: center;
  }

  .code-container {
    background: white;
    border-radius: 0.75rem;
    border: 1px solid #e2e8f0;
    overflow: hidden;
  }

  .code-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
  }

  .code-label {
    font-size: 0.875rem;
    font-weight: 500;
    color: #374151;
  }

  .code-actions {
    display: flex;
    gap: 0.5rem;
  }

  .code-output {
    width: 100%;
    padding: 1rem;
    border: none;
    background: #1e293b;
    color: #f1f5f9;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 0.75rem;
    line-height: 1.5;
    resize: none;
  }

  .code-output:focus {
    outline: none;
  }

  .modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.75rem;
    padding-top: 1rem;
    border-top: 1px solid #e2e8f0;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .form-grid,
    .checkbox-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
