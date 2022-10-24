// function for hiding the introduction text, then
// showing main content on user scroll

window.onload = () => {
    window.document.addEventListener('scroll', introductionHide);
}

// detects scroll from user
const introductionHide = () => {
    // get classes of respected elements
    const introElement = document.querySelector('.introduction-container');
    const mainElement = document.querySelector('.main-container-grid');
    // remove show class, add hide class to intro div
    introElement.classList.add("hide-intro");
    // remove hide class, add show class to main div
    mainElement.classList.remove("hide-main");
    // this removes the event listener from window
    window.document.removeEventListener('scroll', introductionHide);
}