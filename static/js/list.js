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
            html += `<div class='list-item'><h1>${curCat}</h1>`;
        }

        // print each item in format
        html += `<div class='item'><h2>${e["amount"]}</h2><h3>${e["item"]}</h3><i class="fa-solid fa-trash-can"></i>`;
        // if there is a note, print h4 tag with it
        if (e["note"] != "") {
            html += `</div><h4>Note: ${e["note"]}</h4>`;
        }
        else {
            html += `</div>`;
        }

        // set past cat
        pastCat = e["category"];
    });
    // post data to document
    document.getElementById("container-list").innerHTML = html;
})();