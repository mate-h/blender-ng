import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import { openTopographyPlugin } from './vite-plugins/opentopography-plugin.js'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    svelte(),
    openTopographyPlugin()
  ],
})
