document.addEventListener("DOMContentLoaded", () => {
    setupTabNavigation();
});


function setupTabNavigation() {
    const tabLinks = document.querySelectorAll(".tab-link");
    const tabContents = document.querySelectorAll(".tab-content");

    tabLinks.forEach(link => {
        link.addEventListener("click", (event) => {
            event.preventDefault();
            const targetTab = event.target.getAttribute("data-tab");

            // Sembunyikan semua tab
            tabContents.forEach(content => content.style.display = "none");

            // Tampilkan tab yang sesuai
            document.getElementById(targetTab).style.display = "block";
        });
    });

    // Tampilkan tab pertama secara default
    document.getElementById("beranda").style.display = "block";
}



