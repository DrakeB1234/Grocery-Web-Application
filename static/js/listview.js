(function () {
    // go through each object
    let html = "";
    // get first category in list
    let pastCat = "";
    console.log(listdata)
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
            html += `<div class='container-item' style='border:0;'><h2>${e["amount"]}</h2><h3>${e["item"]}</h3><img src="../static/images/icons/icon-trash.svg">`;
            html += `</div><h4>^ Note: ${e["note"]}</h4>`;
        }
        else {
            html += `<div class='container-item'><h2>${e["amount"]}</h2><h3>${e["item"]}</h3><img src="../static/images/icons/icon-trash.svg">`;
            html += `</div>`;
        }

        // set past cat
        pastCat = e["category"];
    });
    // post data to document
    document.getElementById("listdata-get").innerHTML = html;
})();
