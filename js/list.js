
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

// hide/show manage container
document.getElementById('manage-button').addEventListener('click', () => {
    const manageContainer = document.getElementById('manage-container');
    const manageButton = document.getElementById('manage-button');
    if (manageContainer.style.display == 'block') {
        manageContainer.style.display = 'none';
        manageButton.classList.remove('rotate');
        return;
    }
    manageButton.classList.add('rotate');
    manageContainer.style.display = 'block';
});

// hide/show add container
document.getElementById('add-category-button').addEventListener('click', () => {
    const addContainer = document.getElementById('form-add-category');
    if (addContainer.style.display == 'flex') {
        addContainer.style.display = 'none';
        return;
    }
    addContainer.style.display = 'flex';
});
