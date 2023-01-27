const express = require('express');

// routes
const userRoute = require('./routes/user');

// dependencies
require('dotenv').config({path: './src/.env'});

const app = express();
const PORT = 5000;

// middleware
app.use(express.json());
app.use(express.urlencoded());
app.use((req, res, next) => {
    console.log(`${req.method} ${req.url}`)
    next();
});


app.use('/api/users', userRoute);

app.listen(PORT, () => console.log(`Running Server on Port ${PORT}`));