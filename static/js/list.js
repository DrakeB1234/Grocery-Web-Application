// function for toggling mobile nav bar
document.querySelectorAll("#set-btn").forEach(e => {
    e.addEventListener("click", (e) => {
        // if next element in DOM is hidden
        const setContainer = e.target.parentElement.nextElementSibling;
        if (setContainer.style.display == "flex"){
            setContainer.style.display = "none";
            e.target.parentElement.style.backgroundColor = "var(--white-light)";
            return;
        }
        // close every other sublist
        document.querySelectorAll(".sub-list").forEach(e => {
            e.style.display = "none";
            e.previousElementSibling.style.backgroundColor = "var(--white-light)";
        })
        // display selected container
        setContainer.style.display = "flex";
        e.target.parentElement.style.backgroundColor = "var(--white-med)";
    });
});