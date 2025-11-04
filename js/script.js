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
        selecionado.style.backgroundColor = '#1EB4C3';
        selecionado.style.color = '#00363C';
        selecionado.style.border = 'none';

        naoSelecionado.style.backgroundColor = '#BBE8EE';
        naoSelecionado.style.color = '#3F696F';
        naoSelecionado.style.border = '3px solid #3F696F';
    }
}

let itensSelecionados = [];

function sincronizarItens () {
    const todosBotoes = document.querySelectorAll('.itens, .item-mobile-icon');

    todosBotoes.forEach(botao => {
        const img = botao.querySelector('img');
        if (!img) return;
        const identificador = img.alt;

        if (itensSelecionados.includes(identificador)) {
            botao.classList.add('selecionado');
        }
        else {
            botao.classList.remove('selecionado');
        }
    })
}

function atualizarSelecionados (botao) {
    const img = botao.querySelector('img');
    if (!img) return;
    const identificador = img.alt;
    const index = itensSelecionados.indexOf(identificador);

    if (index >= 0) {
        itensSelecionados.splice(index, 1);
    }
    else {
        itensSelecionados.push(identificador);
    }

    sincronizarItens();

    console.clear();
    console.log("Itens selecionados (na ordem):", itensSelecionados);
}

function enviarItensSelecionados () {
    return itensSelecionados;
}

const desktopContainer = document.querySelector('.barra-lateral');

let materiaArea = {
    materia: 'fisica',
    area: 'mecanica'
}

function atualizarAreaSelecionada(materia, area = null) {
    materiaArea.materia = materia;
    if (area) {
        materiaArea.area = area;
    }
}

// função para enviar a matéria e a área selecionadas para o backend.js
function obterMateriaArea() {
    console.log('→ Obtendo área selecionada:', materiaArea);
    return materiaArea;
}

