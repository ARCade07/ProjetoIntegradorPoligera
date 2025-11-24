require('dotenv').config();
const express = require('express');
const cors = require('cors');
const cookieParser = require('cookie-parser');
const path = require('path');
const app = express();
const caminhoFrontend = path.join(__dirname, "../frontend");
const checkToken = require('./middleware/checkToken');
const connectDB = require('./models/db')
const jwt = require ('jsonwebtoken')
const autenticacao = require('./routes/authenticationRoutes');
const historico = require('./routes/historicoRoutes');


app.use(express.json({ limit: '25mb' }))
app.use(cors({
    origin: true,
    credentials: true
}));

app.use(cookieParser())

app.get("/", (req, res) => {
    const token = req.cookies?.token;

    if (token) {
        try {
            jwt.verify(token, process.env.SECRET);
            return res.sendFile(path.join(caminhoFrontend, "index.html"));
        } catch (err) {
            console.log(err)
            res.clearCookie('token');
            res.clearCookie('role');
            return res.sendFile(path.join(caminhoFrontend, "login.html"));
        }
    }
    return res.redirect("/login.html");
});

app.use(express.static(caminhoFrontend));


app.use('/autenticacao', autenticacao);
app.use('/historico', historico);

connectDB().then(() => {
    app.listen(3000, () => console.log('Servidor rodando na porta 3000'));
})

