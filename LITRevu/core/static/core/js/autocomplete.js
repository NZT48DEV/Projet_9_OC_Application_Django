document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("search-user");
    const suggestions = document.getElementById("suggestions");

    if (!input || !suggestions) return; // évite les erreurs sur d'autres pages

    input.addEventListener("input", () => {
        const query = input.value.trim();
        if (query.length > 0) {
            fetch(`/search-users/?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    suggestions.innerHTML = "";
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
                });
        } else {
            suggestions.innerHTML = "";
        }
    });
});
