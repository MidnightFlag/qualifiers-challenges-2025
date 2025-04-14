const express = require("express");
const { v4: uuidv4 } = require('uuid');
const sqlite3 = require('sqlite3').verbose();

const router = express.Router();
const db = new sqlite3.Database(':memory:');

const bot = require("./bot");
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const ADM_USERNAME = "admin";
const ADM_PASSWORD = uuidv4();

db.serialize(() => {
    db.run(`CREATE TABLE Users (
        username VARCHAR(255) PRIMARY KEY,
        password VARCHAR(255)
    )`);

    db.run(`CREATE TABLE Playgrounds (
        uuid VARCHAR PRIMARY KEY,
        user_name VARCHAR,
        data VARCHAR,
        FOREIGN KEY(user_name) REFERENCES Users(username)
    )`);

    db.run(`INSERT INTO Users (username, password) VALUES (?, ?)`, [ADM_USERNAME, ADM_PASSWORD], (err) => {
        if(err) {
            console.log("Unable to setup admin user: ");
            console.log(err);
            process.exit(-1);
        }
        if(process.env.DEBUG) {
            console.log(`ADM_USERNAME = admin`);
            console.log(`ADM_PASSWORD = ${ADM_PASSWORD}`);
        }
    });
});

router.get('/flag', (req, res) => {
    if(req.session.username == "admin") {
        res.status(200).json({"FLAG":process.env.FLAG ?? "MCTF{fake_flag"});
    } else {
        res.status(403).json({"status":403, "error": "Admin restricted."});
    }
})

router.post('/login', (req, res) => {
    const { username, password } = req.body;
    db.get(`SELECT * FROM Users WHERE username = ? AND password = ?`, [username, password], (err, row) => {
        if (err) {
            console.log(`[/login - DATABASE ERROR]: ${e}`);
            res.redirect('/login?msg=1');
        }
        if (row) {
            req.session.username = username;
            res.redirect('/playground');
        } else {
            res.redirect('/login?msg=2');
        }
    });
});

router.post('/register', (req, res) => {
    const { username, password } = req.body;
    db.get(`SELECT * FROM Users WHERE username = ?`, [username], (err, row) => {
        if (err) {
            console.log(`[/register - DATABASE ERROR]: ${e}`);
            res.redirect('/register?msg=1');
        }
        if (row) {
            res.redirect('/register?msg=2');
        } else {
            db.run(`INSERT INTO Users (username, password) VALUES (?, ?)`, [username, password], (err) => {
                if (err) {
                    res.redirect('/register?msg=1');
                }
                res.redirect('/login?msg=3');
            });
        }
    });
});

router.post('/playground/create', (req, res) => {
    if (!req.session.username) {
        res.status(401).send('Please login before accessing the playground.');
    }
    const uuid = uuidv4();
    db.run(`INSERT INTO Playgrounds (uuid, user_name, data) VALUES (?, ?, ?)`, [uuid, req.session.username, ""], (err) => {
        if (err) {
            console.log(`[/playground/create - DATABASE ERROR]: ${e}`);
            res.status(500).json({"status":500, "error":"Internal Server Error"});
        }
    });
    res.json({"status":200, "uuid":uuid});
});

router.get('/playground/:uuid', (req, res) => {
    if (!req.session.username) {
        res.status(401).send('Please login before accessing the playground.');
    }
    db.get(`SELECT * FROM Playgrounds WHERE uuid = ?`, [req.params.uuid], (err, row) => {
        if (err) {
            console.log(`[GET - /playground/:uuid - DATABASE ERROR]: ${e}`);
            res.status(500).json({"status":500, "error":"Internal Server Error"});
        }
        if (row) {
            if(req.session.username === row.user_name || req.session.username === ADM_USERNAME) {
                res.status(200).json({"status":200, "data":row});
            } else {
                res.status(403).json({"status":403, "error": "You don't have access to this playground."})
            }
        } else {
            res.status(404).json({"status":404, "error": "Playground not found"});
        }
    });
})

router.get('/playgrounds', (req, res) => {
    if (!req.session.username) {
        res.status(401).send('Please login before accessing the playground.');
    }
    db.all(`SELECT uuid FROM Playgrounds WHERE user_name = ? AND LENGTH(data) > 0`, [req.session.username], (err, rows) => {
        if (err) {
            console.log(`[GET - /playgrounds - DATABASE ERROR]: ${e}`);
            res.status(500).json({"status":500, "error":"Internal Server Error"});
        }
        if (rows) {
            res.status(200).json({"status":200, "data":rows});
        } else {
            res.status(404).json({"status":404, "error": "Playground not found"});
        }
    });
})

router.post('/playground/:uuid', async (req, res) => {
    if (!req.session.username) {
        res.status(401).send('Please login before accessing the playground.');
    }
    db.get(`SELECT * FROM Playgrounds WHERE uuid = ?`, [req.params.uuid], (err, row) => {
        if (err) {
            console.log(`[POST - /playground/:uuid - DATABASE ERROR]: ${e}`);
            res.status(500).json({"status":500, "error":"Internal Server Error"});
        }
        if (row) {
            if(req.session.username === row.user_name) {
                if(req.body.data !== undefined) {
                    db.run('UPDATE Playgrounds SET data = ? WHERE uuid = ?', [btoa(req.body.data), req.params.uuid], (update_err, _) => {
                        if(update_err) {
                            console.log(`[POST - /playground/:uuid - UPDATE DATABASE ERROR]: ${e}`);
                            res.status(500).json({"status":500, "error":"Internal Server Error"});
                        }
                        res.status(200).json({"status":200, "data": req.body.data});
                    })
                } else {
                    res.status(400).json({"status":400, "error": "Missing parameters."});
                }
            } else {
                res.status(403).json({"status":403, "error": "You don't have access to this playground."})
            }
        } else {
            res.status(404).json({"status":404, "error": "Playground not found"});
        }
    });
})

router.post('/bot', async (req, res) => {
    if(!req.session.username) {
        res.status(401).send('Please login before reporting  to bot.');
    }
    if(req.body.uuid !== undefined && typeof(req.body.uuid) === "string") {
        if(UUID_RE.exec(req.body.uuid) && req.get('origin') !== undefined && 
            (req.get('origin').startsWith("http://") || req.get('origin').startsWith("https://")) ) {
            let bot_res = await bot.goto(req.body.uuid, req.get('origin'), ADM_USERNAME, ADM_PASSWORD);
            if(bot_res) {
                res.status(200).json({"status":200, "data": "Nothing seems wrong with this playground."});
            } else {
                res.status(500).json({"status":500, "error": "Something goes wrong..."});
            }
        } else {
            res.status(400).json({"status":400, "error": "Id is invalid."});
        }
    } else {
        res.status(400).json({"status":400, "error": "Missing parameters."});
    }
})

router.get('/logout', (req, res) => {
    req.session.destroy(err => {
        if(err){
            console.log(`[/logout - ERROR]: ${e}`);
        }
        res.redirect('/login');
    });
});

module.exports = router;