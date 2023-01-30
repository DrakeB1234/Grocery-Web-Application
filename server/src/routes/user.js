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
        res.status(500).send(`Internal Server Error`);
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
        db.promise().execute(`
            INSERT INTO nodeusers (email, username, password, active)
            VALUES (?, ?, ?, false);`, [email, username, password]);

        // add authenication data to database
        db.promise().execute(`
            INSERT INTO userauth (email, token, timestamp)
            VALUES (?, ?, ?);`, [email, token, ts]);

        // ensure user added in db, then send email for verfiying account
        nmailer.sendEmail(email, "Please verify your account", `Visit the Link Below\n\n${process.env.BASE_URL}/api/users/verify?t=${token}`);

        res.status(201).send(`User Added, Awaiting Verification`);

    } catch(err) {
        console.log(`${err.name}: ${err.message}`);
        res.status(500).send(`Internal Server Error`);
    };
});

// verify user email
router.get('/verify', async (req, res) => {
    try {
        // get token form get parameters, then lookup token in database
        const token = req.query.t;

        let query = await db.promise().execute(`SELECT * 
        FROM userauth
        WHERE token = ?;`, [token]);
        query = query[0]

        if (query.length == []){
            return res.status(404).send("Token not found");
        }

        // verify token is not expired
        const datetime = new Date();

        if (datetime > query[0].timestamp){
            return res.status(404).send("Token expired");
        }

        // update usertable to active if not expired
        db.promise().execute(`UPDATE nodeusers
        SET active = 1
        WHERE email = ?;`, [query[0].email]);

        // delete userauth entry
        db.promise().execute(`DELETE FROM userauth
        WHERE email = ?;`, [query[0].email]);

        res.status(200).send("Account verified");

    } catch (err) {
        console.log(`${err.name}: ${err.message}`);
        res.status(500).send("Internal Server Error");
    }
});

// resend verify to user email
router.post('/reverify', async (req, res) => {
    try {
        // get token form get parameters, then lookup token in database
        const email = req.body.email;

        // get and validate form data
        if(!vinput.checkEmail(email)){
            return res.status(400).send('Invalid format');
        }

        // get data from sent email
        let query = await db.promise().execute(`SELECT *
        FROM userauth
        WHERE email = ?;`, [email]);
        query = query[0];

        // catches if account is not in auth table (already verified or account not made)
        if (query.length == []){
            return res.status(404).send("Account not found");
        }

        // ensure that at least 10 minutes has passed since last token
        const timedate = new Date();
        const tokentime = new Date(query[0].timestamp);
        tokentime.setMinutes(tokentime.getMinutes() - 50);
 
        if (timedate < tokentime){
            return res.status(400).send("Wait at least 10 minutes before sending another email");
        }

        // regenerate token
        timedate.setHours(timedate.getHours() + Number(process.env.EMAIL_AUTH_EXPIRY_HOUR));

        const token = jwt.sign(email, `${timedate}`);

        // add new authenication data to database
        db.promise().execute(`
            UPDATE userauth
            SET token = ?, timestamp = ?
            WHERE email = ?;`, [token, timedate, email]);

        // ensure user auth data was updated in db, then send email for verfiying account
        nmailer.sendEmail(email, "Please verify your account", `Visit the Link Below\n\n${process.env.BASE_URL}/api/users/verify?t=${token}`);

        res.status(200).send("Email Sent");

    } catch (err) {
        console.log(`${err.name}: ${err.message}`);
        res.status(500).send("Internal Server Error");
    }
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
        res.status(500).send(`Internal Server Error`);
    };
});


module.exports = router;