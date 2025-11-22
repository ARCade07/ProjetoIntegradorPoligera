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

    try {
    }
});





module.exports = router;