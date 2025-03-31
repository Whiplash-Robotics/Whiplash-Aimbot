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
      "--card": "210 0% 100%", // White card background
      "--muted": "210 20% 90%", // Soft gray for muted elements
      "--muted-foreground": "220 10% 40%", // Medium gray for muted text
      "--primary": "50 100% 50%", // Vibrant blue (adjust as needed)
      "--primary-hover": "221 83% 45%", // Slightly darker blue on hover
      "--primary-active-hover": "56 100% 40%", // Even darker blue when active
      "--accent": "56 68% 91%", // Warm yellow accent
      "--accent-foreground": "240 85% 2%", // Dark text for contrast
      "--background3": "210 50% 98%", // Very light gray background
      "--background2": "210 50% 95%", // Slightly darker than background3
      "--background": "210 50% 100%", // White background in light mode
      "--foreground": "240 85% 2%", // Dark navy blue text in light mode
      "--highlight": "50 100% 50%", // Yellow highlight remains the same
      "--article-blur": "0px",
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
      "--primary-active-hover": "56 100% 50%",
      "--accent-foreground": "0 0% 100%",
      "--accent": "240 67% 14%",
      "--background3": "240, 67%, 8%",
      "--background2": "240, 85%, 6%",
      "--background": "240, 85%, 5%", // Dark navy blue background in dark mode
      "--foreground": "0 0% 100%", // White text in dark mode
      "--highlight": "50 100% 50%", // Yellow highlight remains the same
      "--article-blur": "1rem",
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
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
          text: "hsl(var(--muted-text))",
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
