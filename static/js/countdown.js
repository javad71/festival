(() => {
    const card = document.querySelector('.festival-state-card');
    const el = document.getElementById('countdown');
    if (!card || !el) return;
    const phase = card.dataset.phase;
    if (phase !== 'countdown') {
        const title = card.querySelector('.countdown-title');
        if (phase === 'festival') title.textContent = '🎉 جشنواره اکنون در حال برگزاری است';
        if (phase === 'winners') title.textContent = '🏆 جشنواره به مرحله اعلام نتایج رسیده است';
        return;
    }
    const target = new Date(`${card.dataset.start}T00:00:00+03:30`).getTime();
    const fields = {days: document.getElementById('days'), hours: document.getElementById('hours'), minutes: document.getElementById('minutes'), seconds: document.getElementById('seconds')};
    function tick() {
        const distance = target - Date.now();
        if (distance <= 0) { location.reload(); return; }
        const d = Math.floor(distance / 86400000), h = Math.floor((distance % 86400000) / 3600000), m = Math.floor((distance % 3600000) / 60000), s = Math.floor((distance % 60000) / 1000);
        fields.days.textContent = String(d).padStart(2,'0'); fields.hours.textContent = String(h).padStart(2,'0'); fields.minutes.textContent = String(m).padStart(2,'0'); fields.seconds.textContent = String(s).padStart(2,'0');
    }
    tick(); setInterval(tick, 1000);
})();
