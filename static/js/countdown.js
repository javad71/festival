(() => {
    const el = document.getElementById("countdown");
    if (!el) return;

    // The Jalali date 1405/10/01 is converted server-side conceptually to
    // the browser target timestamp. For Tehran's civil calendar, 1405/10/01
    // corresponds to 2026-12-22.
    const target = new Date("2026-12-22T00:00:00+03:30").getTime();

    const fields = {
        days: document.getElementById("days"),
        hours: document.getElementById("hours"),
        minutes: document.getElementById("minutes"),
        seconds: document.getElementById("seconds")
    };

    function tick() {
        const distance = target - Date.now();
        if (distance <= 0) {
            Object.values(fields).forEach(x => x.textContent = "۰۰");
            return;
        }
        const d = Math.floor(distance / 86400000);
        const h = Math.floor((distance % 86400000) / 3600000);
        const m = Math.floor((distance % 3600000) / 60000);
        const s = Math.floor((distance % 60000) / 1000);
        fields.days.textContent = String(d).padStart(2, "0");
        fields.hours.textContent = String(h).padStart(2, "0");
        fields.minutes.textContent = String(m).padStart(2, "0");
        fields.seconds.textContent = String(s).padStart(2, "0");
    }
    tick();
    setInterval(tick, 1000);
})();
