const mongoose = require('mongoose');

const connectDB = async () => {
    const dbUser = process.env.DB_USER;
    const dbPassword = process.env.DB_PASS;

    try {
        await mongoose.connect(
            `mongodb+srv://${dbUser}:${dbPassword}@poligera.qx9tlbw.mongodb.net
            /?retryWrites=true&w=majority&appName=Poligera`
        )
        console.log('Conectado ao Banco de Dados com sucesso');
    } catch (erro) {
        console.log('Erro ao conectar ao banco: ', erro);
    }
}

module.exports = connectDB;