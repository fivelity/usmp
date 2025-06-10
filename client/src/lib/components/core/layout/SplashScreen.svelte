<script lang="ts">
  import { fly } from 'svelte/transition';

  let { message = 'Initializing Application...' }: { message?: string } = $props();
</script>

<div
  class="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-gray-900/80 backdrop-blur-sm"
  transition:fly={{ y: -20, duration: 300 }}
>
  <div class="text-center">
    <div class="relative mb-8 h-24 w-24">
      <div class="absolute h-full w-full animate-spin rounded-full border-4 border-solid border-blue-500 border-t-transparent"></div>
      <div class="absolute inset-0 flex items-center justify-center">
        <svg class="h-12 w-12 text-blue-400" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21.21 15.89A10 10 0 1 1 8 2.83" />
          <path d="M22 12A10 10 0 0 0 12 2v10z" />
        </svg>
      </div>
    </div>
    <h1
      class="text-2xl font-semibold text-white"
      in:fly={{ y: 20, delay: 100, duration: 400 }}
    >
      Ultimate Sensor Monitor
    </h1>
    <p
      class="mt-2 text-sm text-gray-300"
      in:fly={{ y: 20, delay: 200, duration: 400 }}
    >
      {message}
    </p>
  </div>
</div> 