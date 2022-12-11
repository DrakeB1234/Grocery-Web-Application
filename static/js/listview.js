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
            html += `<div class='container-item'><h2>${e["amount"]}</h2><h3>${e["item"]}</h3>\
            <form id="item-del" action="/listviewmod" method="post" onsubmit="userConfirmAct(event, 'delete')">
            <button name="itemDel" value="${e["id"]}" type="submit"><img src="../static/images/icons/icon-trash.svg"></button>\
            </form>`;
            html += `</div><h4>^ Note: ${e["note"]}</h4>`;
        }
        else {
            html += `<div class='container-item'><h2>${e["amount"]}</h2><h3>${e["item"]}</h3>\
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