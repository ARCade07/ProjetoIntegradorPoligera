axios.defaults.withCredentials = true;
const protocolo = 'http://';
const baseURL = 'localhost:3000';
const endpointAutenticacao = '/autenticacao';


async function cadastrarUsuario() {
    let usuarioCadastroInput = document.querySelector('#nome');
    let emailCadastroInput = document.querySelector('#email-cadastro');
    let passwordCadastroInput = document.querySelector('#senha');
    let confirmPasswordCadastroInput = document.querySelector('#confirmar-senha');
    let usuarioCadastro = usuarioCadastroInput.value;
    let emailCadastro = emailCadastroInput.value.toLowerCase();
    let passwordCadastro = passwordCadastroInput.value;
    let confirmPasswordCadastro = confirmPasswordCadastroInput.value;
    if (usuarioCadastro && emailCadastro && passwordCadastro && confirmPasswordCadastro) {
        try {
            const cadastroEndpoint = '/cadastrar';
            const URLcompleta = `${protocolo}${baseURL}${endpointAutenticacao}${cadastroEndpoint}`;
            const response = await axios.post(
                URLcompleta,
                { name: usuarioCadastro, email: emailCadastro, password: passwordCadastro, confirmpassword: confirmPasswordCadastro }
            );
            usuarioCadastroInput.value = '';
            emailCadastroInput.value = '';
            passwordCadastroInput.value = '';
            confirmPasswordCadastroInput.value = '';
            exibirAlerta('.alert-form-cadastro', 'Cadastro efetuado com sucesso!', ['show', 'alert-success'], ['d-none', 'alert-danger'], 2000);
            if (response.data.success) {
                setTimeout(() => {
                    window.location.href = '../login.html'
                }, 2000);
            }
        } catch (erro) {
            exibirAlerta('.alert-form-cadastro', 'Não foi possível realizar o cadastro', ['show', 'alert-danger'], ['d-none', 'alert-sucess'], 2000);
        }
    }
    else {
        exibirAlerta('.alert-form-cadastro', 'Preencha todos os campos', ['show', 'alert-warning'], ['d-none', 'alert-success'], 2000);
    }

}
async function fazerLogin() {
    let emailLoginInput = document.querySelector('#email-login');
    let passwordLoginInput = document.querySelector('#senha-login');
    let emailLogin = emailLoginInput.value.toLowerCase();
    let passwordLogin = passwordLoginInput.value;
    if (emailLogin && passwordLogin) {
        try {
            const loginEndpoint = '/login';
            const URLcompleta = `${protocolo}${baseURL}${endpointAutenticacao}${loginEndpoint}`;
            const response = await axios.post(
                URLcompleta,
                { email: emailLogin, password: passwordLogin },
                { withCredentials: true }
            );
            console.log(response.data);
            emailLoginInput.value = '';
            passwordLoginInput.value = '';
            localStorage.setItem("userId", response.data.userId);
            exibirAlerta('.alert-form-login', 'Login efetuado com sucesso!', ['show', 'alert-success'], ['d-none', 'alert-danger'], 2000);
            setTimeout(() => {
                window.location.href = '/';
            }, 2500);
        } catch (erro) {
            exibirAlerta('.alert-form-login', 'O e-mail e/ou senha digitados estão incorretos.', ['show', 'alert-danger'], ['d-none', 'alert-sucess'], 2000);
        }
    }
    else {
        exibirAlerta('.alert-form-login', 'Preencha todos os campos', ['show', 'alert-warning'], ['d-none', 'alert-success'], 2000);
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
                { email: emailRecuperar }
            );
            emailRecuperarInput.value = '';
            exibirAlerta('.alert-form-esquecersenha', 'O email para recuperação de senha foi enviado.', ['show', 'alert-success'], ['d-none', 'alert-danger'], 2000);
        } catch (erro) {
            exibirAlerta('.alert-form-esquecersenha', 'Não existe usuário vinculado à esse endereço de email.', ['show', 'alert-danger'], ['d-none', 'alert-success'], 2000);
        }
    }
    else {
        exibirAlerta('.alert-form-esquecersenha', 'Digite um email válido.', ['show', 'alert-warning'], ['d-none', 'alert-success'], 2000);
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
    if (!email || !resetToken) {
        exibirAlerta('.alert-form-redefinirsenha', 'Link inválido. Por favor, solicite uma nova redefinição de senha.', ['show', 'alert-danger'], ['d-none', 'alert-success'], 2000);
    }
    if (passwordRedefinir && confirmPasswordRedefinir) {
        if (passwordRedefinir !== confirmPasswordRedefinir) {
            exibirAlerta('.alert-form-redefinirsenha', 'É necessário que as ambas as senhas sejam iguais.', ['show', 'alert-danger'], ['d-none', 'alert-success'], 2000);
        }
        else {
            try {
                const redefinirSenhaEnpoint = '/redefinir-senha';
                const URLcompleta = `${protocolo}${baseURL}${endpointAutenticacao}${redefinirSenhaEnpoint}`;
                const response = await axios.post(
                    URLcompleta,
                    { email, resetToken, newPassword: passwordRedefinir }
                );
                exibirAlerta('.alert-form-redefinirsenha', 'Senha redefinida com sucesso!', ['show', 'alert-success'], ['d-none', 'alert-danger'], 2000);
                passwordRedefinirInput.value = '';
                confirmPasswordRedefinirInput.value = '';
                if (response.data.success) {
                    window.location.href = '../login.html';
                }
            } catch (erro) {
                exibirAlerta('.alert-form-redefinirsenha', 'Não foi possível redefinir a senha. Tente novamente.', ['show', 'alert-danger'], ['d-none', 'alert-success'], 2000);
            }
        }
    }
    else {
        exibirAlerta('.alert-form-esquecersenha', 'Digite a sua nova senha e a sua confirmação.', ['show', 'alert-warning'], ['d-none', 'alert-success'], 2000);
    }
}
async function verificarToken() {
    try {
        const verificarTokenEnpoint = '/check-token';
        const URLcompleta = `${protocolo}${baseURL}${endpointAutenticacao}${verificarTokenEnpoint}`;
        const response = await axios.post(
            URLcompleta,
            { withCredentials: true }
        );
        if (response.status === 200) {
            window.location.href = 'index.html';
        }
    } catch (erro) {
        console.error('Token inválido ou ausente', erro);
        window.location.href = 'login.html';
    }
}

async function fazerLogout() {
    try {
        await axios.post('http://localhost:3000/autenticacao/logout', {}, {
            withCredentials: true
        });
        window.location.href = 'login.html';
    } catch (erro) {
        console.error('Erro ao fazer logout:', erro);
    }
}

function exibirAlerta(seletor, innerHTML, classesToAdd, classesToRemove, timeout) {
    let alert = document.querySelector(seletor);
    alert.innerHTML = innerHTML;
    //'...' é o spread operator
    //quado aplicado a um array, ele 'desmembra' o array
    //depois disso, passamos os elementos do array como argumentos para add e remove
    alert.classList.add(...classesToAdd);
    alert.classList.remove(...classesToRemove);
    setTimeout(() => {
        alert.classList.remove('show');
        alert.classList.add('d-none');
    }, timeout);
}
function ativarEnter(seletor, funcao) {
    const form = document.querySelector(seletor);

    if (!form) return;

    form.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            e.preventDefault();
            funcao();
        }
    });
}

ativarEnter('.login', fazerLogin);
ativarEnter('.campos-preenchimento', cadastrarUsuario);
ativarEnter('.recuperar', esquecerSenha);
ativarEnter('.nova-senha-form', redefinirSenha);