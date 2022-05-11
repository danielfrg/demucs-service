module.exports = {
    content: ["./src/**/*.{astro,html,js,jsx,svelte,ts,tsx,vue}"],
    theme: {
        extend: {},
    },
    theme: {
        extend: {
            colors: {
                primary: "#313638",
                blue: "#222831",
            },
            fontSize: {
                title: "15rem",
            },
            typography: {
                DEFAULT: {
                    css: {},
                },
            },
        },
    },
    variants: {
        extend: {
            borderStyle: ["responsive", "hover"],
            borderWidth: ["responsive", "hover"],
        },
    },
    plugins: [require("@tailwindcss/typography")],
};
