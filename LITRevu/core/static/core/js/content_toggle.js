document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".toggle-btn").forEach(btn => {
    const target = document.querySelector(btn.dataset.target);

    // Cache le bouton si pas besoin
    if (target.scrollHeight <= target.clientHeight) {
      btn.style.display = "none";
      return;
    }

    btn.addEventListener("click", () => {
      target.classList.toggle("clamp");

      if (target.classList.contains("clamp")) {
        btn.textContent = "Voir plus";
        btn.classList.remove("btn-secondary");
        btn.classList.add("btn-primary");
      } else {
        btn.textContent = "Voir moins";
        btn.classList.remove("btn-primary");
        btn.classList.add("btn-secondary");
      }
    });
  });
});
