const { Router } = require('express');

const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken')
const db = require('../db');
const vinput = require('../utils/helpersVInput');
const nmailer = require('../utils/nodeMailer');

const router = Router();

// get users
router.get('/data', async (req, res) => {
    try {
        const query = await db.promise().execute('SELECT * FROM nodeusers;');

        res.status(200).send(query[0]);

    } catch(err) {
        console.log(`${err.name}: ${err.message}`);
        res.status(500).send(`${err.name}: ${err.message}`);
    }
});

// handle register
router.post('/register', async (req, res) => {
    try {
        // get and validate form data
        if(!vinput.checkUsername(req.body.username) || !vinput.checkEmail(req.body.email) || !vinput.checkPassword(req.body.password)){
            return res.status(400).send('Invalid format');
        }

        const email = req.body.email;
        const username = req.body.username;

        // getting usernames and emails to ensure uniqueness
        const query = await db.promise().execute('SELECT username,email FROM nodeusers;');
        query[0].every(e => {
            if (e.email == email){
                res.status(400).send('Email taken');
                return false;
            }
            if (e.username == username){
                res.status(400).send('Username taken');
                return false;
            }
            return true;
        });

        // catches if an error was thrown in loop
        if(res.statusCode == 400){
            return res;
        }

        // hashing password
        const password =  await bcrypt.hash(req.body.password, 10);

        // get JWT token based on set hour expiry time
        const ts = new Date();
        ts.setHours(ts.getHours() + Number(process.env.EMAIL_AUTH_EXPIRY_HOUR));

        const token = jwt.sign(email, `${ts}`);

        // add user to database
        db.promise().execute(`\
            INSERT INTO nodeusers (email, username, password, active)\
            VALUES (?, ?, ?, false);`, [email, username, password]);

        // add authenication data to database
        db.promise().execute(`\
            INSERT INTO userauth (email, token, timestamp)\
            VALUES (?, ?, ?);`, [email, token, ts]);

        // ensure user added in db, then send email for verfiying account
        nmailer.sendEmail(email, "Please verify your account", `Visit the Link Below\n\n${process.env.BASE_URL}/api/users/verify?t=${token}`);

        res.status(201).send(`User Added, Awaiting Verification`);

    } catch(err) {
        console.log(`${err.name}: ${err.message}`);
        res.status(500).send(`${err.name}: ${err.message}`);
    };
});

// handle login
router.post('/login', async (req, res) => {
    try {
        // get user by username or email
        let query = await db.promise().execute(`SELECT * FROM nodeusers WHERE email = ? OR username = ?;`, [req.body.username, req.body.username]);
        query = query[0];

        // if no results, invalid username or email
        if (query.length == []){
            return res.status(400).send('Invalid username/email or password');
        };

        // compare form password to stored hash
        if (!await bcrypt.compare(req.body.password, query[0].password)){
            return res.status(400).send('Invalid username/email or password');
        }

        // check to see if account is active
        if (query[0].active == 0){
            return res.status(400).send("Please Confirm your email to login");
        }

        res.status(200).send(`User logged in`);

    } catch(err) {
        console.log(`${err.name}: ${err.message}`);
        res.status(500).send(`${err.name}: ${err.message}`);
    };
});


module.exports = router;