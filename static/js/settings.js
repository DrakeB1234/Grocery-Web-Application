// function for toggling mobile nav bar
window.onload = () => {
    const navEle = document.getElementById("mobile-nav-container")
    document.querySelectorAll("#toggle-mobile-nav").forEach(e => {
        e.addEventListener("click", (e) => {
            if (navEle.style.display === "flex"){
                navEle.style.display = "none";
                return;
            }
            navEle.style.display = "flex";
        });
    });
};