require('dotenv').config();
const express = require('express');
const cors = require('cors');
const cookieParser = require('cookie-parser');
const path = require('path');
const app = express();
const caminhoFrontend = path.join(__dirname, "../frontend");
const connectDB = require('./models/db')

const autenticacao = require('./routes/authenticationRoutes');
const usuarios = require('./routes/usersRoutes');

app.use(express.json());
app.use(cors({
    origin: true,
    credentials: true
}));

app.use(cookieParser())

app.get('/', (req, res) => {
    res.status(200).json({ msg: 'Teste' });
})
app.get("/", (req, res) => {
    const token = req.cookies?.token;
    if (token) {
        return res.sendFile(path.join(caminhoFrontend, "index.html"));
    }
    return res.sendFile(path.join(caminhoFrontend, "login.html"));
});

app.use(express.static(caminhoFrontend));


app.use('/autenticacao', autenticacao);
app.use('/usuarios', usuarios)

connectDB().then(() => {
    app.listen(3000, () => console.log('Servidor rodando na porta 3000'));
})

