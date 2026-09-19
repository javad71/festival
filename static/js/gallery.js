(() => {
  const items = [...document.querySelectorAll('.gallery-item')];
  const box = document.getElementById('lightbox');
  if (!items.length || !box) return;
  const img = document.getElementById('lightboxImage');
  const caption = document.getElementById('lightboxCaption');
  let index = 0;
  const render = () => {
    const item = items[index];
    img.src = item.dataset.gallerySrc;
    img.alt = item.dataset.galleryTitle || '';
    caption.textContent = [item.dataset.galleryTitle, item.dataset.gallerySubtitle].filter(Boolean).join(' — ');
  };
  const open = i => { index = i; render(); box.classList.add('open'); box.setAttribute('aria-hidden','false'); document.body.classList.add('modal-open'); };
  const close = () => { box.classList.remove('open'); box.setAttribute('aria-hidden','true'); document.body.classList.remove('modal-open'); };
  items.forEach((item, i) => { item.addEventListener('click', () => open(i)); item.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(i); } }); });
  document.getElementById('lightboxClose')?.addEventListener('click', close);
  document.getElementById('lightboxPrev')?.addEventListener('click', () => { index = (index - 1 + items.length) % items.length; render(); });
  document.getElementById('lightboxNext')?.addEventListener('click', () => { index = (index + 1) % items.length; render(); });
  box.addEventListener('click', e => { if (e.target === box) close(); });
  document.addEventListener('keydown', e => { if (!box.classList.contains('open')) return; if (e.key === 'Escape') close(); if (e.key === 'ArrowLeft') document.getElementById('lightboxNext')?.click(); if (e.key === 'ArrowRight') document.getElementById('lightboxPrev')?.click(); });
})();
