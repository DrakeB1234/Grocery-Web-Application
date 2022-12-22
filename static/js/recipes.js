// function for toggling settings nav
document.querySelectorAll("#toggleAddContainer").forEach(e => {
    e.addEventListener("click", () => {
        // if next element in DOM is hidden
        const setContainer = document.getElementById("recipe-adder");
        if (setContainer.style.display == "flex"){
            setContainer.style.display = "none";
            return;
        }
        setContainer.style.display = "flex";
    });
});

// function for adding additional inputs
// setting global var
let ingreIndex = 2
let instruIndex = 2
const addInput = (e, type) => {
    const ingredientInput = document.createElement("div");
    ingredientInput.classList.add("container-input");

    // check if type added was ingredient or instruction
    if (type == "instruction"){
        const regex = "^[a-zA-Z0-9][a-zA-Z0-9!\-,./' ]*$"
        ingredientInput.innerHTML = `<h1>Step ${instruIndex}:</h1>
        <input name="recipeInstructions"
        type="text" placeholder="Instruction" autocomplete="off" 
        pattern="${regex}" title="Only use letters, numbers, spaces, and ! . , / -" required >
        <hr>
        `;
        // increment index
        instruIndex++;
    }
    else {
        // set element to instruction input
        ingredientInput.innerHTML = `<h1>Ingredient ${ingreIndex}:</h1>
        <input name="recipeIngredients"
        type="text" placeholder="Ingredient" autocomplete="off"
        pattern="^[a-zA-Z][a-zA-Z ]*$" title="Only use letters and spaces" required>
        <input name="recipeMeasure"
        type="text" placeholder="Amount" autocomplete="off"
        pattern="^[a-zA-Z0-9][a-zA-Z0-9\\/\\- ]*$" title="Only use letters, numbers, spaces, and - /" required>
        <hr>
        `;

        // increment index
        ingreIndex++;
    }

    // append child to parent element
    e.target.parentElement.previousElementSibling.appendChild(ingredientInput);
    return
};

const removeInput = (e, type) => {
    // remove child element based on target
    if (e.target.parentElement.previousElementSibling.children.length > 1){
    e.target.parentElement.previousElementSibling.removeChild(e.target.parentElement.previousElementSibling.lastChild)

    // decrement value based on type that was removed
    if (type == "instruction"){
        instruIndex--;
        return
    }
    ingreIndex--;
    return
    }
}