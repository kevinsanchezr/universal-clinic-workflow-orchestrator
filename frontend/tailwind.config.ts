import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#f4f6f8",
        panel: "#ffffff",
        ink: "#13202b",
        muted: "#6e7b87",
        line: "#d8e0e7",
        accent: "#0f766e",
        warning: "#d97706",
        danger: "#b91c1c",
      },
      boxShadow: {
        panel: "0 16px 48px rgba(17, 24, 39, 0.08)",
      },
      fontFamily: {
        sans: ["'IBM Plex Sans'", "sans-serif"],
        mono: ["'IBM Plex Mono'", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;
