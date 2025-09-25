/**
 * Aperçu dynamique de l’image uploadée dans un formulaire.
 *
 * Fonctionnement :
 * - Écoute le champ input `#id_image`.
 * - Lorsqu’un fichier est sélectionné, il est lu via FileReader.
 * - L’aperçu est affiché dans l’élément <img id="preview">.
 * - Le texte alternatif (#no-image) est masqué si une image est sélectionnée.
 *
 * Pré-requis dans le template :
 * - <input type="file" id="id_image">
 * - <img id="preview" style="display:none;">
 * - <p id="no-image">Pas d’image sélectionnée</p> (optionnel)
 */
document.addEventListener("DOMContentLoaded", function () {
    const input = document.querySelector("#id_image");
    const preview = document.getElementById("preview");
    const noImageText = document.getElementById("no-image");

    if (!input) {
        console.error("❌ Champ image introuvable !");
        return;
    }

    input.addEventListener("change", function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = "block";
                if (noImageText) {
                    noImageText.style.display = "none";
                }
            };

            reader.readAsDataURL(file);
        }
    });
});
