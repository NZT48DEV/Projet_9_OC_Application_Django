document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ toasts.js chargé !");
    const toastElList = document.querySelectorAll('.toast');
    toastElList.forEach((toastEl) => {
        console.log("Toast trouvé :", toastEl);
        const bsToast = new bootstrap.Toast(toastEl, { autohide: true, delay: 3000 });
        bsToast.show();
    });
});
