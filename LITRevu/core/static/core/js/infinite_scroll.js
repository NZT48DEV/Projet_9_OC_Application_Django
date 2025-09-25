/**
 * Gestion du scroll infini pour les posts.
 *
 * Fonctionnement :
 * - Quand l'utilisateur arrive en bas de la page, une requête AJAX est envoyée
 *   vers l'URL courante avec un paramètre `page` incrémenté.
 * - Le backend renvoie un fragment HTML avec les posts de la page demandée.
 * - Les nouveaux posts sont insérés dans le conteneur `#posts-container`.
 * - Les boutons "Voir plus / Voir moins" sont initialisés pour le contenu ajouté.
 * - L'URL visible dans le navigateur est mise à jour via `history.pushState`
 *   (exemple : ?page=2, ?page=3...), sans rechargement complet de la page.
 * - Quand il n'y a plus de page suivante (`has_next == false`),
 *   le scroll infini est désactivé pour éviter les doublons.
 */
document.addEventListener("DOMContentLoaded", () => {
    let page = 2;         // Numéro de la prochaine page à charger
    let loading = false;  // Flag pour éviter les requêtes multiples simultanées

    const postsContainer = document.getElementById("posts-container");
    const loadingSpinner = document.getElementById("loading");

    if (!postsContainer) return;

    window.addEventListener("scroll", function onScroll() {
        if (loading) return;

        // Déclenche quand on arrive proche du bas de la page
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 200) {
            loading = true;
            loadingSpinner.classList.remove("d-none");

            // 🔹 Construit l’URL en gardant les paramètres existants (filter, etc.)
            const url = new URL(window.location.href);
            url.searchParams.set("page", page);

            fetch(url.toString(), {
                headers: { "X-Requested-With": "XMLHttpRequest" }
            })
                .then(response => response.json())
                .then(data => {
                    // ✅ Toujours ajouter la page reçue
                    if (data.html && data.html.trim() !== "") {
                        postsContainer.insertAdjacentHTML("beforeend", data.html);

                        // ✅ Réinitialise les boutons Voir plus / Voir moins pour le contenu ajouté
                        if (typeof initToggleButtons === "function") {
                            initToggleButtons(postsContainer);
                        }

                        // ✅ Met à jour l'URL visible dans le navigateur
                        const newUrl = new URL(window.location.href);
                        newUrl.searchParams.set("page", page);
                        window.history.pushState({}, "", newUrl.toString());
                    }

                    // Vérifie si une autre page existe
                    if (data.has_next) {
                        page++;
                        loading = false;
                    } else {
                        console.log("No more pages → stopping infinite scroll.");
                        // ✅ Arrêter l’écouteur scroll
                        window.removeEventListener("scroll", onScroll);
                    }
                })
                .finally(() => {
                    loadingSpinner.classList.add("d-none");
                });
        }
    });
});
