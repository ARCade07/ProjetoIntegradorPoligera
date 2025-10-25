const bcrypt = require('bcrypt');

async function criarHash(texto) {
    const salt = await bcrypt.genSalt(12);
    return bcrypt.hash(texto, salt);
}

