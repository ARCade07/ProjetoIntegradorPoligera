const router = require('express').Router();
const User = require('../models/User');
const checkToken = require('../middleware/checkToken');

router.get('/:id', checkToken, async (req, res) => {
    const id = req.params.id;

    const user = await User.findById(id, '-password');
    if (!user) return res.status(404).json({ msg: 'Usuário não encontrado ' });

    res.status(200).json({ user });
});

router.get('/check-token', checkToken, (req, res) => {
    try {
        res.status(200).json({ msg: 'Token válido' });
    } catch (erro) {
        console.log(erro);
    }
});

module.exports = router;