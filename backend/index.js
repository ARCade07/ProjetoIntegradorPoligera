require('dotenv').config();
const express = require('express');
const app = express();
const connectDB = require('./models/db')

app.use(express.json());

app.get('/', (req, res) => {
    res.status(200).json({ msg: 'Teste' });
})
connectDB().then(() => {
    app.listen(3000, () => console.log('Servidor rodando na porta 3000'));
})

