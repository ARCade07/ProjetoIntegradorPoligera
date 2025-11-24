const mensagemUsuario = document.querySelector('#chat');
const botao = document.querySelector('#enviar');
const loading = document.querySelector(".loading");
const resposta_gerada = document.querySelector(".resposta");
const protocolo = "http://";
const baseURL = "127.0.0.1:5000";
const chatEndpoint = "/chat";

function ativarBotaoEnviar () {
    const escreveuPrompt = mensagemUsuario.value.trim().length > 0
    const selecionouIcones = itensSelecionados.length > 0

    botao.disabled = !(escreveuPrompt || selecionouIcones)
}

mensagemUsuario.addEventListener('input', ativarBotaoEnviar)

function registrarEstatistica(tipo, materia, area, icones) {
    try {
        let eventos = JSON.parse(localStorage.getItem('eventosPoligera')) || [];
        eventos.push({
            tipo: tipo,
            materia: materia,
            area: area,
            icones: icones,
            hora: new Date().getHours(),
            data: new Date().toISOString
        });

        localStorage.setItem('eventosPoligera', JSON.stringfy(eventos));
        console.log('Estatística registrada: ', eventos[eventos.length - 1]);
    }
    catch(error) {
        console.error('Erro ao registrar estatística no localStorage: ', error)
    }
}

// declaração da função callback 
// (função passada como parâmetro de outra função para ser posteriormente executada em resposta a ocorrência de determinado evento)
async function tratamentoPrompt(event) {
    const URLcompleta = `${protocolo}${baseURL}${chatEndpoint}`

    // para que o navegador não recarregue a página
    event.preventDefault();

    const prompt = mensagemUsuario.value;

    mensagemUsuario.value = '';
    resposta_gerada.innerHTML = "";
    
    // mostra a mensagem de loading
    loading.style.display = 'block';

    const materiaInfo = obterMateriaArea()
    const itensSelecionados = enviarItensSelecionados()

    let tipoImagemSelecionado = document.querySelector('input[name="modo-switch-desktop"]:checked')
    if (!tipoImagemSelecionado) {
        tipoImagemSelecionado = document.querySelector('input[name="modo-switch"]:checked')
    }

    const labelImagemSelecionada = tipoImagemSelecionado ? 
        document.querySelector(`label[for="${tipoImagemSelecionado.id}"]`).textContent.trim() : 
        'Técnico';
    
    console.log('Tipo de imagem selecionada:', labelImagemSelecionada);
    
    try {
        // requisição post para o back que devolve a reposta gerada pela IA
        const userId = localStorage.getItem("userId");
        const response = await axios.post(URLcompleta, {prompt: prompt, elementos: itensSelecionados, materia: materiaInfo.materia, area: materiaInfo.area, tipo: labelImagemSelecionada, userId})
        resposta_gerada.innerHTML = `
            <img class="imagem-gerada" src="${response.data.resposta}" alt="imagem gerada">
            <button onclick="copiarImagemGerada()">
                <ion-icon name="copy-outline" class="copy-icon"></ion-icon>
            </button>
            <a href="${response.data.resposta}" download="imagem-gerada.jpg">
                <ion-icon name="download-outline"></ion-icon>
            </a>
        `;

        registrarEstatistica(
            labelImagemSelecionada, 
            materiaInfo.materia, 
            materiaInfo.area, 
            itensSelecionados
        );
    }
    catch (e) {
        console.error("Erro:", e);

        let mensagemErro = 'Erro ao conectar-se com o servidor. Verifique a sua conexão'

        // para o caso de o servidor ter respondido com um erro
        if (e.response){
            mensagemErro = 'Verifique se você esta na área correta'
        }
        // requisição foi feita mas não houve resposta
        else if (e.request){
            mensagemErro = e.message
            
        }

        resposta_gerada.innerHTML = `
            <div class="mensagem-erro">
                <ion-icon name="alert-circle-outline" class="icone-erro"></ion-icon>
                <p>ERRO</p>
                <p>${mensagemErro}</p>
                <p class="mensagem-tente-novamente">Por favor, tente novamente.</p>
            </div>
        `;
    
    
    }
    // é executado independentemente do bloco try ou catch
    finally {
        loading.style.display = 'none';
        botao.disabled = true; 
        limparSelecao();
    }
}

// adiciona um listener para quando o usuário digitar o prompt e clicar no botão de enviar da interface
botao.addEventListener('click', tratamentoPrompt);

// adiciona um listener para quando o usuário digitar o prompt e pressionar a tecla enter do teclado
if(mensagemUsuario) {
    mensagemUsuario.addEventListener('keypress', function(e) {
        if(e.key === 'Enter') {
            tratamentoPrompt(e);
        }
    });
}

// função que copia a imagem quando o botão é clicado
async function copiarImagemGerada() {
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