<script lang="ts">
  import { onMount } from 'svelte';
  import type { BaseComponentProps } from '$lib/types';
  import type { Snippet } from 'svelte';
  import Button from './Button.svelte';

  interface Props extends BaseComponentProps {
    fallback?: Snippet<[{ error: Error | null, errorInfo: any, retry: () => void }]>;
    onError?: (error: Error, errorInfo: any) => void;
    children?: Snippet;
  }

  let {
    fallback,
    onError,
    children,
    class: className = '',
    ...restProps
  }: Props = $props();

  let hasError = $state(false);
  let error = $state<Error | null>(null);
  let errorInfo = $state<any>(null);

  function handleError(event: ErrorEvent) {
    hasError = true;
    error = new Error(event.message);
    errorInfo = {
      filename: event.filename,
      lineno: event.lineno,
      colno: event.colno,
      stack: event.error?.stack
    };
    
    onError?.(error, errorInfo);
  }

  function handleUnhandledRejection(event: PromiseRejectionEvent) {
    hasError = true;
    error = new Error(event.reason);
    errorInfo = { type: 'unhandledRejection', reason: event.reason };
    
    onError?.(error, errorInfo);
  }

  function retry() {
    hasError = false;
    error = null;
    errorInfo = null;
  }

  onMount(() => {
    window.addEventListener('error', handleError);
    window.addEventListener('unhandledrejection', handleUnhandledRejection);

    return () => {
      window.removeEventListener('error', handleError);
      window.removeEventListener('unhandledrejection', handleUnhandledRejection);
    };
  });
</script>

{#if hasError}
  {#if fallback}
    {@render fallback({ error, errorInfo, retry })}
  {:else}
    <div class="error-boundary {className}" {...restProps}>
      <div class="error-content">
        <div class="error-icon">
          <svg class="w-12 h-12 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        </div>
        
        <h2 class="error-title">Something went wrong</h2>
        <p class="error-message">
          An unexpected error occurred. Please try refreshing the page or contact support if the problem persists.
        </p>
        
        {#if error}
          <details class="error-details">
            <summary>Error Details</summary>
            <pre class="error-stack">{error.message}</pre>
            {#if errorInfo?.stack}
              <pre class="error-stack">{errorInfo.stack}</pre>
            {/if}
          </details>
        {/if}
        
        <div class="error-actions">
          <Button variant="primary" onClick={retry}>
            Try Again
          </Button>
          <Button variant="outline" onClick={() => window.location.reload()}>
            Refresh Page
          </Button>
        </div>
      </div>
    </div>
  {/if}
{:else}
  {@render children?.()}
{/if}

<style>
  .error-boundary {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    padding: 2rem;
  }

  .error-content {
    text-align: center;
    max-width: 500px;
  }

  .error-icon {
    margin-bottom: 1.5rem;
  }

  .error-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 1rem;
  }

  .error-message {
    font-size: 1rem;
    color: #6b7280;
    margin-bottom: 2rem;
    line-height: 1.6;
  }

  .error-details {
    text-align: left;
    margin-bottom: 2rem;
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    padding: 1rem;
  }

  .error-details summary {
    cursor: pointer;
    font-weight: 600;
    color: #374151;
    margin-bottom: 0.5rem;
  }

  .error-stack {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #ef4444;
    background: #fef2f2;
    padding: 0.75rem;
    border-radius: 0.375rem;
    overflow-x: auto;
    margin: 0.5rem 0;
  }

  .error-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
  }
</style>
