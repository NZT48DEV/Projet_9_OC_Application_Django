document.addEventListener("DOMContentLoaded", function () {
    const input = document.querySelector("#id_image");  
    const preview = document.getElementById("preview");
    const noImageText = document.getElementById("no-image");

    if (!input) {
        console.error("Champ image introuvable !");
        return;
    }

    input.addEventListener("change", function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = "block";
                if (noImageText) noImageText.style.display = "none";
            };
            reader.readAsDataURL(file);
        }
    });
});
