const menuBtn = document.getElementById("mobileMenuBtn");
const nav = document.getElementById("mainNav");
menuBtn?.addEventListener("click", () => nav.classList.toggle("open"));
document.querySelectorAll("#mainNav a").forEach(a => a.addEventListener("click", () => nav.classList.remove("open")));
