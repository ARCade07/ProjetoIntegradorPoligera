async function carregarHistorico() {
    const userId = localStorage.getItem("userId");

    if (!userId) {
        console.error("userId não encontrado no localStorage");
        return;
    }
    try {
        const response = await axios.get(
            'http://localhost:3000/historico/buscar',
            {
                params: { userId }
            }
        );
        const container = document.getElementById("historico-container");
        container.innerHTML = "";
        console.log("Container encontrado:", container);
        response.data.forEach(item => {
            criarItemDoHistorico(container, item);
        });
    } catch (erro) {
        console.error("Erro ao carregar histórico:", erro);
    }
}
