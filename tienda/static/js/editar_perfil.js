function toggleForm() {
    var form = document.getElementById("editar-perfil-form");
    var overlay = document.getElementById("overlay");
    if (form.style.display === "block") {
        form.style.display = "none";
        overlay.style.display = "none";
    } else {
        form.style.display = "block";
        overlay.style.display = "block";
    }
}

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("editar-perfil-btn").addEventListener("click", toggleForm);
});