const { Router } = require('express');

const router = Router();

let groceryList = [
    {
        item : 'Milk',
        quantity: 2
    },
];

router.get('',
(req, res, next) => {
    console.log('Before Handling req');
    next();
},
(req, res) => {
    res.send(groceryList);
});

router.get('/:item',
(req, res) => {
    const { item } = req.params;
    const groceryItem = groceryList.find((g) => g.item === item);
    res.send(groceryItem)
});

router.post('', 
(req, res, next) => {
    console.log('Before Handling POST');
    if (req.body.item == "apples"){
        console.log("Apples are nasty")
    }
    next();
},
(req, res) => {
    console.log(req.body);
    groceryList.push(req.body)
    res.send(201);
});

module.exports = router;