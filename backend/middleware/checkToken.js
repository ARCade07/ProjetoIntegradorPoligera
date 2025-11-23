const jwt = require('jsonwebtoken');

function checkToken(req, res, next) {
    let token = req.cookies?.token;
    // também aceita header:
    if (!token) {
        const authHeader = req.headers.authorization;
        if (authHeader?.startsWith("Bearer ")) {
            token = authHeader.split(" ")[1];
        }
    }
    if (!token) {
        return res.status(401).json({ msg: 'Acesso negado: token não encontrado.' });
    }
    try {
        const secret = process.env.SECRET;
        const decoded = jwt.verify(token, secret);
        req.user = decoded;
        next();
    } catch (erro) {
        res.status(401).json({ msg: 'Token inválido! ' });
    }
}

module.exports = checkToken;