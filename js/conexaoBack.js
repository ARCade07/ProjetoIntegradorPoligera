const mensagem_usuario = document.querySelector('#chat');
const botao = document.querySelector('#enviar');
const loading = document.querySelector(".loading");
const resposta_gerada = document.querySelector(".resposta");
const protocolo = "http://";
const baseURL = "localhost:5000";
const chatEndpoint = "/chat";

// so habilitará o botão quando o usuário tiver escrevido alguma coisa no campo do prompt
mensagem_usuario.addEventListener('input', function() {
    // trim() elimina espaços em branco
    if(mensagem_usuario.value.trim().length > 0) {
        botao.disabled = false;
    }
    else {
        botao.disabled = true;
    }
})

// declaração da função callback 
// (função passada como parâmetro de outra função para ser posteriormente executada em resposta a ocorrência de determinado evento)
async function tratamentoPrompt(event) {
    const URLcompleta = `${protocolo}${baseURL}${chatEndpoint}`

    // para que o navegador não recarregue a página
    event.preventDefault();

    const prompt = mensagem_usuario.value;

    mensagem_usuario.value = '';
    
    // mostra a mensagem de loading
    loading.style.display = 'block';
    
    try {
        // requisição post para o back que devolve a reposta gerada pela IA
        const response = await axios.post(URLcompleta, {prompt: prompt})
        resposta_gerada.innerHTML = `
            <img class="imagem-gerada" src="${response.data.resposta}" alt="imagem gerada">
            <button onclick="copiarImagem()">
                <ion-icon name="copy-outline" class="copy-icon"></ion-icon>
            </button>
        `;
    }
    catch (e) {
        console.log(e);
    
    // é executado independentemente do bloco try ou catch
    }
    finally {
        loading.style.display = 'none';
        botao.disabled = true; 
    }
}

// adiciona um listener para quando o usuário digitar o prompt e clicar no botão de enviar da interface
botao.addEventListener('click', tratamentoPrompt);

// adiciona um listener para quando o usuário digitar o prompt e pressionar a tecla enter do teclado
if(mensagem_usuario) {
    mensagem_usuario.addEventListener('keypress', function(e) {
        if(e.key === 'Enter') {
            tratamentoPrompt(e);
        }
    });
}

// função que copia a imagem quando o botão é clicado
async function copiarImagem() {
    // pega a imagem na árvore doom
    const imagem = document.querySelector('.imagem-gerada')
    try{
        // utiliza fetch para baixar a imagem atraves de seu endereço 'image.src'
        const imagemBaixada = await fetch(imagem.src)
        // converte a imagem baixada para blob
        const imagemBlob = await imagemBaixada.blob()
        // criação de um item de área de transferência
        const clipboardItem = new ClipboardItem({ [imagemBlob.type]: imagemBlob})
        // copia a imagem para a área de transferência
        // navigator.clipboard.write é uma API de copiar imagens
        await navigator.clipboard.write([clipboardItem])
        // manda um alerta 
        alert('Imagem copiada')
    }
    catch (e) {
        console.log(e)
        alert('Erro ao copiar imagem')
    }
}