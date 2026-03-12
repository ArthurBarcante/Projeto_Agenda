import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    // paths are relative to frontend/config/styles/ → ../../src/
    "../../src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "../../src/features/**/*.{js,ts,jsx,tsx,mdx}",
    "../../src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "../../src/hooks/**/*.{js,ts,jsx,tsx,mdx}",
    "../../src/utils/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};

export default config;
