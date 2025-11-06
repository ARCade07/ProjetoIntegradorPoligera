const mongoose = require('mongoose');
const historicoSchema = new mongoose.Schema({
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    prompt: {
        type: String,
        required: true
    },
    caminhoImagem: {
        type: String,
        required: true
    },
}, { timestamps: true });
// Criação de índice composto para consultas por usuários ord. por data
historicoSchema.index({ userId: 1, createdAt: 1 });

const Historico = mongoose.model('Historico', historicoSchema);

module.exports = Historico;