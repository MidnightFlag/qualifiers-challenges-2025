const express = require("express");
const router = express.Router();
const path = require('path');

module.exports = (ROOT_DIR) => {
    router.get('/', (req, res) => {
        if (req.session.username) {
            res.redirect('/playground');
        } else {
            res.sendFile(path.join(ROOT_DIR, 'views', 'index.html'));
        }
    });
    
    router.get('/login', (req, res) => {
        if (req.session.username) {
            res.redirect('/playground');
        } else {
            res.sendFile(path.join(ROOT_DIR, 'views', 'login.html'));
        }
    });
    
    router.get('/register', (req, res) => {
        if (req.session.username) {
            res.redirect('/playground');
        } else {
            res.sendFile(path.join(ROOT_DIR, 'views', 'register.html'));
        }
    });
    
    router.get('/playground', (req, res) => {
        if (req.session.username) {
            res.sendFile(path.join(ROOT_DIR, 'views', 'playground.html'));
        } else {
            res.redirect('/login');
        }
    });
    
    router.get('/render_frame', (req, res) => {
        if (req.session.username) {
            res.sendFile(path.join(ROOT_DIR, 'views', 'render_frame.html'));
        } else {
            res.redirect('/login');
        }
    })
    
    router.get('/exec_frame', (req, res) => {
        if(req.session.username) {
            res.sendFile(path.join(ROOT_DIR, 'views', 'exec_frame.html'));
        } else {
            res.redirect('/login');
        }
    })

    return router;
};