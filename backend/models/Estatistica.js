const mongoose = require('mongoose');

const estatisticaSchema = new mongoose.Schema({
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    tipo: {
        type: String,
    },
    materia: {
        type: String,
    },
    icones: {
        type: [String],
        default: []
    }
}, { timestamps: true });

estatisticaSchema.index({ userId: 1, createdAt: 1 });

const Estatistica = mongoose.model('Estatistica', estatisticaSchema);

module.exports = Estatistica;