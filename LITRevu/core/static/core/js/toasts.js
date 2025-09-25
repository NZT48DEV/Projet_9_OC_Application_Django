/**
 * Gestion des notifications Bootstrap Toasts.
 *
 * Fonctionnement :
 * - Attend que le DOM soit chargé (DOMContentLoaded).
 * - Sélectionne tous les éléments `.toast` présents dans la page.
 * - Initialise un toast Bootstrap pour chacun et l’affiche automatiquement.
 *
 * Utilisation :
 * - Dans tes templates Django, ajoute un bloc <div class="toast"> pour afficher
 *   une notification (ex: messages de succès, erreur, info...).
 * - Ce script s’assure que tous les toasts sont affichés dès le chargement.
 */

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".toast").forEach((toastEl) => {
        const bsToast = new bootstrap.Toast(toastEl);
        bsToast.show();
    });
});
