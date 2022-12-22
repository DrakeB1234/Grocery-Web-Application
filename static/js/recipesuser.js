// function to handle each recipe double click
const toggleRecipe = (e) => {
    console.log(e.target.nextElementSibling)
}

// function for toggling settings nav
const editRecipe = (id) => {
    const container = document.getElementById('container-edit')
    // get data by recipe ID
    if (container.style.display !== "flex") {
        data.forEach(e => {
            if (e["recipe_id"] == id){
                // form html to edit
                html = `
                <form action="/recipesmod" method="post" onsubmit="userConfirmAct(event, 'edit')" enctype="multipart/form-data">
                <div id="closeContainer" onclick="editRecipe(0)">
                <i class="fa-solid fa-chevron-left"></i>
                <h2>Return</h2>
                </div>
                <h1>Edit ${e["recipe_name"]}</h1>
                <input name="recipeEditID" value="${e["recipe_id"]}" hidden />
                <input name="recipeEditTitle" type="text" placeholder="${e["recipe_name"]}" pattern="^[a-zA-Z][a-zA-Z ]*$" title="Only use letters and spaces" autocomplete="off" />
                <input name="recipeEditLink" type="url" placeholder="Reference Link: ${e["outer_link"]}" autocomplete="off" />
                <select name="recipeEditCourse">
                    <option selected hidden value="">${e["course"]}</option>
                    <option value="Breakfast">Breakfast</option>
                    <option value="Lunch">Lunch</option>
                    <option value="Dinner">Dinner</option>
                    <option value="Snack">Snack</option>
                    <option value="Dessert">Dessert</option>
                </select>
                <input name="recipeEditCategory" type="text" placeholder="${e["category"]}" pattern="^[a-zA-Z][a-zA-Z ]*$" title="Only use letters and spaces" autocomplete="off" />
                <textarea name="recipeEditDescription" placeholder="${e["description"]}" pattern="^[a-zA-Z0-9][a-zA-Z0-9!?.,' ]*$" title="Only use letters, numbers, spaces, and ! ? . , - '" autocomplete="off"></textarea>
                <h3>^ Note: Only use ( ! ? . , ' ) will NOT autocheck</h3>

                <h2>Recipe Cover Image</h2>
                <label for="file" class="btn">Select Image</label>
                <input id="file" name="avatarFile" style="visibility:hidden;" type="file" accept=".jpg, .jpeg, .png">`

                html += `<h2 style="align-self: flex-start;">Ingredients</h2>`
                let index = 1
                ingredients.forEach(ele => {
                    if (ele["recipe_id"] == e["recipe_id"]) {
                        html += `
                        <div class="input-list">
                            <div class="container-input">
                                <input name="recipeIngredientsID" value="${ele['ingredients_id']}" hidden >
                                <h1>Ingredient ${index}:</h1>
                                <input name="recipeIngredients" type="text" placeholder="${ele['ingredient_name']}" autocomplete="off" pattern="^[a-zA-Z][a-zA-Z ]*$" title="Only use letters and spaces" />
                                <input name="recipeMeasure" type="text" placeholder="${ele['ingredient_measure']}" autocomplete="off" pattern="^[a-zA-Z0-9][a-zA-Z0-9\/\- ]*$" title="Only use letters, numbers, spaces, and / -" />
                                <hr>
                            </div>
                        </div>`
                        index++;
                    }
                })

                html += `<h2 style="align-self: flex-start;">Instructions</h2>`
                index = 1
                instructions.forEach(ele => {
                    
                    if (ele["recipe_id"] == e["recipe_id"]) {
                        html += `
                        <div class="input-list">
                            <div class="container-input">
                                <input name="recipeInstructionsID" value="${ele['instructions_id']}" hidden >
                                <h1>Step ${index}:</h1>
                                <input name="recipeInstructions" type="text" placeholder="${ele['instructions_name']}" autocomplete="off" pattern="^[a-zA-Z0-9][a-zA-Z0-9!\-,./()' ]*$" title="Only use letters, numbers, spaces, and ! . , ' /- ( )" />
                                <hr>
                            </div>
                        </div>`
                        index++;
                    }
                })

                html += `
                <button type="submit">Save Changes</button>
                </form>
                `
                container.innerHTML = html;
                container.style.display = "flex"
            }
        });
        return
    }
    // otherwise, function call is to close container
    container.style.display = "none"
    return
};