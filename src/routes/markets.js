const { Router } = require('express');

const router = Router();

let marketsList = [
    {
        id: 1,
        store: "Target",
        location: "Springfield"
    },
    {
        id: 2,
        store: "Home Depot",
        location: "Moberly"
    },
    {
        id: 3,
        store: "Walmart",
        location: "Tampa"
    },
    {
        id: 4,
        store: "Walmart",
        location: "Springfield"
    },
]

router.get('', (req, res) => {
    const { location } = req.query
    const pattern = /[0-9]/;

    if (location && pattern.test(location) == false) {
        const filterList = marketsList.filter((s) => s.location == location)
        res.send(filterList);
    } else res.send(marketsList);

})

module.exports = router;