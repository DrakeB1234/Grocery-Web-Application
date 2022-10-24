// constants for element ids
// const dataGet = document.getElementById('data-get');
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
itemArr.push(groceryList("Frozen", "Pizza", 3));

// get all categories
const getCategories = () => {
    itemArr.forEach((e) => {
        // if current category is not in array, then push to array
        if (!(categoryArr.includes(e.category))) {
            categoryArr.push(e.category);
            console.log(e.category);
        }
        else {
            console.log("item is already in array");
        }
    });
}

// call function for each item in list
const cycleEachItem = () => {
    let differentCategory = "";
    itemArr.forEach((e) => {
        if (differentCategory == e.category){
            postListData(e.category, e.amount, e.item, e.note, false);
        }
        else {
            postListData(e.category, e.amount, e.item, e.note, true);
            differentCategory = e.category;
            // adds ending list tag
            html += "</list>";
        }
    });

    console.log(html);
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
    html += "\
        <item class='item'>\
            <button class='item-amount'>" + amnt + "</button>\
            <h1>" + item + "</h1>\
            <i onclick='removeItem();' class='fa-solid fa-trash-can'></i>\
        </item>";
}

getCategories();
cycleEachItem();