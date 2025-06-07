<script lang="ts">
  import { Button, Modal } from '../index';


  interface Props {
    open?: boolean;
    uploadType?: 'background' | 'gauge-sequence' | 'single';
    maxFiles?: any;
    upload: (data: any) => void;
    close: () => void;
  }

  let {
    open = $bindable(false),
    uploadType = 'single',
    maxFiles = uploadType === 'gauge-sequence' ? 50 : 1,
    upload,
    close
  }: Props = $props();

  let fileInput: HTMLInputElement = $state();
  let dragActive = $state(false);
  let uploadedFiles: File[] = $state([]);
  let previewUrls: string[] = $state([]);
  let uploading = $state(false);

  // Image processing options
  let resizeImages = $state(true);
  let maxWidth = $state(1920);
  let maxHeight = $state(1080);
  let quality = $state(0.9);

  function handleFileSelect(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files) {
      processFiles(Array.from(input.files));
    }
  }

  function handleDrop(event: DragEvent) {
    event.preventDefault();
    dragActive = false;
    
    if (event.dataTransfer?.files) {
      processFiles(Array.from(event.dataTransfer.files));
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

  async function processFiles(files: File[]) {
    const imageFiles = files.filter(file => file.type.startsWith('image/'));
    
    if (imageFiles.length === 0) {
      alert('Please select valid image files');
      return;
    }

    if (imageFiles.length > maxFiles) {
      alert(`Maximum ${maxFiles} files allowed`);
      return;
    }

    uploading = true;
    uploadedFiles = imageFiles;
    previewUrls = [];

    try {
      for (const file of imageFiles) {
        const processedFile = resizeImages ? await resizeImage(file) : file;
        const url = URL.createObjectURL(processedFile);
        previewUrls.push(url);
      }
    } catch (error) {
      console.error('Error processing images:', error);
      alert('Error processing images');
    } finally {
      uploading = false;
    }
  }

  async function resizeImage(file: File): Promise<File> {
    return new Promise((resolve) => {
      const img = new Image();
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d')!;

      img.onload = () => {
        // Calculate new dimensions
        let { width, height } = img;
        
        if (width > maxWidth || height > maxHeight) {
          const ratio = Math.min(maxWidth / width, maxHeight / height);
          width *= ratio;
          height *= ratio;
        }

        canvas.width = width;
        canvas.height = height;
        
        // Draw and compress
        ctx.drawImage(img, 0, 0, width, height);
        
        canvas.toBlob((blob) => {
          if (blob) {
            const resizedFile = new File([blob], file.name, {
              type: file.type,
              lastModified: Date.now()
            });
            resolve(resizedFile);
          } else {
            resolve(file);
          }
        }, file.type, quality);
      };

      img.src = URL.createObjectURL(file);
    });
  }

  function removeFile(index: number) {
    uploadedFiles = uploadedFiles.filter((_, i) => i !== index);
    URL.revokeObjectURL(previewUrls[index]);
    previewUrls = previewUrls.filter((_, i) => i !== index);
  }

  function handleUpload() {
    if (uploadedFiles.length === 0) return;

    const uploadData = {
      files: uploadedFiles,
      urls: previewUrls,
      type: uploadType,
      settings: {
        resized: resizeImages,
        maxWidth,
        maxHeight,
        quality
      }
    };

    upload(uploadData);
    close();
  }

  function handleClose() {
    // Clean up object URLs
    previewUrls.forEach(url => URL.revokeObjectURL(url));
    uploadedFiles = [];
    previewUrls = [];
    close();
  }

  // Get upload instructions based on type
  let uploadInstructions = $derived({
    background: 'Upload a background image for your dashboard',
    'gauge-sequence': 'Upload multiple images to create an animated gauge sequence',
    single: 'Upload an image'
  }[uploadType]);

  
</script>

<Modal bind:open title="Upload Images" size="lg" onclose={handleClose}>
  <div class="upload-manager">
    <!-- Upload Instructions -->
    <div class="upload-instructions">
      <h3>{uploadInstructions}</h3>
      <p class="text-sm text-gray-600">
        Supported formats: JPEG, PNG, GIF, WebP
        {#if uploadType === 'gauge-sequence'}
          <br>Upload up to {maxFiles} images for animation sequence
        {/if}
      </p>
    </div>

    <!-- Drag & Drop Area -->
    <div 
      class="drop-zone"
      class:drag-active={dragActive}
      ondrop={handleDrop}
      ondragover={handleDragOver}
      ondragleave={handleDragLeave}
      role="button"
      tabindex="0"
      onclick={() => fileInput?.click()}
      onkeydown={(e) => e.key === 'Enter' && fileInput?.click()}
    >
      {#if uploading}
        <div class="upload-spinner">
          <div class="spinner"></div>
          <p>Processing images...</p>
        </div>
      {:else}
        <div class="drop-content">
          <svg class="upload-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          <p class="drop-text">
            {dragActive ? 'Drop images here' : 'Drag & drop images here or click to browse'}
          </p>
          <p class="drop-subtext">
            {uploadType === 'gauge-sequence' ? `Up to ${maxFiles} files` : 'Single file'}
          </p>
        </div>
      {/if}
    </div>

    <!-- Hidden File Input -->
    <input
      bind:this={fileInput}
      type="file"
      accept={acceptedFormats}
      multiple={uploadType === 'gauge-sequence'}
      class="hidden"
      onchange={handleFileSelect}
    />

    <!-- Processing Options -->
    <div class="processing-options">
      <h4>Processing Options</h4>
      
      <label class="option-row">
        <input type="checkbox" bind:checked={resizeImages} />
        <span>Resize images for optimal performance</span>
      </label>

      {#if resizeImages}
        <div class="resize-settings">
          <div class="setting-row">
            <span>Max Width:</span>
            <input type="number" bind:value={maxWidth} min="100" max="4096" />
          </div>
          <div class="setting-row">
            <span>Max Height:</span>
            <input type="number" bind:value={maxHeight} min="100" max="4096" />
          </div>
          <div class="setting-row">
            <span>Quality:</span>
            <input type="range" bind:value={quality} min="0.1" max="1" step="0.1" />
            <span>{Math.round(quality * 100)}%</span>
          </div>
        </div>
      {/if}
    </div>

    <!-- Preview Grid -->
    {#if previewUrls.length > 0}
      <div class="preview-section">
        <h4>Preview ({previewUrls.length} files)</h4>
        <div class="preview-grid">
          {#each previewUrls as url, index}
            <div class="preview-item">
              <img src={url || "/placeholder.svg"} alt="Preview {index + 1}" />
              <button 
                class="remove-btn"
                onclick={() => removeFile(index)}
                title="Remove image"
                aria-label="Remove image"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
              {#if uploadType === 'gauge-sequence'}
                <div class="sequence-number">{index + 1}</div>
              {/if}
            </div>
          {/each}
        </div>
      </div>
    {/if}

    <!-- Actions -->
    <div class="modal-actions">
      <Button variant="outline" onclick={handleClose}>Cancel</Button>
      <Button 
        variant="primary" 
        onclick={handleUpload}
        disabled={uploadedFiles.length === 0 || uploading}
      >
        Upload {uploadedFiles.length} {uploadedFiles.length === 1 ? 'Image' : 'Images'}
      </Button>
    </div>
  </div>
</Modal>

<style>
  .upload-manager {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .upload-instructions h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.125rem;
    font-weight: 600;
  }

  .drop-zone {
    border: 2px dashed #d1d5db;
    border-radius: 1rem;
    padding: 3rem 2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
    background: #f9fafb;
  }

  .drop-zone:hover,
  .drop-zone.drag-active {
    border-color: #3b82f6;
    background: #eff6ff;
  }

  .upload-icon {
    width: 3rem;
    height: 3rem;
    margin: 0 auto 1rem;
    color: #6b7280;
  }

  .drop-text {
    font-size: 1.125rem;
    font-weight: 500;
    color: #374151;
    margin: 0 0 0.5rem 0;
  }

  .drop-subtext {
    font-size: 0.875rem;
    color: #6b7280;
    margin: 0;
  }

  .upload-spinner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .spinner {
    width: 2rem;
    height: 2rem;
    border: 3px solid #e5e7eb;
    border-top: 3px solid #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .processing-options {
    background: #f8fafc;
    padding: 1.5rem;
    border-radius: 0.75rem;
    border: 1px solid #e2e8f0;
  }

  .processing-options h4 {
    margin: 0 0 1rem 0;
    font-size: 1rem;
    font-weight: 600;
  }

  .option-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
    cursor: pointer;
  }

  .resize-settings {
    margin-left: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .setting-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .setting-row span {
    min-width: 80px;
    font-size: 0.875rem;
    font-weight: 500;
  }

  .setting-row input[type="number"] {
    width: 80px;
    padding: 0.25rem 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
  }

  .setting-row input[type="range"] {
    flex: 1;
  }

  .preview-section h4 {
    margin: 0 0 1rem 0;
    font-size: 1rem;
    font-weight: 600;
  }

  .preview-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 1rem;
    max-height: 300px;
    overflow-y: auto;
  }

  .preview-item {
    position: relative;
    aspect-ratio: 1;
    border-radius: 0.5rem;
    overflow: hidden;
    border: 2px solid #e5e7eb;
  }

  .preview-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .remove-btn {
    position: absolute;
    top: 0.25rem;
    right: 0.25rem;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    border: none;
    border-radius: 50%;
    width: 1.5rem;
    height: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.2s;
  }

  .preview-item:hover .remove-btn {
    opacity: 1;
  }

  .sequence-number {
    position: absolute;
    bottom: 0.25rem;
    left: 0.25rem;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.125rem 0.375rem;
    border-radius: 0.25rem;
  }

  .modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.75rem;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
  }

  .hidden {
    display: none;
  }
</style>
