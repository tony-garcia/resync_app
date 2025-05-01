import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import { nodePolyfills } from 'vite-plugin-node-polyfills';

export default defineConfig(({ command, mode }) => {
  // Load env file based on `mode` in the current working directory.
  // Set the third parameter to '' to load all env regardless of the `VITE_`
  const env = loadEnv(mode, process.cwd(), '');
  const config = {
    build: {
      sourcemap: true,
    },
    optimizeDeps: {
      exclude: [] // You can add specific problematic dependencies here if needed
    },
    plugins: [
      react(),
      nodePolyfills({
        // Whether to polyfill `node:` protocol imports.
        protocolImports: true,
      }),
    ],
    server: {
      host: '0.0.0.0', // This allows external acces to the dev server
      port: 3000,
      hmr: {
        clientPort: 3000 // Ensure websocket connections to use the correct port
      },
      watch: {
        usePolling: true // Help with file watching in Docker
      },
      proxy: {
        '/api': {
          target: 'http://api:8000',
          changeOrigin: true,
          secure: false,
        },
      },
    },
  };
  return config;
});
