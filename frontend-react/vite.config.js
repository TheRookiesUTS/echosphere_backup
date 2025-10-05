import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    host: true,
    open: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: false, // Disable sourcemaps in production
    minify: 'esbuild', // Use esbuild for faster minification
    rollupOptions: {
      output: {
        manualChunks: {
          // Code splitting - separate large dependencies
          'react-vendor': ['react', 'react-dom'],
          'map-vendor': ['leaflet', 'react-leaflet'],
          'ui-vendor': ['lucide-react', 'zustand'],
        },
      },
    },
    chunkSizeWarningLimit: 1000, // Increase warning limit
  },
})

