const bcrypt = require('bcrypt');

async function criarHash(texto) {
    const salt = await bcrypt.genSalt(12);
    return bcrypt.hash(texto, salt);
}

async function compararHash(texto, hash) {
    return bcrypt.compare(texto, hash);
}

module.exports = { criarHash, compararHash };