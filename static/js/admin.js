// function for toggling mobile nav bar
const toggleContainer = (e) => {
    const nextContainer = e.target.nextElementSibling;
    if (nextContainer.style.display === "flex"){
        e.target.style.backgroundColor = "var(--white-light)";
        nextContainer.style.display = "none";
        return
    }
    e.target.style.backgroundColor = "var(--white-med)";
    nextContainer.style.display = "flex";
}