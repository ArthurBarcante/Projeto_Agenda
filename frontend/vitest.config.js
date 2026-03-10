import { defineConfig } from "vitest/config"

export default defineConfig({
  server: {
    fs: {
      allow: [".."]
    }
  },
  test: {
    environment: "jsdom",
    include: ["../tests/fase_2_engajamento/**/*.test.js"],
    globals: true
  }
})
