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
document.getElementById("aba-historico").addEventListener("click", () => {
    carregarHistorico();
});

function copiarPrompt(texto) {
    navigator.clipboard.writeText(texto);
    alert("Prompt copiado!");
}
function copiarImagem(base64) {
    const link = document.createElement("a");
    link.href = base64;
    link.download = "imagem.png";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    alert("Imagem salva! (Copiar direto para a área de transferência não é permitido por este navegador)");
}

async function apagarHistorico(id, elementoHTML) {
    if (!confirm("Tem certeza que deseja apagar este item?")) return;

    try {
        const url = `http://localhost:3000/historico/${id}`;

        await axios.delete(url);

        elementoHTML.remove();

    } catch (err) {
        console.error("Erro ao apagar:", err);
        alert("Erro ao remover do histórico.");
    }
}
