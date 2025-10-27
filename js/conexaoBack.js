const campo_texto = document.querySelector('#form-prompt');
const mensagem_usuario = document.querySelector('#chat');
const botao = document.querySelector('#enviar');
const loading = document.querySelector(".loading");
const resposta_gerada = documnt.querySelector(".resposta-gerada");
const protocolo = "http://";
const baseURL = "localhost:5000";
const chatEndpoint = "/chat";

mensagem_usuario.addEventListener('input', function() {
    if(prompt_enviado.value.trim().length > 0) {
        botao.disabled = false;
    }
    else {
        botao.disabled = true;
    }
})

async function tratamentoPrompt(event) {
    constURLcompleta = `${protocolo}${baseURL}${chatEndpoint}`

    event.preventDefault();

    const prompt = mensagem_usuario.value;

    mensagem_usuario.value = '';
    
    loading.style.display = 'block';
    resposta_gerada.innerHTML = '';
    
    try {
        const response = await axios.post(URLcompleta, {prompt: 'prompt'})

        resposta_gerada.innerHTML = `
        <h3>${response.data.message}</h3>
        `;
    }
    catch (e) {
        console.log(e);
        
    }
    finally {
        loading.style.display = 'none';
        botao.disabled = true; 
    }
}

campo_texto.addEventListener('submit', tratamentoPrompt)