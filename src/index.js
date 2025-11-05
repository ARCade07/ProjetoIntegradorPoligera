require('dotenv').config();
const express = require('express');
const cors = require('cors');
const cookieParser = require('cookie-parser');
const path = require('path');
const app = express();
const connectDB = require('./models/db')

const autenticacao = require('./routes/authenticationRoutes');
const usuarios = require('./routes/usersRoutes');

app.use(express.json());
app.use(cors());
app.use(cookieParser())

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'))
})

app.use('/auth', autenticacao);
app.use('/usuarios', usuarios)

connectDB().then(() => {
    app.listen(3000, () => console.log('Servidor rodando na porta 3000'));
})

