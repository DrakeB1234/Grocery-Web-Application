(function () {
    // go through each object
    let html = "";
    // get first category in list
    let pastCat = "";
    listdata.forEach(e => {
        let curCat = e["category"];
        // if cur cat is different than past
        if (curCat != pastCat) {
            html += `</div>`;
            html += `<h1>${curCat}</h1>`;
        }

        // print each item in format
        // if there is a note, print h4 tag with it
        if (e["note"] != "") {
            html += `<div class='container-item'><h2>${e["amount"]}</h2><h3 ondblclick="listItemEdit(event, ${e["id"]})">${e["item"]}</h3>\
            <form id="item-del" action="/listviewmod" method="post" onsubmit="userConfirmAct(event, 'delete')">
            <button name="itemDel" value="${e["id"]}" type="submit"><img src="../static/images/icons/icon-trash.svg"></button>\
            </form>`;
            html += `</div><h4>^ Note: ${e["note"]}</h4>`;
        }
        else {
            html += `<div class='container-item'><h2>${e["amount"]}</h2><h3 ondblclick="listItemEdit(event, ${e["id"]})">${e["item"]}</h3>\
            <form id="item-del" action="/listviewmod" method="post" onsubmit="userConfirmAct(event, 'delete')">
            <button name="itemDel" value="${e["id"]}" type="submit"><img src="../static/images/icons/icon-trash.svg"></button>\
            </form>`;
            html += `</div>`;
        }

        // set past cat
        pastCat = e["category"];
    });
    // post data to document
    document.getElementById("listdata-get").innerHTML = html;
})();

// function for handling item edit
// global var for storing previous html
let tempHTML = ""
const listItemEdit = (e, itemID) => {
    // if tempHTML has not been set, then set it and replace div with form
    if (tempHTML == ""){
        tempHTML = e.target.parentElement.innerHTML;
        // get list data for current itemID
        let curItem = "";
        listdata.forEach(e => {
            if (e["id"] == itemID){
                curItem = e;
                return;
            }
        });

        // get form HTML to set div to it
        const formHTML = `
        <form id="itemEditForm" action="/listviewmod" method="post" onsubmit="userConfirmAct(event, 'edit')">
            <input name="listID" value="${itemID}" hidden />
            <h1>Edit ${curItem['item']}</h1>
            <div class="container-input">
                <input value="${curItem['amount']}" name="itemEditAmnt" type="number" placeholder="Amount" autocomplete="off" value="1" required />
                <input value="${curItem['item']}" name="itemEditItem" type="text" placeholder="Item" pattern="^[a-zA-Z][a-zA-Z ]*$" title="Only use letters and spaces" autocomplete="off" required />
            </div>
            <input value="${curItem['note']}" name="itemEditNote" type="text" placeholder="Note (Optional)" pattern="^[a-zA-Z0-9][a-zA-Z0-9 ]*$" title="Only use letters and spaces" autocomplete="off" />

            <div class="container-input">
                <button type="button" onclick="listItemEdit(event, 'cancel')">Cancel</button>
                <button type="submit" >Edit</button>
            </div>
        </form>
        `;
        e.target.parentElement.innerHTML = formHTML;
        return
    }
    // else, change ele if cancel button is pressed
    else if (itemID == "cancel"){
        e.target.parentElement.parentElement.parentElement.innerHTML = tempHTML;
        tempHTML = "";
        return
    }
    // if another ele is dbl clicked, stop operation until other is cancelled
    return
}

// function for toggling add container
document.getElementById("add-btn").addEventListener("click", e => {
    const addContainer = document.getElementById("container-add")
    if (addContainer.style.display === "flex"){
        addContainer.style.display = "none";
        e.target.style.rotate = "0deg";
        return;
    }
    addContainer.style.display = "flex";
    e.target.style.rotate = "-45deg";
});