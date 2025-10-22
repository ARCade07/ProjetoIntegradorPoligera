const botaoFisica = document.querySelector('.botao-fisica');
const botaoQuimica = document.querySelector('.botao-quimica');

function selecionarMateria(selecionado, naoSelecionado) {
    selecionado.style.backgroundColor = '#1EB4C3'
    selecionado.style.color = '#00363C'
    selecionado.style.border = 'none';

    naoSelecionado.style.backgroundColor = '#BBE8EE';
    naoSelecionado.style.color = '#3F696F'
    naoSelecionado.style.border = '3px solid #3F696F';
}

botaoFisica.addEventListener('click', () => {
    selecionarMateria(botaoFisica, botaoQuimica);
});

botaoQuimica.addEventListener('click', () => {
    selecionarMateria(botaoQuimica, botaoFisica);
});

const abaCriacao = document.getElementById('aba-criacao');
const abaHistorico = document.getElementById('aba-historico');
const conteudoCriacao = document.getElementById('conteudo-criacao');
const conteudoHistorico = document.getElementById('conteudo-historico');

abaCriacao.addEventListener('click', () => {
    abaCriacao.classList.add('ativa');
    abaHistorico.classList.remove('ativa');

    conteudoCriacao.classList.remove('hidden');
    conteudoHistorico.classList.add('hidden');
});

abaHistorico.addEventListener('click', () => {
    abaHistorico.classList.add('ativa');
    abaCriacao.classList.remove('ativa');

    conteudoHistorico.classList.remove('hidden');
    conteudoCriacao.classList.add('hidden');
});