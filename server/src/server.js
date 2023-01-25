const express = require('express');
const userRoute = require('./routes/user')

const app = express();
const PORT = 5000;

// middleware
app.use(express.json());
app.use(express.urlencoded());
app.use((req, res, next) => {
    console.log(`${req.method} ${req.url}`)
    next();
});


app.use('/api/user', userRoute);

app.listen(PORT, () => console.log(`Running Express on Port ${PORT}`));