document.addEventListener("DOMContentLoaded", () => {
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

    // Active l’autocomplete pour les deux champs
    setupAutocomplete("search-user-follow", "suggestions-follow", "follow");
    setupAutocomplete("search-user-block", "suggestions-block", "block");
});
