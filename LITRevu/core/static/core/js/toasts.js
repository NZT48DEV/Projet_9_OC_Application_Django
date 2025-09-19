document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.toast').forEach(toastEl => {
        const bsToast = new bootstrap.Toast(toastEl);
        bsToast.show();
    });
});
