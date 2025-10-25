const protocolo = 'http://';
const baseURL = 'localhost:3000';
const endpointAutenticacao = "/autenticacao"

async function cadastrarUsuario () {
    let usuarioCadastroInput = document.querySelector('#nome');
    let emailCadastroInput = document.querySelector('#email-cadastro');
    let passwordCadastroInput = document.querySelector('#senha');
    let confirmPasswordCadastroInput = document.querySelector('#confirmar-senha')
    let usuarioCadastro = usuarioCadastroInput.value;
    let emailCadastro = emailCadastroInput.value;
    let passwordCadastro = passwordCadastroInput.value;
    let confirmPasswordCadastro = confirmPasswordCadastroInput.value;
    if (usuarioCadastro && emailCadastro && passwordCadastro && confirmPasswordCadastro) {
        try {
            const cadastroEndpoint = '/cadastrar';
            const URLcompleta = `${protocolo}${baseURL}${endpointAutenticacao}${cadastroEndpoint}`;
            await axios.post (
                URLcompleta,
                {name: usuarioCadastro, email: emailCadastro, password: passwordCadastro, confirmpassword: confirmPasswordCadastro}
            );
            usuarioCadastroInput.value = '';
            emailCadastroInput.value = '';
            passwordCadastroInput.value = '';
            confirmPasswordCadastroInput.value = '';
        } catch (erro) {
            console.log(erro);
        }
    }

}