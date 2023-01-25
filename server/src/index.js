const express = require('express');
const groceriesRoute = require('./routes/groceries')
const marketsRoute = require('./routes/markets')
const renderRoute = require('./routes/render')

const app = express();
const PORT = 3001;

// middleware
app.use(express.json());
app.use(express.urlencoded());
app.use((req, res, next) => {
    console.log(`${req.method} ${req.url}`)
    next();
});


app.use('/api/groceries', groceriesRoute);
app.use('/api/markets', marketsRoute);
app.use('/api/render', renderRoute);

app.listen(PORT, () => console.log(`Running Express on Port ${PORT}`));