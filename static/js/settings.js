// function for toggling mobile nav bar
window.onload = () => {
    document.querySelectorAll("#set-btn").forEach(e => {
        e.addEventListener("click", (e) => {
            // set the original target element
            let nextEle = e.originalTarget
            console.log(nextEle)
            // if next element in DOM is hidden
            if (nextEle.nextElementSibling.style.display == "flex") {
                nextEle.nextElementSibling.style.display = "none";
                nextEle = "";
                return;
            }
            nextEle.nextElementSibling.style.display = "flex";
            nextEle = "";
        });
    });
};