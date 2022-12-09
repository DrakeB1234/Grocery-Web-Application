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

// function for toggling add container
document.getElementById("add-btn").addEventListener("click", e => {
    const addContainer = document.getElementById("container-add")
    if (addContainer.style.display === "flex"){
        addContainer.style.display = "none";
        e.target.style.rotate = "0deg";
        return;
    }
    addContainer.style.display = "flex";
    e.target.style.rotate = "-45deg";
});