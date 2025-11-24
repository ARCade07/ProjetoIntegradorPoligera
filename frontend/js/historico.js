async function carregarHistorico(containerId = "historico-container") {
    const userId = localStorage.getItem("userId");

    if (!userId) {
        console.error("userId não encontrado no localStorage");
        return;
    }

    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`Container com ID ${containerId} não encontrado.`);
        return;
    }

    try {
        const response = await axios.get(
            'http://localhost:3000/historico/buscar',
            {
                params: { userId }
            }
        );
        
        container.innerHTML = "";
        console.log(`Container ${containerId} atualizado.`);
        
        if (response.data.length === 0) {
            container.innerHTML = "<p class='text-center text-muted mt-3'>Nenhum item no histórico.</p>";
            return;
        }

        response.data.forEach(item => {
            criarItemDoHistorico(container, item);
        });
    } catch (erro) {
        console.error("Erro ao carregar histórico:", erro);
        container.innerHTML = "<p class='text-center text-danger mt-3'>Erro ao carregar histórico.</p>";
    }
}

function criarItemDoHistorico(container, item) {
    // Blocos principais para cada item
    const bloco = document.createElement("div");
    bloco.classList.add("item-historico");
    // Área da esquerda
    const esquerda = document.createElement("div");
    esquerda.classList.add("historico-esquerda");
    // miniatura
    const img = document.createElement("img");
    img.src = item.imageBase64;
    img.classList.add("thumb");
    // texto limitado a 60 char
    const texto = document.createElement("p");
    texto.classList.add("prompt-texto");
    texto.innerText =
        item.prompt.length > 60 ? item.prompt.substring(0, 60) + "..." : item.prompt;
    // texto e imagem dentro da div
    esquerda.appendChild(img);
    esquerda.appendChild(texto);
    // Wrapper para o menu e os 3 pontos
    const menuWrapper = document.createElement("div");
    menuWrapper.classList.add("menu-wrapper");

    const pontos = document.createElement("span");
    pontos.classList.add("pontos");
    pontos.innerHTML = "⋮"; 
    // criando menu com opções
    const menu = document.createElement("div");
    menu.classList.add("menu-opcoes");
    const opc1 = document.createElement("div");
    opc1.innerText = "Salvar imagem";
    opc1.onclick = () => copiarImagem(item.imageBase64);
    const opc2 = document.createElement("div");
    opc2.innerText = "Copiar prompt";
    opc2.onclick = () => copiarPrompt(item.prompt);
    const opc3 = document.createElement("div");
    opc3.innerText = "Apagar do histórico";
    opc3.onclick = () => apagarHistorico(item._id, bloco);
    // adicionando opções ao menu
    menu.appendChild(opc1);
    menu.appendChild(opc2);
    menu.appendChild(opc3);
    // adicionando o pontos e o menu
    menuWrapper.appendChild(pontos);
    menuWrapper.appendChild(menu);

    pontos.onclick = (e) => {
        // evita que os cliques foram fechem o menu instantaneamente
        e.stopPropagation();
        
        document.querySelectorAll(".menu-opcoes.ativo").forEach(m => {
            if(m !== menu) m.classList.remove("ativo");
        });

        menu.classList.toggle("ativo");
    };
    bloco.appendChild(esquerda);
    bloco.appendChild(menuWrapper);
    container.appendChild(bloco);
}

const abaHistoricoBtn = document.getElementById("aba-historico");
if (abaHistoricoBtn) {
    abaHistoricoBtn.addEventListener("click", () => {
        carregarHistorico("historico-container");
    });
}

const modalHistoricoMobile = document.getElementById('modalHistoricoMobile');
if (modalHistoricoMobile) {
    modalHistoricoMobile.addEventListener('shown.bs.modal', () => {
        console.log("Modal mobile aberto, carregando histórico...");
        carregarHistorico("historico-mobile-container");
    });
}


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

    alert("Imagem salva!");
}

async function apagarHistorico(id, elementoHTML) {
    if (!confirm("Tem certeza que deseja apagar este item?")) return;

    try {
        const url = `http://localhost:3000/historico/${id}`;

        await axios.delete(url);

        elementoHTML.remove();

        const container = elementoHTML.parentElement;
        if (container && container.children.length === 0) {
            container.innerHTML = "<p class='text-center text-muted mt-3'>Nenhum item no histórico.</p>";
        }

    } catch (err) {
        console.error("Erro ao apagar:", err);
        alert("Erro ao remover do histórico.");
    }
}

document.addEventListener("click", () => {
    document.querySelectorAll(".menu-opcoes.ativo")
        .forEach(menu => menu.classList.remove("ativo"));
});