// function for handling item edit
// global var for storing previous html
let tempHTML = ""
const mealEdit = (e, mealID) => {
    // if tempHTML has not been set, then set it and replace div with form
    if (tempHTML == ""){

        tempHTML = e.target.parentElement.parentElement.innerHTML;
        // get form HTML to set div to it
        const formHTML = `
        <form id="mealEditForm" action="/mealplannermod" method="post" onsubmit="userConfirmAct(event, 'edit')">
            <h1>Edit Meal</h1>
            <input name="mealID" value="${mealID}" hidden />
            <input name="mealEditItem" type="text" placeholder="Meal" pattern="^[a-zA-Z][a-zA-Z ]*$" title="Only use letters and spaces" autocomplete="off" required />
            <div class="container-input">
                <button type="button" onclick="mealEdit(event, 'cancel')">Cancel</button>
                <button type="submit" >Edit</button>
            </div>
        </form>
        `;

        e.target.parentElement.parentElement.innerHTML = formHTML;
        return
    }
    // else, change ele if cancel button is pressed
    else if (mealID == "cancel"){
        e.target.parentElement.parentElement.parentElement.innerHTML = tempHTML;
        tempHTML = "";
        return
    }
    // if another ele is dbl clicked, stop operation until other is cancelled
    return
}