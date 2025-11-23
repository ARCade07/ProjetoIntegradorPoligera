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
function criarItemDoHistorico(container, item) {
    const bloco = document.createElement("div");
    bloco.classList.add("item-historico");

    const esquerda = document.createElement("div");
    esquerda.classList.add("historico-esquerda");

    const img = document.createElement("img");
    img.src = item.imageBase64;
    img.classList.add("thumb");

    const texto = document.createElement("p");
    texto.classList.add("prompt-texto");
    texto.innerText =
        item.prompt.length > 60 ? item.prompt.substring(0, 60) + "..." : item.prompt;

    esquerda.appendChild(img);
    esquerda.appendChild(texto);

    const menuWrapper = document.createElement("div");
    menuWrapper.classList.add("menu-wrapper");

    const pontos = document.createElement("span");
    pontos.classList.add("pontos");
    pontos.innerHTML = "⋮"; 

    const menu = document.createElement("div");
    menu.classList.add("menu-opcoes");

    const opc1 = document.createElement("div");
    opc1.innerText = "Copiar imagem";
    opc1.onclick = () => copiarImagem(item.imageBase64);
    const opc2 = document.createElement("div");
    opc2.innerText = "Copiar prompt";
    opc2.onclick = () => copiarPrompt(item.prompt);
    const opc3 = document.createElement("div");
    opc3.innerText = "Apagar do histórico";
    opc3.onclick = () => apagarHistorico(item._id, bloco);

    menu.appendChild(opc1);
    menu.appendChild(opc2);
    menu.appendChild(opc3);
    menuWrapper.appendChild(pontos);
    menuWrapper.appendChild(menu);

    pontos.onclick = (e) => {
        e.stopPropagation();
        menu.classList.toggle("ativo");
    };

    bloco.appendChild(esquerda);
    bloco.appendChild(menuWrapper);

    container.appendChild(bloco);
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
