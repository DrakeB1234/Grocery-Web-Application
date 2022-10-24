// array for grocery items
let itemArr = [];

// factory function for making grocery items
const groceryList = (category, item, amount, note) => {
    return {category, item, amount, note};
}

itemArr.push(groceryList("Produce", "Spinach", 2, "Need two bags"));
itemArr.push(groceryList("Produce", "Apples", 5));
itemArr.push(groceryList("Produce", "Brocolli", 3));


itemArr.forEach((e) => {
    console.log(e);
    postListData(e.category, e.amount, e.item, e.note);
});

// constants for element ids
const dataGet = document.getElementById('data-get');

function postListData(cat, amnt, item, note){

}