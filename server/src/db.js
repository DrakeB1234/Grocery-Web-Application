const mysql = require('mysql2');

module.exports = mysql.createConnection({
    host: 'main-database.cbhkqg0xerfz.us-east-2.rds.amazonaws.com',
    user: 'root',
    password: '791384265Templegrd',
    database: 'database1'
})