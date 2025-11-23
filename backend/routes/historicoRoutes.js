const router = require('express').Router();
const User = require('../models/User');
const checkToken = require('../middleware/checkToken');
const Historico = require('../models/Historico')
const jwt = require("jsonwebtoken");

router.post('/salvar', async (req, res) => {
  try {
    const {userId, prompt, imageBase64 } = req.body;

    if (!userId) return res.status(422).json({ msg: "userId é obrigatório." });
    if (!prompt || !imageBase64) return res.status(422).json({ msg: "Prompt e imagem são obrigatórios." });

    const registro = new Historico({ userId, prompt, imageBase64 });
    await registro.save();

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