if (desktopContainer) {
    const desktopBotaoFisica = desktopContainer.querySelector('.botao-fisica');
    const desktopBotaoQuimica = desktopContainer.querySelector('.botao-quimica');
    const desktopConteudoQuimica = desktopContainer.querySelector('.conteudo-quimica');
    const desktopConteudoFisicaTodos = desktopContainer.querySelectorAll('.conteudo-fisica');
    const desktopComboboxContainer = desktopContainer.querySelector('.combobox-customizado-container');
    const selectVerdadeiro = document.getElementById('areas');
    const itens = document.querySelectorAll('.itens');
    
    desktopBotaoFisica.addEventListener('click', () => {
        selecionarMateria(desktopBotaoFisica, desktopBotaoQuimica);
        atualizarAreaSelecionada('fisica')
        desktopConteudoQuimica.classList.remove('active');
        desktopComboboxContainer.style.display = '';
        let selectedValue = selectVerdadeiro.value;
        if (!selectedValue) {
            const combobox = desktopComboboxContainer.querySelector('.combobox-customizado');
            const defaultOption = desktopComboboxContainer.querySelector('.opcoes li[data-value="mecanica"]');
            if (combobox && defaultOption) {
                combobox.textContent = defaultOption.textContent.trim();
            }
        }

        desktopConteudoFisicaTodos.forEach(conteudo => {
            conteudo.classList.remove('active');
        });

        const conteudoSelecionado = desktopContainer.querySelector(`.barra-lateral .conteudo-fisica.${selectedValue}`);
        if (conteudoSelecionado) {
            conteudoSelecionado.classList.add('active');
        }
    });

    desktopBotaoQuimica.addEventListener('click', () => {
        selecionarMateria(desktopBotaoQuimica, desktopBotaoFisica);
        atualizarAreaSelecionada('quimica')
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
            atualizarAreaSelecionada('fisica', selectedValue)
            combobox.textContent = selectedText;
            selectVerdadeiro.value = selectedValue;
            opcoes.classList.remove('active');
            combobox.classList.remove('open');

            desktopConteudoFisicaTodos.forEach(conteudo => {
                conteudo.classList.remove('active');
            });
            const conteudoSelecionado = desktopContainer.querySelector(`.barra-lateral .conteudo-fisica.${selectedValue}`);
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

    itens.forEach(item =>{
        item.addEventListener('click', () =>{
            atualizarSelecionados(item);
        })
    })

    desktopBotaoFisica.click();
}

const mobileHeader = document.querySelector('.mobile-header');
const mobileFooter = document.querySelector('.mobile-footer');

if (mobileHeader && mobileFooter) {
    const mobileBotaoFisica = mobileFooter.querySelector('.botao-fisica');
    const mobileBotaoQuimica = mobileFooter.querySelector('.botao-quimica');
    const mobileConteudoFisica = mobileFooter.querySelector('.conteudo-fisica');
    const mobileConteudoQuimica = mobileFooter.querySelector('.conteudo-quimica');
    const mobileAreasFisica = mobileFooter.querySelector('.areas-fisica');
    const mobileConteudoMecanica = mobileFooter.querySelector('.icones-lista.mecanica');
    const mobileConteudoEletrica = mobileFooter.querySelector('.icones-lista.eletrica');
    const mobileConteudoOptica = mobileFooter.querySelector('.icones-lista.optica');
    const mobileBotoesArea = mobileAreasFisica.querySelectorAll('.botao-area');
    const itensMobile = mobileFooter.querySelectorAll('.item-mobile-icon');

    function resetMobileView() {
        mobileConteudoFisica.classList.remove('active');
        mobileConteudoQuimica.classList.remove('active');
        
        if (mobileConteudoMecanica) mobileConteudoMecanica.classList.remove('active');
        if (mobileConteudoEletrica) mobileConteudoEletrica.classList.remove('active');
        if (mobileConteudoOptica) mobileConteudoOptica.classList.remove('active');

        mobileConteudoFisica.classList.remove('area-selecionada');

        mobileBotoesArea.forEach(btn => {
            btn.classList.remove('selecionado');
        });
    }

    mobileBotaoFisica.addEventListener('click', () => {
        selecionarMateria(mobileBotaoFisica, mobileBotaoQuimica);
        resetMobileView();
        atualizarAreaSelecionada('fisica', 'mecanica')
        
        mobileConteudoFisica.classList.add('active');
    });
    
    mobileBotaoQuimica.addEventListener('click', () => {
        selecionarMateria(mobileBotaoQuimica, mobileBotaoFisica);
        resetMobileView();
        atualizarAreaSelecionada('quimica')
        
        mobileConteudoQuimica.classList.add('active');
    });

    mobileBotoesArea.forEach(botao => {
        botao.addEventListener('click', () => {
            const area = botao.dataset.area;
            atualizarAreaSelecionada('fisica', area)

            mobileBotoesArea.forEach(btn => btn.classList.remove('selecionado'));
            botao.classList.add('selecionado');

            mobileConteudoFisica.classList.add('area-selecionada');

            if (mobileConteudoMecanica) mobileConteudoMecanica.classList.remove('active');
            if (mobileConteudoEletrica) mobileConteudoEletrica.classList.remove('active');
            if (mobileConteudoOptica) mobileConteudoOptica.classList.remove('active');

            if (area === 'mecanica' && mobileConteudoMecanica) {
                mobileConteudoMecanica.classList.add('active');
            } else if (area === 'eletrica' && mobileConteudoEletrica) {
                mobileConteudoEletrica.classList.add('active');
            } else if (area === 'optica' && mobileConteudoOptica) {
                mobileConteudoOptica.classList.add('active');
            }
        });
    });

    itensMobile.forEach(item => {
        item.addEventListener('click', () =>{
            atualizarSelecionados(item);
        })
    })

    mobileBotaoFisica.click();
}

document.addEventListener("click", function (e) {
  const img = e.target;
  if (img.closest(".resposta img")) {
    img.classList.toggle("ampliada");
  }
});