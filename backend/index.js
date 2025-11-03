require('dotenv').config();
const express = require('express');
const cors = require('cors');
const cookieParser = require('cookie-parser');
const app = express();
const connectDB = require('./models/db')

const autenticacao = require('./routes/authenticationRoutes');
const usuarios = require('./routes/usersRoutes');

app.use(express.json());
app.use(cors());
app.use(cookieParser())

app.get('/', (req, res) => {
    res.status(200).json({ msg: 'Teste' });
})

app.use('/autenticacao', autenticacao);
app.use('/usuarios', usuarios)

connectDB().then(() => {
    app.listen(3000, () => console.log('Servidor rodando na porta 3000'));
})

