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

// callable function allows for user validation for actions
const userConfirmAct = (e) => {
    const res = confirm("Are you sure you want to Continue?");
    if (res == true) {
        return true;
    }
    e.preventDefault()
}