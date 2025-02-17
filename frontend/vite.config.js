import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom', // Simulates the browser for React testing
    setupFiles: './src/setupTests.js', // Setup file for Jest
  },
});
