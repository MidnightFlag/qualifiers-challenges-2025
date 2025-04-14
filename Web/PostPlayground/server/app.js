const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const crypto = require('crypto');
const path = require('path');
const helmet = require('helmet');
const ROOT_DIR = process.cwd();
const apiRoutes = require("./routes/api");
const frontRoutes = require("./routes/front")(ROOT_DIR);

const app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(session({
    secret: crypto.randomBytes(64).toString('hex'),
    resave: false,
    saveUninitialized: false
}));
app.use(express.static(path.join(__dirname, 'public')));
app.use(helmet.frameguard());
app.use("/api", apiRoutes);
app.use("/", frontRoutes);

const PORT = process.env.PORT ?? 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server started on port ${PORT}`);
});