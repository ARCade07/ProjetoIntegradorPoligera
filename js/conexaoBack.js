const mensagem_usuario = document.querySelector('#chat');
const botao = document.querySelector('#enviar');
const loading = document.querySelector(".loading");
const resposta_gerada = document.querySelector(".reposta");
const protocolo = "http://";
const baseURL = "localhost:5000";
const chatEndpoint = "/chat";

mensagem_usuario.addEventListener('input', function() {
    if(mensagem_usuario.value.trim().length > 0) {
        botao.disabled = false;
    }
    else {
        botao.disabled = true;
    }
})

async function tratamentoPrompt(event) {
    const URLcompleta = `${protocolo}${baseURL}${chatEndpoint}`

    event.preventDefault();

    const prompt = mensagem_usuario.value;

    mensagem_usuario.value = '';
    
    loading.style.display = 'block';
    // resposta_gerada.innerHTML = '';
    
    try {
        const response = await axios.post(URLcompleta, {prompt: prompt})

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


botao.addEventListener('click', tratamentoPrompt);

if(mensagem_usuario) {
    mensagem_usuario.addEventListener('keypress', function(e) {
        if(e.key === 'Enter') {
            tratamentoPrompt(e);
        }
    });
}