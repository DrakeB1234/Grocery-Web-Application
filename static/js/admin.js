// function for toggling mobile nav bar
const toggleContainer = (e) => {
    const nextContainer = e.target.nextElementSibling;
    if (nextContainer.style.display === "flex"){
        nextContainer.style.display = "none";
        return
    }
    nextContainer.style.display = "flex";
}