// constants for element ids
const dataGet = document.getElementById('data-get');
let html = "";

// arrays
let itemArr = [];
let categoryArr = [];

// factory function for making grocery items
const groceryList = (category, item, amount, note) => {
    return {category, item, amount, note};
}

// items added manually
itemArr.push(groceryList("Produce", "Spinach", 2, "Need two bags"));
itemArr.push(groceryList("Produce", "Apples", 5));
itemArr.push(groceryList("Produce", "Brocolli", 3));
itemArr.push(groceryList("Produce", "Spinach", 2, "Need two bags"));
// itemArr.push(groceryList("Frozen", "Pizza", 3));
// itemArr.push(groceryList("Frozen", "Mangos", 3, "For a friend :)"));
// itemArr.push(groceryList("Canned", "Chickpeas", 2, "Need big cans"));
// itemArr.push(groceryList("Canned", "Beans", 2));
// itemArr.push(groceryList("House", "Paper Plates", 2, "For moms house"));

// get all categories
const getCategories = () => {
    itemArr.forEach((e) => {
        // if current category is not in array, then push to array
        if (!(categoryArr.includes(e.category))) {
            categoryArr.push(e.category);
        };
    });
}

// call function for each item in list
const cycleEachItem = () => {
    let differentCategory = "";
    itemArr.forEach((e) => {
        if (differentCategory == e.category){
            postListData(e.category, e.amount, e.item, e.note, false);
        }
        else if (differentCategory != e.category) {
            postListData(e.category, e.amount, e.item, e.note, true);
            differentCategory = e.category;
            // adds ending list tag
        }
    });
    dataGet.innerHTML = html;
}

const postListData = (cat, amnt, item, note, dif) => {
    // get container per category
    if (dif == true){
        html += "<list class='item-container'>";
        html += "\
        <item class='item'>\
            <h1>" + cat + "</h1>\
        </item>";
    }

    // adds data into html packet
    html += "\
        <item class='item'>\
            <button class='item-amount'>" + amnt + "</button>\
            <h1>" + item + "</h1>\
            <i onclick='removeItem();' class='fa-solid fa-trash-can'></i>\
        </item>";

    // if there is a note, then add to end of item
    if (note != undefined){
        html += "<h2><i class='fa-solid fa-caret-up'></i>Note: " + note + "</h2>";
    }
}

// catches form submit for add form
document.getElementById('add-form').addEventListener('submit', (e) =>{
    e.preventDefault();

    const inputCat = document.getElementById('category-add').value;
    const inputItem = document.getElementById('item-add').value;
    const inputNote = document.getElementById('note-add').value;
    const inputAmount = document.getElementById('amount-add').value;

    itemArr.push(groceryList(inputCat, inputItem, inputAmount, inputNote));
    console.log(inputCat + inputItem + inputAmount + inputNote);

    // resets values
    document.getElementById('category-add').value = "";
    document.getElementById('item-add').value = "";
    document.getElementById('note-add').value = "";
    document.getElementById('amount-add').value = "";
    cycleEachItem();
});

getCategories();
cycleEachItem();

// function for hiding adder div
const hideAdder = () => {
    const adderDiv = document.getElementById('show-add');

    if (adderDiv.style.opacity == 0){
        adderDiv.style.display = 'block';
        adderDiv.style.opacity = 1;
    }
    else {
        adderDiv.style.opacity = 0;
        adderDiv.style.display = 'none';
    }
}