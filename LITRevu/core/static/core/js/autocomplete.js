/**
 * Autocomplétion pour la recherche d’utilisateurs (abonnements & blocages).
 *
 * Fonctionnement :
 * - Chaque champ input (#search-user-follow et #search-user-block) déclenche
 *   une requête AJAX (fetch) vers `/search-users/` avec les paramètres :
 *   - q : valeur saisie
 *   - type : "follow" ou "block" selon le contexte
 * - Les résultats sont affichés dans une liste <ul>.
 * - Cliquer sur une suggestion remplit le champ input et efface la liste.
 *
 * Pré-requis dans le template :
 * - <input id="search-user-follow"> + <ul id="suggestions-follow">
 * - <input id="search-user-block"> + <ul id="suggestions-block">
 */
document.addEventListener("DOMContentLoaded", () => {
    /**
     * Initialise un champ d’autocomplétion.
     * @param {string} inputId - ID du champ input texte.
     * @param {string} suggestionsId - ID de la liste <ul> pour afficher les résultats.
     * @param {string} type - Contexte ("follow" ou "block").
     */
    function setupAutocomplete(inputId, suggestionsId, type) {
        const input = document.getElementById(inputId);
        const suggestions = document.getElementById(suggestionsId);

        if (!input || !suggestions) {
            return;
        }

        input.addEventListener("input", () => {
            const query = input.value.trim();

            if (query.length > 0) {
                fetch(`/search-users/?q=${encodeURIComponent(query)}&type=${type}`)
                    .then(response => response.json())
                    .then(data => {
                        suggestions.innerHTML = "";

                        if (data.length === 0) {
                            const li = document.createElement("li");
                            li.classList.add("list-group-item", "text-muted");
                            li.textContent = "Aucun utilisateur trouvé";
                            suggestions.appendChild(li);
                        } else {
                            data.forEach(user => {
                                const li = document.createElement("li");
                                li.classList.add("list-group-item", "list-group-item-action");
                                li.textContent = user.username;

                                // Lorsqu’on clique sur une suggestion
                                li.addEventListener("click", () => {
                                    input.value = user.username;
                                    suggestions.innerHTML = "";
                                });

                                suggestions.appendChild(li);
                            });
                        }
                    })
                    .catch(err => {
                        console.error("❌ Erreur fetch :", err);
                    });
            } else {
                suggestions.innerHTML = "";
            }
        });
    }

    // 🔹 Active l’autocomplete pour les deux champs
    setupAutocomplete("search-user-follow", "suggestions-follow", "follow");
    setupAutocomplete("search-user-block", "suggestions-block", "block");
});
