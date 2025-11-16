const canvasHorarios = document.getElementById('graficoHorarios');
const canvasTipoImagem = document.getElementById('graficoTipoImagem');
const canvasAreas = document.getElementById('graficoAreas');
const canvasIcones = document.getElementById('graficoIcones');
const canvasContinuidade = document.getElementById('graficoContinuidade');
const modalEstatisticas = document.getElementById('modalEstatisticas');

let chartHorarios, chartTipoImagem, chartAreas, chartIcones, chartContinuidade;

const imgItens = document.querySelectorAll('.itens img');
const nomeItens = Array.from(imgItens).map(img => img.alt);

const alturaGraficoIcones = Math.max(nomeItens.length * 30 + 100, 400);
const containerGraficoIcones = document.querySelector('.chart-container-icones');
if (containerGraficoIcones) {
    containerGraficoIcones.style.height = `${alturaGraficoIcones}px`;
}

const labelsHorarios = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'];
const numHorarios = labelsHorarios.length;
const alturaGraficoHorarios = Math.max(numHorarios * 28 + 100, 400);
const containerGraficoHorarios = document.querySelector('.chart-container-bar');
if (containerGraficoHorarios) {
    containerGraficoHorarios.style.height = `${alturaGraficoHorarios}px`;
}

function atualizarGraficos() {
    const eventos = JSON.parse(localStorage.getItem('eventosPoligera')) || [];

    const dados = {
        tipoImagem: { 'Técnico': 0, 'Realista': 0 },
        areas: { 'Física': 0, 'Química': 0 },
        icones: {},
        horarios: Array(24).fill(0),
        continuidade: {
            totalGeracoes: eventos.length,
            diasAtivos: new Set(eventos.map(e => new Date(e.data).toDateString())).size
        }
    };
    
    nomeItens.forEach(nome => { dados.icones[nome] = 0; });

    eventos.forEach(e => {
        if (e.tipo === 'Técnico') dados.tipoImagem['Técnico']++;
        if (e.tipo === 'Realista') dados.tipoImagem['Realista']++;
        
        if (e.materia === 'fisica') dados.areas['Física']++;
        if (e.materia === 'quimica') dados.areas['Química']++;
        
        if (e.hora >= 0 && e.hora <= 23) {
            dados.horarios[e.hora]++;
        }
        
        if (e.icones && Array.isArray(e.icones)) {
            e.icones.forEach(iconeNome => {
                if (iconeNome in dados.icones) {
                    dados.icones[iconeNome]++;
                }
            });
        }
    });

    const dataHorarios = {
        labels: labelsHorarios,
        datasets: [{
            label: 'Vezes',
            data: dados.horarios,
            borderWidth: 1
        }]
    };
    if (!chartHorarios) {
        chartHorarios = new Chart(canvasHorarios, {
            type: 'bar',
            data: dataHorarios,
            options: {
                indexAxis: 'y', responsive: true, maintainAspectRatio: false,
                scales: {
                    x: { beginAtZero: true, title: { display: true, text: 'Acessos' } },
                    y: { type: 'category', title: { display: true, text: 'Horários' }, ticks: { autoSkip: false } }
                },
                plugins: { legend: { position: 'bottom' } }
            }
        });
    } else {
        chartHorarios.data = dataHorarios;
        chartHorarios.update();
    }

    const dataTipoImagem = {
        labels: ['Técnico', 'Realista'],
        datasets: [{
            label: 'Imagens geradas',
            data: [dados.tipoImagem['Técnico'], dados.tipoImagem['Realista']],
            borderWidth: 1
        }]
    };
    if (!chartTipoImagem) {
        chartTipoImagem = new Chart(canvasTipoImagem, {
            type: 'pie',
            data: dataTipoImagem,
            options: { plugins: { legend: { position: 'bottom' } } }
        });
    } else {
        chartTipoImagem.data = dataTipoImagem;
        chartTipoImagem.update();
    }

    const dataAreas = {
        labels: ['Física', 'Química'],
        datasets: [{
            label: 'Imagens geradas',
            data: [dados.areas['Física'], dados.areas['Química']],
            borderWidth: 1
        }]
    };
    if (!chartAreas) {
        chartAreas = new Chart(canvasAreas, {
            type: 'pie',
            data: dataAreas,
            options: { plugins: { legend: { position: 'bottom' } } }
        });
    } else {
        chartAreas.data = dataAreas;
        chartAreas.update();
    }

    const dataIcones = {
        labels: nomeItens,
        datasets: [{
            label: 'Imagens geradas',
            data: nomeItens.map(nome => dados.icones[nome]),
            borderWidth: 1
        }]
    };
    if (!chartIcones) {
        chartIcones = new Chart(canvasIcones, {
            type: 'bar',
            data: dataIcones,
            options: {
                indexAxis: 'y', responsive: true, maintainAspectRatio: false,
                scales: {
                    x: { beginAtZero: true, title: { display: true, text: 'Quantidade' } },
                    y: { type: 'category', title: { display: true, text: 'Ícones' }, ticks: { autoSkip: false } }
                },
                plugins: { legend: { display: true, position: 'bottom' } }
            }
        });
    } else {
        chartIcones.data = dataIcones;
        chartIcones.update();
    }

    const dataContinuidade = {
        labels: ['Total de Imagens Geradas', 'Total de Dias Ativos'],
        datasets: [{
            label: 'Estatísticas de Uso (Este Usuário)',
            data: [dados.continuidade.totalGeracoes, dados.continuidade.diasAtivos],
            borderWidth: 1,
            backgroundColor: ['#36A2EB', '#FFCE56']
        }]
    };
    if (chartContinuidade) {
        chartContinuidade.destroy();
    }
    chartContinuidade = new Chart(canvasContinuidade, {
        type: 'bar',
        data: dataContinuidade,
        options: {
            indexAxis: 'x',
            scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } },
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

if (modalEstatisticas) {
    modalEstatisticas.addEventListener('show.bs.modal', () => {
        console.log("Modal de estatísticas aberto. Atualizando gráficos...");
        atualizarGraficos();
    });
} else {
    console.error("Não foi possível encontrar o elemento #modalEstatisticas");
}