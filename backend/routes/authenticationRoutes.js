const router = require('express').Router();
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const User = require('../models/User');

router.post('/cadastrar', async (req, res) => {
    const { name, email, password, confirmpassword } = req.body;

    if (!name) return res.status(422).json({ msg: 'O nome é obrigatório'});
    if (!email) return res.status(422).json({ msg: 'O email é obrigatório'});
    if (!password) return res.status(422).json({ msg: 'A senha é obrigatória'});
    if (password !== confirmpassword) {
        return res.status(422).json({ msg: 'As senhas não conferem!'});
    }

    const userExists = await User.findOne({ email });
    if (userExists) {
        return res.status(422).json({ msg: 'Por favor, utilize outro e-mail!'});
    }

    const salt = await bcrypt.genSalt(12);
    const passwordHash = await bcrypt.hash(password, salt);

    const user = new User({
        name,
        email,
        password: passwordHash,
    })

    try {
        res.status(201).json({ msg: 'Usuário criado com sucesso!'})
    } catch (erro) {
        res
            .status(500)
            .json({msg: 'Erro no servidor, tente novamente mais tarde'})
    }
});

router.post('/login', async (req, res) => {
    const { email, password } = req.body;
    if (!email) return res.status(422).json({ msg: 'O email é obrigatório'});
    if (!password) return res.status(422).json({ msg: 'A senha é obrigatória'});

    const user = await User.findOne({ email });
    if(!user) return res.status(422).json({msg: 'Usuário não encontrado.'});

    const checkPassword = await bcrypt.compare(password, user.password);
    if (!checkPassword) return res.status(422).json({ msg: 'Senha inválida!'});
    
    try {
        const secret = process.env.SECRET;
        const token = jwt.sign({ id: user._id, secret });
        res
            .status(200)
            .json({ msg: 'Autentiação realizada com sucesso', token });
    } catch (erro) {
        res.status(500).json({ msg: 'Erro ao gerar token' });
    }
});

module.exports = router;