const abaCriacao = document.getElementById('aba-criacao');
const abaHistorico = document.getElementById('aba-historico');
const conteudoCriacao = document.getElementById('conteudo-criacao');
const conteudoHistorico = document.getElementById('conteudo-historico');

if (abaCriacao && abaHistorico) { 
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
}


function selecionarMateria(selecionado, naoSelecionado) {
    if (selecionado && naoSelecionado) {
        selecionado.style.backgroundColor = '#1EB4C3'
        selecionado.style.color = '#00363C'
        selecionado.style.border = 'none';

        naoSelecionado.style.backgroundColor = '#BBE8EE';
        naoSelecionado.style.color = '#3F696F'
        naoSelecionado.style.border = '3px solid #3F696F';
    }
}

const desktopContainer = document.querySelector('.barra-lateral');

if (desktopContainer) {
    const desktopBotaoFisica = desktopContainer.querySelector('.botao-fisica');
    const desktopBotaoQuimica = desktopContainer.querySelector('.botao-quimica');
    const desktopConteudoQuimica = desktopContainer.querySelector('.conteudo-quimica');
    const desktopConteudoFisicaTodos = desktopContainer.querySelectorAll('.conteudo-fisica');
    const desktopComboboxContainer = desktopContainer.querySelector('.combobox-customizado-container');
    const selectVerdadeiro = document.getElementById('areas');
    
    desktopBotaoFisica.addEventListener('click', () => {
        selecionarMateria(desktopBotaoFisica, desktopBotaoQuimica);
        desktopConteudoQuimica.classList.remove('active');
        desktopComboboxContainer.style.display = '';
        let selectedValue = selectVerdadeiro.value;
        if (!selectedValue) {
            selectedValue = 'mecanica';
            selectVerdadeiro.value = 'mecanica';
            
            const combobox = desktopComboboxContainer.querySelector('.combobox-customizado');
            const defaultOption = desktopComboboxContainer.querySelector('.opcoes li[data-value="mecanica"]');
            if (combobox && defaultOption) {
                combobox.textContent = defaultOption.textContent.trim();
            }
        }

        desktopConteudoFisicaTodos.forEach(conteudo => {
            conteudo.classList.remove('active');
        });

        const conteudoSelecionado = desktopContainer.querySelector(`.conteudo-fisica.${selectedValue}`);
        if (conteudoSelecionado) {
            conteudoSelecionado.classList.add('active');
        }
    });

    desktopBotaoQuimica.addEventListener('click', () => {
        selecionarMateria(desktopBotaoQuimica, desktopBotaoFisica);
        desktopComboboxContainer.style.display = 'none';
        desktopConteudoFisicaTodos.forEach(conteudo => {
            conteudo.classList.remove('active');
        });
        desktopConteudoQuimica.classList.add('active');
    });

    const combobox = desktopComboboxContainer.querySelector('.combobox-customizado');
    const opcoes = desktopComboboxContainer.querySelector('.opcoes');
    const todasOpcoes = desktopComboboxContainer.querySelectorAll('.opcoes li');

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

            desktopConteudoFisicaTodos.forEach(conteudo => {
                conteudo.classList.remove('active');
            });
            const conteudoSelecionado = desktopContainer.querySelector(`.conteudo-fisica.${selectedValue}`);
            if (conteudoSelecionado) {
                conteudoSelecionado.classList.add('active');
            }
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
}

const mobileHeader = document.querySelector('.mobile-header');
const mobileFooter = document.querySelector('.mobile-footer');

if (mobileHeader && mobileFooter) {
    const mobileBotaoFisica = mobileHeader.querySelector('.botao-fisica');
    const mobileBotaoQuimica = mobileHeader.querySelector('.botao-quimica');
    const mobileConteudoQuimica = mobileFooter.querySelector('.conteudo-quimica');
    const mobileConteudoFisicaTodos = mobileFooter.querySelectorAll('.conteudo-fisica');
    
    mobileBotaoFisica.addEventListener('click', () => {
        selecionarMateria(mobileBotaoFisica, mobileBotaoQuimica);
        mobileConteudoQuimica.classList.remove('active');
        mobileConteudoFisicaTodos.forEach(conteudo => {
            conteudo.classList.add('active');
        });
        const primeiraFisica = mobileFooter.querySelector('.conteudo-fisica.eletrica')
        if (primeiraFisica) {
            primeiraFisica.classList.add('active')
        }
    });
    
    mobileBotaoQuimica.addEventListener('click', () => {
        selecionarMateria(mobileBotaoQuimica, mobileBotaoFisica);
        mobileConteudoFisicaTodos.forEach(conteudo => {
            conteudo.classList.remove('active');
        });
        mobileConteudoQuimica.classList.add('active');
    });
}