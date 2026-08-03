const toggleBtn = document.getElementById("theme-toggle");

const body = document.body;

// Load saved theme
if (localStorage.getItem("theme") === "dark") {
    body.classList.add("dark-mode");
    toggleBtn.innerHTML = "☀️ Light Mode";
}

toggleBtn.addEventListener("click", () => {

    body.classList.toggle("dark-mode");

    if (body.classList.contains("dark-mode")) {

        localStorage.setItem("theme", "dark");

        toggleBtn.innerHTML = "☀️ Light Mode";

    } else {

        localStorage.setItem("theme", "light");

        toggleBtn.innerHTML = "🌙 Dark Mode";

    }

});