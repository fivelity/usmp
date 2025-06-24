// tailwind.config.js for Tailwind CSS v4
/**
 * Tailwind CSS v4 Configuration
 * @type {import('tailwindcss').Config}
 */
export default {
  content: [
    './src/**/*.{html,js,svelte,ts}',
    './index.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Monaco', 'Consolas', 'monospace'],
      },
    },
  },
  plugins: [],
};
