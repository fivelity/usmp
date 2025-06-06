import adapter from "@sveltejs/adapter-static"; // Changed from adapter-auto
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),

  kit: {
    adapter: adapter(),
    alias: {
      $lib: "./src/lib",
    },
    // Ensure paths are relative for static export if you have base path needs
    // paths: {
    //  base: process.env.NODE_ENV === 'production' ? '/your-base-path' : '',
    // },
  },
  compilerOptions: {
    runes: true,
  },
};

export default config;
