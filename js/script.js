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

const comboboxContainer = document.querySelector('.combobox-customizado-container');
const combobox = comboboxContainer.querySelector('.combobox-customizado');
const opcoes = comboboxContainer.querySelector('.opcoes');
const todasOpcoes = comboboxContainer.querySelectorAll('.opcoes li');
const selectVerdadeiro = document.getElementById('areas');

combobox.addEventListener('click', (e) => {
    e.stopPropagation();
    opcoes.classList.toggle('active');
    combobox.classList.toggle('open');
});

todasOpcoes.forEach(option => {
    option.addEventListener('click', () => {
        const selectedText = option.textContent.trim();
        const selectedValue = option.dataset.value;
        combobox.textContent = selectedText;
        selectVerdadeiro.value = selectedValue;
        opcoes.classList.remove('active');
        combobox.classList.remove('open');
    });
});

window.addEventListener('click', () => {
    if (opcoes.classList.contains('active')) {
        opcoes.classList.remove('active');
        combobox.classList.remove('open');
    }
});

combobox.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        combobox.click();
    }
});