const router = require('express').Router();
const { criarHash, compararHash } = require('../util/cript');
const jwt = require('jsonwebtoken');
const enviarEmail = require('../util/mail');
const crypto = require('crypto');
const cookie = require('cookie');
const User = require('../models/User');

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
        return res.status(409).json({ msg: 'Este email já esta sendo utilizado. Por favor, utilize outro e-mail!' });
    }
    const isAdmin = email.endsWith("@poliedro.com");
    const passwordHash = await criarHash(password);

    const user = new User({
        name,
        email,
        password: passwordHash,
        role: isAdmin ? "admin" : "user"
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

router.post('/login', async (req, res) => {
    const { email, password } = req.body;
    if (!email) return res.status(422).json({ msg: 'O email é obrigatório' });
    if (!password) return res.status(422).json({ msg: 'A senha é obrigatória' });

    const user = await User.findOne({ email });
    if (!user) return res.status(401).json({ msg: 'Usuário não encontrado.' });

    const checkPassword = await compararHash(password, user.password);
    if (!checkPassword) return res.status(422).json({ msg: 'Senha inválida!' });

    try {
        const secret = process.env.SECRET;
        const token = jwt.sign({
            id: user._id,
            role: user.role
        },
            secret,
            { expiresIn: '1h' }
        );
        const cookieOption = {
            httpOnly: true,
            maxAge: 3600000,
            path: '/'
        }
            maxAge: 3600000, // 1 hora
            sameSite: "strict",
            secure: false
        };
        res.cookie('token', token, cookieOption);
        res.cookie("role", user.role, {
            httpOnly: false,
            sameSite: "Lax",
        });
        res
            .status(200)
            .json({ msg: 'Autentiação realizada com sucesso', token });
    } catch (erro) {
        res.status(500).json({ msg: 'Erro ao gerar token' });
    }
});

router.post('/esqueceu-senha', async (req, res) => {
    try {
        // Checa se o email do usuário existe
        const user = await User.findOne({ email: req.body.email });
        if (!user) {
            return res
                .status(404)
                .json({ msg: "O usuário com esse mail não existe." });
        }
        const resetToken = crypto.randomBytes(20).toString('hex');
        const tokenHash = await criarHash(resetToken);
        user.resetTokenHash = tokenHash;
        user.resetTokenExpires = Date.now() + 3600000; // 1 hora

        await user.save();

        await enviarEmail(user, resetToken);
        res
            .status(200)
            .json({ msg: "Token para recuperação gerado e enviado com sucesso!" })
    } catch (erro) {
        console.log(erro)
        return res.status(500).json({ msg: 'Erro interno do servidor.' })
    }
});
//Rota para resetar senha:
router.post('/redefinir-senha', async (req, res) => {
    try {
        const { email, resetToken, newPassword } = req.body;
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(404).json({ msg: 'Usuário não encontrado!' });
        }
        const isToken = await compararHash(resetToken, user.resetTokenHash);
        if (!isToken || user.resetTokenExpires < Date.now()) {
            return res.status(401).json({ msg: "Token inválido ou expirado." });
        }
        const passwordHash = await criarHash(newPassword);

        user.password = passwordHash;
        user.resetTokenHash = undefined;
        user.resetTokenExpires = undefined;

        await user.save();

        return res.status(200).json({ success: true, msg: 'Senha redefina com sucesso! ' });
    } catch (erro) {
        console.log(erro)
        return res.status(500).json({ msg: 'Erro interno do servidor.' });
    }
});




module.exports = router;