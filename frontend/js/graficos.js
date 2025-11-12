const graficoHorarios = document.getElementById('graficoHorarios');
const graficoTipoImagem = document.getElementById('graficoTipoImagem');
const graficoAreas = document.getElementById('graficoAreas');
const graficoIcones = document.getElementById('graficoIcones');
const graficoContinuidade = document.getElementById('graficoContinuidade');

const imgItens = document.querySelectorAll('.itens img');
const nomeItens = Array.from(imgItens).map(img => img.alt);

new Chart(graficoHorarios, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

new Chart(graficoTipoImagem, {
    type: 'pie',
    data: {
        labels: ['Técnico', 'Realista'],
        datasets: [{
            label: 'Imagens geradas',
            data: [20, 5],
            borderWidth: 1
        }]
    },
});

new Chart(graficoAreas, {
    type: 'pie',
    data: {
        labels: ['Física', 'Química'],
        datasets: [{
            label: 'Imagens geradas',
            data: [22, 3],
            borderWidth: 1
        }]
    },
});

new Chart(graficoIcones, {
    type: 'scatter',
    data: {
        labels: nomeItens,
        datasets: [{
            label: 'Imagens geradas',
            data: [20, 5],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            x: {
                type: 'category',
                offset: true,
                title: {
                    display: true,
                    text: 'Ícones'
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Quantidade'
                }
            }
        },
        plugins: {
            legend: {
                display: true
            }
        }
    }
});

new Chart(graficoContinuidade, {
    type: 'pie',
    data: {
        labels: ['Nenhuma vez', '1-2 vezes', '3-5 vezes', '6-8 vezes', '9-10 vezes', '+10 vezes'],
        datasets: [{
            label: 'Usuários',
            data: [2, 20, 10, 13, 5, 3],
            borderWidth: 1
        }]
    },
});