import { createPreset } from "fumadocs-ui/tailwind-plugin";

// This plugin injects CSS variables for our color themes.
// Light theme (default) is defined on :root and dark mode variables are set under .dark.
function addThemeVariables({ addBase }) {
  addBase({
    ":root": {
      // Light theme variables
      "--border": "220 14% 96%",
      "--input": "220 14% 96%",
      "--ring": "220 14% 96%",
      "--background": "0 0% 100%", // White background in light mode
      "--foreground": "240 85% 2%", // Dark navy blue text in light mode
      "--highlight": "50 100% 50%", // Yellow highlight remains the same
      // Additional variables can be defined as needed
    },
    ".dark": {
      "--border": "210 29% 20%",
      "--input": "210 29% 20%",
      "--ring": "210 29% 20%",
      "--card": "232 52% 8%",
      "--muted": "233 37% 15%",
      "--muted-foreground": "0 0% 75%",
      "--primary": "50 100% 50%",
      "--primary-hover": "65 41% 90%",
      "--primary-active-hover":"56 100% 50%",
      "--accent-foreground": "0 0% 100%",
      "--accent": "240, 67%, 14%",
      "--background": "240 85% 4%", // Dark navy blue background in dark mode
      "--foreground": "0 0% 100%", // White text in dark mode
      "--highlight": "50 100% 50%", // Yellow highlight remains the same
    },
  });
}

/** @type {import('tailwindcss').Config} */
export default {
  // Enable dark mode via a CSS class (i.e. add "dark" on your <html> or <body>)
  darkMode: "class",
  content: [
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./content/**/*.{md,mdx}",
    "./mdx-components.{ts,tsx}",
    "./node_modules/fumadocs-ui/dist/**/*.js",
  ],
  theme: {
    extend: {
      // Use CSS variables to define your palette
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        highlight: "hsl(var(--highlight))",
        primary: {
          DEFAULT: "hsl(var(--foreground))",
          foreground: "hsl(var(--background))",
        },
        secondary: {
          DEFAULT: "hsl(var(--input))",
          foreground: "hsl(var(--background))",
        },
      },
      // Custom border radius values using a CSS variable for dynamic control.
      borderRadius: {
        lg: "var(--radius, 0.5rem)",
        md: "calc(var(--radius, 0.5rem) - 2px)",
        sm: "calc(var(--radius, 0.5rem) - 4px)",
      },
      // Custom keyframes for accordion and background animations.
    },
  },
  presets: [
    createPreset({
      // You can customize preset options here if needed.
    }),
  ],
  plugins: [addThemeVariables],
};
