// function for toggling mobile nav bar
document.querySelectorAll("#set-btn").forEach(e => {
    e.addEventListener("click", (e) => {
        // if next element in DOM is hidden
        if (e.originalTarget.nextElementSibling.style.display == "flex") {
            e.originalTarget.nextElementSibling.style.display = "none";
            return;
        }
        e.originalTarget.nextElementSibling.style.display = "flex";
    });
});