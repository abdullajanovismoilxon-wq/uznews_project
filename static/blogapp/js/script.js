document.addEventListener("DOMContentLoaded", function () {
    // Navbar active class
    const navLinks = document.querySelectorAll(".nav-link, .dropdown-item");
    navLinks.forEach(link => {
        link.addEventListener("click", function () {
            navLinks.forEach(l => l.classList.remove("active"));
            this.classList.add("active");
        });
    });

    // Dropdown tanlangan nomni ko‘rsatish
    const categoryLinks = document.querySelectorAll(".category-link");
    const categoryToggle = document.getElementById("categoryDropdown");
    categoryLinks.forEach(link => {
        link.addEventListener("click", function () {
            categoryToggle.textContent = this.textContent; // tanlangan nomni tugmaga yozadi
        });
    });

    // Alert avtomatik yopilishi
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.display = "none";
        }, 5000);
    });

    // Live search (autocomplete)
    const searchInput = document.getElementById("searchInput");
    const suggestionsBox = document.getElementById("searchSuggestions");

    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const query = this.value.trim();
            if (query.length > 2) {
                fetch(`/search_suggestions/?q=${query}`)
                    .then(response => response.json())
                    .then(data => {
                        suggestionsBox.innerHTML = "";
                        data.forEach(item => {
                            const link = document.createElement("a");
                            link.href = `/post/${item.id}/`;
                            link.className = "list-group-item list-group-item-action";
                            link.textContent = item.title;
                            suggestionsBox.appendChild(link);
                        });
                    });
            } else {
                suggestionsBox.innerHTML = "";
            }
        });
    }
});
