(() => {
    const root = document.getElementById("publicStats");
    if (!root) return;

    const numberFormatter = new Intl.NumberFormat("fa-IR");
    const animateNumber = (el, target) => {
        const start = Number(el.dataset.current || 0);
        const duration = 650;
        const started = performance.now();

        const tick = (now) => {
            const progress = Math.min((now - started) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const value = Math.round(start + (target - start) * eased);
            el.textContent = numberFormatter.format(value);
            if (progress < 1) requestAnimationFrame(tick);
        };
        el.dataset.current = String(target);
        requestAnimationFrame(tick);
    };

    const update = async () => {
        try {
            const response = await fetch(root.dataset.statsUrl, {
                headers: {"Accept": "application/json"},
                cache: "no-store"
            });
            if (!response.ok) return;
            const data = await response.json();

            ["submissions", "participants", "categories", "approved", "pending"].forEach((key) => {
                const el = root.querySelector(`[data-stat="${key}"]`);
                if (el && Number.isFinite(Number(data[key]))) {
                    animateNumber(el, Number(data[key]));
                }
            });

            const total = Number(data.submissions) || 0;
            root.querySelectorAll(".category-stat").forEach((item) => {
                const slug = item.dataset.category;
                const count = Number(data.category_counts?.[slug] || 0);
                const countEl = item.querySelector(".category-stat-top strong");
                const bar = item.querySelector(".category-progress span");
                if (countEl) countEl.textContent = numberFormatter.format(count);
                if (bar) bar.style.width = `${total ? Math.min((count / total) * 100, 100) : 0}%`;
            });
        } catch (_) {
            // The server-rendered values remain visible if live refresh is unavailable.
        }
    };

    root.querySelectorAll("[data-stat]").forEach((el) => {
        el.dataset.current = String(Number(el.textContent.replace(/[^\d]/g, "")) || 0);
    });

    update();
    window.setInterval(update, 60000);
})();
