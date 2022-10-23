// function for hiding the introduction text, then
// showing main content on user scroll

// detects scroll from user
window.onscroll = () => {
    let userScroll = false;
    if (userScroll == false) {
        const introElement = document.querySelector('.introduction-container');
        const mainElement = document.querySelector('.main-container-grid');
        // remove show class, add hide class to intro div
        introElement.classList.remove("show");
        introElement.classList.add("hide-intro");
        // remove hide class, add show class to main div
        mainElement.classList.remove("hide-main");
        mainElement.classList.add("show");
        console.log(mainElement);
    } else {
        userScroll = true;
    }
}
