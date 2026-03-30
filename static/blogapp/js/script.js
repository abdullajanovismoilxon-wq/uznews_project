//document.addEventListener("DOMContentLoaded", function () {
//    // Navbar active class
//    const navLinks = document.querySelectorAll(".nav-link, .dropdown-item");
//    navLinks.forEach(link => {
//        link.addEventListener("click", function () {
//            navLinks.forEach(l => l.classList.remove("active"));
//            this.classList.add("active");
//        });
//    });
//
//    // Dropdown tanlangan nomni ko‘rsatish
//    const categoryLinks = document.querySelectorAll(".category-link");
//    const categoryToggle = document.getElementById("categoryDropdown");
//    categoryLinks.forEach(link => {
//        link.addEventListener("click", function () {
//            categoryToggle.textContent = this.textContent; // tanlangan nomni tugmaga yozadi
//        });
//    });
//
//    // Alert avtomatik yopilishi
//    const alerts = document.querySelectorAll(".alert");
//    alerts.forEach(alert => {
//        setTimeout(() => {
//            alert.style.display = "none";
//        }, 5000);
//    });
//
//    // Live search (autocomplete)
//    const searchInput = document.getElementById("searchInput");
//    const suggestionsBox = document.getElementById("searchSuggestions");
//
//    if (searchInput) {
//        searchInput.addEventListener("input", function () {
//            const query = this.value.trim();
//            if (query.length > 2) {
//                fetch(`/search_suggestions/?q=${query}`)
//                    .then(response => response.json())
//                    .then(data => {
//                        suggestionsBox.innerHTML = "";
//                        data.forEach(item => {
//                            const link = document.createElement("a");
//                            link.href = `/post/${item.id}/`;
//                            link.className = "list-group-item list-group-item-action";
//                            link.textContent = item.title;
//                            suggestionsBox.appendChild(link);
//                        });
//                    });
//            } else {
//                suggestionsBox.innerHTML = "";
//            }
//        });
//    }
//    const loadMoreBtn = document.getElementById("loadMoreBtn");
//    if (loadMoreBtn) {
//        loadMoreBtn.addEventListener("click", function(e) {
//        e.preventDefault();
//        const url = this.getAttribute("data-url");
//
//        fetch(url)
//            .then(response => response.text())
//            .then(data => {
//            const parser = new DOMParser();
//            const doc = parser.parseFromString(data, "text/html");
//            const newPosts = doc.querySelectorAll("#postContainer .post-card");
//            const postContainer = document.getElementById("postContainer");
//
//            newPosts.forEach(post => postContainer.appendChild(post));
//
//            const newBtn = doc.querySelector("#loadMoreBtn");
//            if (newBtn) {
//                this.setAttribute("href", newBtn.getAttribute("href"));
//                this.setAttribute("data-url", newBtn.getAttribute("data-url"));
//            } else {
//                this.remove();
//            }
//            });
//        });
//    }
//    // Detail sahifada "Shu kabi" uchun
//    const loadMoreRelated = document.getElementById("loadMoreRelated");
//    if (loadMoreRelated) {
//        loadMoreRelated.addEventListener("click", function(e) {
//            e.preventDefault();
//            const url = this.getAttribute("data-url");
//
//            fetch(url)
//                .then(response => response.text())
//                .then(data => {
//                    const parser = new DOMParser();
//                    const doc = parser.parseFromString(data, "text/html");
//                    const newPosts = doc.querySelectorAll("#relatedContainer .col-md-4");
//                    const relatedContainer = document.getElementById("relatedContainer");
//
//                    newPosts.forEach(post => relatedContainer.appendChild(post));
//
//                    const newBtn = doc.querySelector("#loadMoreRelated");
//                    if (newBtn) {
//                        this.setAttribute("href", newBtn.getAttribute("href"));
//                        this.setAttribute("data-url", newBtn.getAttribute("data-url"));
//                    } else {
//                        this.remove();
//                    }
//                });
//        });
//    }
//    tinymce.init({
//        selector: '#post_body',
//        height: 500,
//        plugins: 'image link media table code',
//        toolbar: 'undo redo | bold italic | alignleft aligncenter alignright | image media link | code',
//        images_upload_url: '/upload/',
//        automatic_uploads: true,
//        file_picker_types: 'image',
//        file_picker_callback: function (callback, value, meta) {
//            var input = document.createElement('input');
//            input.setAttribute('type', 'file');
//            input.setAttribute('accept', 'image/*');
//            input.onchange = function () {
//            var file = this.files[0];
//            var reader = new FileReader();
//            reader.onload = function () {
//                callback(reader.result, { alt: file.name });
//            };
//            reader.readAsDataURL(file);
//            };
//            input.click();
//        }
//        });
//});
document.addEventListener("DOMContentLoaded", function () {

    /* =======================
       🚫 FORMGA TEGMAYMIZ
    ======================== */
    // Form submitni hech qachon bloklamaymiz
    const forms = document.querySelectorAll("form");
    forms.forEach(form => {
        form.addEventListener("submit", function () {
            // TinyMCE bo‘lsa contentni saqlaydi
            if (typeof tinymce !== "undefined") {
                tinymce.triggerSave();
            }
        });
    });


    /* =======================
       ✅ NAVBAR ACTIVE
    ======================== */
    const navLinks = document.querySelectorAll(".nav-link, .dropdown-item");

    navLinks.forEach(link => {
        link.addEventListener("click", function () {
            navLinks.forEach(l => l.classList.remove("active"));
            this.classList.add("active");
        });
    });


    /* =======================
       ✅ CATEGORY DROPDOWN
    ======================== */
    const categoryLinks = document.querySelectorAll(".category-link");
    const categoryToggle = document.getElementById("categoryDropdown");

    if (categoryToggle) {
        categoryLinks.forEach(link => {
            link.addEventListener("click", function () {
                categoryToggle.textContent = this.textContent;
            });
        });
    }


    /* =======================
       ✅ ALERT AUTO HIDE
    ======================== */
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.display = "none";
        }, 5000);
    });


    /* =======================
       ✅ LIVE SEARCH
    ======================== */
    const searchInput = document.getElementById("searchInput");
    const suggestionsBox = document.getElementById("searchSuggestions");

    if (searchInput && suggestionsBox) {
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


    /* =======================
       ✅ LOAD MORE (POST LIST)
    ======================== */
    const loadMoreBtn = document.getElementById("loadMoreBtn");
    if (newBtn) {
        this.setAttribute("data-url", newBtn.getAttribute("data-url"));
    } else {
        this.remove();
    }

    if (loadMoreBtn) {
        loadMoreBtn.addEventListener("click", function (e) {
            e.preventDefault();
            const url = this.getAttribute("data-url");

            fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(response => response.text())
                .then(data => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(data, "text/html");

                    const newPosts = doc.querySelectorAll(".post-card");
                    const postContainer = document.getElementById("postContainer");

                    newPosts.forEach(post => postContainer.appendChild(post));

                    const newBtn = doc.querySelector("#loadMoreBtn");
                    if (newBtn) {
                        this.setAttribute("data-url", newBtn.getAttribute("data-url"));
                    } else {
                        this.remove();
                    }
                });
        });
    }


    /* =======================
       ✅ LOAD MORE RELATED
    ======================== */
    const loadMoreRelated = document.getElementById("loadMoreRelated");

    if (loadMoreRelated) {
        loadMoreRelated.addEventListener("click", function (e) {
            e.preventDefault();

            const url = this.getAttribute("data-url");

            fetch(url)
                .then(response => response.text())
                .then(data => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(data, "text/html");

                    const newPosts = doc.querySelectorAll("#relatedContainer .col-md-4");
                    const container = document.getElementById("relatedContainer");

                    newPosts.forEach(post => container.appendChild(post));

                    const newBtn = doc.querySelector("#loadMoreRelated");

                    if (newBtn) {
                        this.setAttribute("data-url", newBtn.getAttribute("data-url"));
                    } else {
                        this.remove();
                    }
                });
        });
    }


    /* =======================
       ✅ TINYMCE INIT (XAVFSIZ)
    ======================== */
    if (typeof tinymce !== "undefined") {
    tinymce.init({
        selector: '#post_body',
        height: 500,
        plugins: 'linktable code',
        toolbar: 'undo redo | bold italic | alignleft aligncenter alignright | link | code',
        images_upload_url: '/upload/',
        automatic_uploads: true,
        file_picker_types: 'image',

        file_picker_callback: function (callback, value, meta) {
            var input = document.createElement('input');
            input.setAttribute('type', 'file');
            input.setAttribute('accept', 'image/*');

            input.onchange = function () {
                var file = this.files[0];
                var reader = new FileReader();

                reader.onload = function () {
                    callback(reader.result, { alt: file.name });
                };

                reader.readAsDataURL(file);
            };

            input.click();
        },

        // 🔥 ENG MUHIM QO‘SHIMCHA
        setup: function (editor) {
            editor.on('change keyup', function () {
                editor.save(); // textarea ga yozadi
            });
        }
    });
}

});