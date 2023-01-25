const { Router } = require('express');

const router = Router();

router.post('/login', (req, res) => {
    console.log(`${req.body.email}`)
    res.send(`logged in ${req.body.email} <a href="/">Go Back</a>`)
})

module.exports = router;