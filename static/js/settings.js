// function for toggling mobile nav bar
document.querySelectorAll("#set-btn").forEach(e => {
    e.addEventListener("click", (e) => {
        // if next element in DOM is hidden
        const setContainer = e.target.parentElement.nextElementSibling;
        if (setContainer.style.display == "flex"){
            setContainer.style.display = "none";
            return;
        }
        setContainer.style.display = "flex";
    });
});