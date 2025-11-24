const router = require('express').Router();
const User = require('../models/User');
const checkToken = require('../middleware/checkToken');
const Historico = require('../models/Historico')
const Estatistica = require('../models/Estatistica');
const jwt = require("jsonwebtoken");

router.post('/salvar', async (req, res) => {
    try {
        const { userId, prompt, imageBase64, tipo, materia, icones } = req.body;

        if (!userId) return res.status(422).json({ msg: "userId é obrigatório." });
        if (!imageBase64) return res.status(422).json({ msg: "A imagem é obrigatória." });

        const novoHistorico = new Historico({
            userId,
            prompt: prompt || "Nenhum prompt foi especificado",
            imageBase64
        });
        const novaEstatistica = new Estatistica({ userId, tipo, materia, icones });
        await Promise.all([
            novoHistorico.save(),
            novaEstatistica.save()
        ]);

        return res.status(201).json({ success: true, msg: "Histórico salvo com sucesso!" });
    } catch (erro) {
        console.error("Erro ao salvar histórico:", erro);
        return res.status(500).json({ msg: "Erro ao salvar histórico." });
    }
});

router.get('/buscar', async (req, res) => {
    const { userId } = req.query;
    if (!userId) {
        return res.status(400).json({ msg: "userId não fornecido" });
    }
    try {
        const historico = await Historico.find({ userId })
            .sort({ createdAt: -1 });

        res.json(historico);
    } catch (erro) {
        res.status(500).json({ msg: "Erro ao buscar histórico" });
    }
});

router.get('/estatisticas', async (req, res) => {
    const { userId } = req.query;

    if (!userId) {
        return res.status(400).json({ msg: "userId é necessário para identificar a permissão." });
    }

    try {
        const user = await User.findById(userId);

        if (!user) {
            return res.status(404).json({ msg: "Usuário não encontrado." });
        }

        let filtro = {};

        if (user.role !== 'admin') {
            filtro = { userId: userId };
        }

        const dados = await Estatistica.find(filtro)
            .select('tipo materia icones createdAt')
            .sort({ createdAt: 1 });

        res.json(dados);

    } catch (erro) {
        console.error("Erro ao buscar estatísticas:", erro);
        res.status(500).json({ msg: "Erro ao buscar estatísticas" });
    }
});

router.delete('/:id', async (req, res) => {
    try {
        const id = req.params.id;
        const item = await Historico.findByIdAndDelete(id);
        if (!item) {
            return res.status(404).json({ msg: "Item não encontrado" });
        }

        res.json({ msg: "Item removido com sucesso" });

    } catch (erro) {
        console.error(erro);
        res.status(500).json({ msg: "Erro interno" });
    }
});

module.exports = router;