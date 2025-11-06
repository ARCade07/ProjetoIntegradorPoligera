const router = require('express').Router();
const { criarHash, compararHash } = require('../util/cript');
const jwt = require('jsonwebtoken')
const enviarEmail = require('../util/mail')
const crypto = require('crypto')
const cookie = require('cookie')
const path = require('path');
const User = require('../models/User');

router.get('/cadastrar', (req, res) => {
    res.sendFile(path.join(__dirname, '../public', 'cadastro.html'));
})
router.post('/cadastrar', async (req, res) => {
    const { name, email, password, confirmpassword } = req.body;

    if (!name) return res.status(422).json({ msg: 'O nome é obrigatório' });
    if (!email) return res.status(422).json({ msg: 'O email é obrigatório' });
    if (!password) return res.status(422).json({ msg: 'A senha é obrigatória' });
    if (password !== confirmpassword) {
        return res.status(422).json({ msg: 'As senhas não conferem!' });
    }

    const userExists = await User.findOne({ email });
    if (userExists) {
        return res.status(422).json({ msg: 'Por favor, utilize outro e-mail!' });
    }

    const passwordHash = await criarHash(password)

    const user = new User({
        name,
        email,
        password: passwordHash,
    });

    try {
        await user.save();
        res.status(201).json({ success: true, msg: 'Usuário criado com sucesso!' });
    } catch (erro) {
        res
            .status(500)
            .json({ msg: 'Erro no servidor, tente novamente mais tarde' });
    }
});

router.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, '../public', 'login.html'));
})

router.post('/login', async (req, res) => {
    const { email, password } = req.body;
    if (!email) return res.status(422).json({ msg: 'O email é obrigatório' });
    if (!password) return res.status(422).json({ msg: 'A senha é obrigatória' });

    const user = await User.findOne({ email });
    if (!user) return res.status(422).json({ msg: 'Usuário não encontrado.' });

    const checkPassword = await compararHash(password, user.password);
    if (!checkPassword) return res.status(422).json({ msg: 'Senha inválida!' });

    try {
        const secret = process.env.SECRET;
        const token = jwt.sign(
            { id: user._id},
            secret,
            { expiresIn: '1h' }
            );
        const cookieOption = {
            httpOnly: true,
            maxAge: 3600000,
            path: '/'
        }
        res.cookie('token', token, cookieOption);
        res
            .status(200)
            .json({ msg: 'Autentiação realizada com sucesso', token });
    } catch (erro) {
        res.status(500).json({ msg: 'Erro ao gerar token' });
    }
});

router.get('/esqueceu-senha', (req, res) => {
    res.sendFile(path.join(__dirname, '../public', 'esqueci_senha.html'));
})

router.post('/esqueceu-senha', async (req, res) => {
    try {
        // Checa se o email do usuário existe
        const user = await User.findOne({ email: req.body.email });
        if (!user) {
            return res
                .status(404)
                .json({ msg: "O usuário com esse mail não existe."});
        }
        const resetToken = crypto.randomBytes(20).toString('hex');
        const tokenHash = await criarHash(resetToken);
        user.resetTokenHash = tokenHash;
        user.resetTokenExpires = Date.now() + 3600000; // 1 hora

        await user.save();

        await enviarEmail(user, resetToken);
        res
            .status(200)
            .json({ msg: "Token para recuperação gerado e enviado com sucesso!"})
    } catch (erro) {
        console.log(erro)
        return res.status(500).json({ msg: 'Erro interno do servidor.' })
    }
});
//Rota para resetar senha:
router.get('/redefinir-senha', (req, res) => {
    res.sendFile(path.join(__dirname, '../public', 'nova_senha.html'));
})

router.post('/redefinir-senha', async (req, res) => {
    try {
        const { email, resetToken, newPassword } = req.body;
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(404).json({ msg: 'Usuário não encontrado!' });
        }
        const isToken = await compararHash(resetToken, user.resetTokenHash);
        if(!isToken || user.resetTokenExpires < Date.now()) {
            return res.status(400).json({ msg: "Token inválido ou expirado."});
        }
        const passwordHash = await criarHash(newPassword);

        user.password = passwordHash;
        user.resetTokenHash = undefined;
        user.resetTokenExpires = undefined;

        await user.save();

        return res.status(200).json({ success: true, msg: 'Senha redefina com sucesso! '})
    } catch (erro) {
        console.log(erro)
        return res.status(500).json({ msg: 'Erro interno do servidor.' })
    }
});




module.exports = router;