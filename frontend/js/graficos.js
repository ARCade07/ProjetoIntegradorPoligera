const graficoHorarios = document.getElementById('graficoHorarios');
const graficoTipoImagem = document.getElementById('graficoTipoImagem');
const graficoAreas = document.getElementById('graficoAreas');
const graficoIcones = document.getElementById('graficoIcones');
const graficoContinuidade = document.getElementById('graficoContinuidade');

const imgItens = document.querySelectorAll('.itens img');
const nomeItens = Array.from(imgItens).map(img => img.alt);

const dadosIconesExemplo = nomeItens.map(() => Math.floor(Math.random() * 25) + 1);

const numItens = nomeItens.length;
const alturaGrafico = Math.max(numItens * 30 + 100, 400);

const containerGraficoIcones = document.querySelector('.chart-container-icones');
if (containerGraficoIcones) {
    containerGraficoIcones.style.height = `${alturaGrafico}px`;
}

const dadosGraficoHorarios = {
    labels: ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
    data: [12, 19, 3, 5, 2, 3, 4, 8, 15, 22, 20, 18, 16, 19, 23, 21, 20, 17, 14, 10, 9, 8, 10, 11]
};

const numHorarios = dadosGraficoHorarios.labels.length;
const alturaGraficoHorarios = Math.max(numHorarios * 28 + 100, 400);

const containerGraficoHorarios = document.querySelector('.chart-container-bar');
if (containerGraficoHorarios) {
    containerGraficoHorarios.style.height = `${alturaGraficoHorarios}px`;
}

new Chart(graficoHorarios, {
    type: 'bar',
    data: {
        labels: dadosGraficoHorarios.labels,
        datasets: [{
            label: 'Vezes',
            data: dadosGraficoHorarios.data,
            borderWidth: 1
        }]
    },
    options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Acessos'
                }
            },
            y: {
                type: 'category',
                title: {
                    display: true,
                    text: 'Horários'
                },
                ticks: {
                    autoSkip: false
                }
            }
        },
        plugins: {
            legend: {
                position: 'bottom'
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
    options: {
        plugins: {
            legend: {
                position: 'bottom'
            }
        }
    }
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
    options: {
        plugins: {
            legend: {
                position: 'bottom'
            }
        }
    }
});

new Chart(graficoIcones, {
    type: 'bar',
    data: {
        labels: nomeItens,
        datasets: [{
            label: 'Imagens geradas',
            data: dadosIconesExemplo,
            borderWidth: 1
        }]
    },
    options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Quantidade'
                }
            },
            y: {
                type: 'category',
                title: {
                    display: true,
                    text: 'Ícones'
                },
                ticks: {
                    autoSkip: false
                }
            }
        },
        plugins: {
            legend: {
                display: true,
                position: 'bottom'
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
    options: {
        plugins: {
            legend: {
                position: 'bottom'
            }
        }
    }
});