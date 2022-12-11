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
const userConfirmAct = (e, msg) => {
    // ensure input needs confirm
    if (msg == "skip"){
        // display loading container
        document.getElementById("container-loading").style.display = 'flex';
        return true;
    }
    const res = confirm(`Are you sure you want to ${msg} this?`);
    if (res == true) {
        // display loading container
        document.getElementById("container-loading").style.display = 'flex';
        return true;
    }
    e.preventDefault()
}