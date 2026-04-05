/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        appBg: "#121212",
        appSurface: "#1E1E1E",
        appPrimary: "#F97316",
        appText: "#FFFFFF",
        appMuted: "#A1A1AA",
      },
      borderRadius: {
        card: "16px",
        hero: "24px",
      },
    },
  },
  plugins: [],
};
