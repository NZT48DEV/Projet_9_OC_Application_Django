document.addEventListener("DOMContentLoaded", () => {
    const toastElList = document.querySelectorAll('.toast');
    toastElList.forEach((toastEl) => {
        const bsToast = new bootstrap.Toast(toastEl, { autohide: true, delay: 3000 });
        bsToast.show();
    });
});
