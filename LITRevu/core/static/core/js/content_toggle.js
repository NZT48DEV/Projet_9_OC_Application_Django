/**
 * Gestion des boutons "Voir plus / Voir moins" pour les contenus longs.
 *
 * Fonctionnement :
 * - Fournit une fonction initToggleButtons(scope) pour initialiser les boutons dans un élément donné.
 * - Alterne la classe CSS `.clamp` sur l’élément cible pour afficher/cacher le contenu complet.
 * - Met à jour le texte et les classes du bouton en fonction de l'état (voir plus / voir moins).
 * - Cache automatiquement les boutons qui ne sont pas nécessaires (contenu trop court).
 *
 * Utilisation :
 * - Appelé une première fois au chargement (DOMContentLoaded).
 * - Peut être rappelé après insertion dynamique (par ex. infinite scroll).
 */

/**
 * Initialise les boutons "Voir plus / Voir moins" dans une zone donnée.
 * @param {HTMLElement} scope - Élément dans lequel chercher les boutons (par défaut document).
 */
function initToggleButtons(scope = document) {
  scope.querySelectorAll(".toggle-btn").forEach(btn => {
    const target = btn.closest(".card").querySelector(btn.dataset.target);  // ✅ correction

    if (!target) return;

    const updateButtonVisibility = () => {
      if (target.scrollHeight <= target.clientHeight) {
        btn.style.display = "none";
      } else {
        btn.style.display = "inline-block"; // utile si recalcul et bouton doit apparaître
      }
    };

    // Vérifie d'abord
    updateButtonVisibility();

    // Vérifie aussi après chargement des images dans la zone
    target.querySelectorAll("img").forEach(img => {
      img.addEventListener("load", updateButtonVisibility);
    });

    // Supprime d’anciens listeners pour éviter les doublons
    btn.removeEventListener("click", btn._toggleHandler);

    // Définit un nouveau handler
    btn._toggleHandler = () => {
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
    };

    btn.addEventListener("click", btn._toggleHandler);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initToggleButtons();
  // Vérifie à nouveau après que tout est chargé
  window.addEventListener("load", () => initToggleButtons());
});
