
// header.js

function handleRegister(select) {
    const url = select.value;
    if (url) {
        window.location.href = url; 
    }
}

function handleLogin(select) {
    const url = select.value;
    if (url) {
        window.location.href = url;
    }
}
const startButton = document.getElementById("startBtn");
if (startButton) {
    startButton.addEventListener("click", function (event) {
        event.preventDefault();
        fetch("/start_test")
            .then(res => {
                if (!res.ok) throw new Error("تعذر تسجيل بدء الاختبار");
                return res.text();
            })
            .then(() => { window.location.href = "/informtion"; })
            .catch(() => { window.location.href = "/informtion"; });
    });
}
document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.querySelector(".nav-toggle");
    const nav = document.getElementById("main-nav");
    if (!toggle || !nav) return;
    toggle.addEventListener("click", function () {
        const isOpen = nav.classList.toggle("is-open");
        toggle.setAttribute("aria-expanded", String(isOpen));
        toggle.innerHTML = isOpen
          ? '<i class="fa-solid fa-xmark" aria-hidden="true"></i>'
          : '<i class="fa-solid fa-bars" aria-hidden="true"></i>';
    });
    nav.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
            nav.classList.remove("is-open");
            toggle.setAttribute("aria-expanded", "false");
            toggle.innerHTML = '<i class="fa-solid fa-bars" aria-hidden="true"></i>';
        });
    });
});
