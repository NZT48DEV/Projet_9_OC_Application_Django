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
    // 🔹 Récupère la page actuelle dans l’URL (par défaut 1)
    const url = new URL(window.location.href);
    let currentPage = parseInt(url.searchParams.get("page") || "1", 10);

    // 🔹 La prochaine page à charger
    let page = currentPage + 1;
    let loading = false;

    const postsContainer = document.getElementById("posts-container");
    const loadingSpinner = document.getElementById("loading");

    if (!postsContainer) return;

    window.addEventListener("scroll", function onScroll() {
        if (loading) return;

        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 200) {
            loading = true;
            loadingSpinner.classList.remove("d-none");

            const url = new URL(window.location.href);
            url.searchParams.set("page", page);

            fetch(url.toString(), { headers: { "X-Requested-With": "XMLHttpRequest" } })
                .then(response => response.json())
                .then(data => {
                    if (data.html && data.html.trim() !== "") {
                        postsContainer.insertAdjacentHTML("beforeend", data.html);

                        if (typeof initToggleButtons === "function") {
                            initToggleButtons(postsContainer);
                        }

                        // Met à jour l’URL
                        const newUrl = new URL(window.location.href);
                        newUrl.searchParams.set("page", page);
                        window.history.pushState({}, "", newUrl.toString());
                    }

                    if (data.has_next) {
                        page++;
                        loading = false;
                    } else {
                        console.log("No more pages → stopping infinite scroll.");
                        window.removeEventListener("scroll", onScroll);
                    }
                })
                .finally(() => {
                    loadingSpinner.classList.add("d-none");
                });
        }
    });
});
