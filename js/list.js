
// hide/show add container
document.getElementById('add-button').addEventListener('click', () => {
    const addContainer = document.getElementById('input-container');
    const addButton = document.getElementById('add-button');
    if (addContainer.style.display == 'flex') {
        addContainer.style.display = 'none';
        addButton.classList.remove('rotate');
        return;
    }
    addButton.classList.add('rotate');
    addContainer.style.display = 'flex';
});