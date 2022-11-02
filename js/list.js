// hide/show add container
document.getElementById('show-add-btn').addEventListener('click', () => {
    const addContainer = document.getElementById('form-add');
    const addBtn = document.getElementById('show-add-btn');
    if (!(addContainer.classList.contains('show'))) {
        addContainer.classList.add('show');
        addBtn.classList.add('rotate');
        return;
    }
    addBtn.classList.remove('rotate');
    addContainer.classList.remove('show');
});
