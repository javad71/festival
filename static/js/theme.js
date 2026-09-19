(() => {
    const root = document.documentElement;
    const button = document.getElementById("themeToggle");
    const icon = document.getElementById("themeIcon");
    const saved = localStorage.getItem("festival-theme");
    if (saved) root.dataset.theme = saved;
    else if (window.matchMedia?.("(prefers-color-scheme: dark)").matches) root.dataset.theme = "dark";

    function render() {
        icon.textContent = root.dataset.theme === "dark" ? "🌙" : "☀️";
    }
    render();
    button?.addEventListener("click", () => {
        root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
        localStorage.setItem("festival-theme", root.dataset.theme);
        render();
    });
})();
