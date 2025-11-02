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
            const response = await axios.post (
                URLcompleta,
                {name: usuarioCadastro, email: emailCadastro, password: passwordCadastro, confirmpassword: confirmPasswordCadastro}
            );
            usuarioCadastroInput.value = '';
            emailCadastroInput.value = '';
            passwordCadastroInput.value = '';
            confirmPasswordCadastroInput.value = '';
            if (response.data.success) {
                window.location.href = "../login.html"
            }
        } catch (erro) {
            console.log(erro);
        }
    }

}
async function fazerLogin() {
    let emailLoginInput = document.querySelector('#email-login');
    let passwordLoginInput = document.querySelector('#senha-login');
    let emailLogin = emailLoginInput.value;
    let passwordLogin = passwordLoginInput.value;
    if (emailLogin && passwordLogin) {
        try {
            const loginEndpoint = '/login';
            const URLcompleta = `${protocolo}${baseURL}${endpointAutenticacao}${loginEndpoint}`;
            const response = await axios.post(
                URLcompleta,
                {email: emailLogin, password: passwordLogin}
            );
            console.log(response.data);
            emailLoginInput.value = '';
            passwordLoginInput.value = '';
        } catch(erro) {
            console.log(erro);
        }
    }

}
async function esquecerSenha() {
    let emailRecuperarInput = document.querySelector('#email-recuperar');
    let emailRecuperar = emailRecuperarInput.value;
    if (emailRecuperar) {
        try {
            const esquecerSenhaEndpoint = '/esqueceu-senha';
            const URLcompleta = `${protocolo}${baseURL}${endpointAutenticacao}${esquecerSenhaEndpoint}`;
            const response = await axios.post(
                URLcompleta,
                {email: emailRecuperar}
            );
            emailRecuperarInput.value = '';
        } catch (erro) {
            console.log(erro);
        }
    }
}
async function redefinirSenha() {
    let passwordRedefinirInput = document.querySelector('#senha-redefinir');
    let confirmPasswordRedefinirInput = document.querySelector('#confirmar-senha-redefinir');

    let passwordRedefinir = passwordRedefinirInput.value;
    let confirmPasswordRedefinir = confirmPasswordRedefinirInput.value;

    const params = new URLSearchParams(window.location.search);
    const email = params.get('email');
    const resetToken = params.get('token');
    
    if(!email || !resetToken) {
        alert('Link inválido. Por favor, solicite uma nova redefinição de senha');
    }
    if (passwordRedefinir && confirmPasswordRedefinir) {
        if (passwordRedefinir !== confirmPasswordRedefinir) {
            alert('As senhas não conferem');
        }
        try {
            const redefinirSenhaEnpoint = '/redefinir-senha';
            const URLcompleta = `${protocolo}${baseURL}${endpointAutenticacao}${redefinirSenhaEnpoint}`;
            await axios.post(
                URLcompleta,
                { email, resetToken, newPassword: passwordRedefinir }
            );
            passwordRedefinirInput.value = '';
            confirmPasswordRedefinirInput.value = '';
        } catch (erro) {
            console.log(erro);
        }
    }
}