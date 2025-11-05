import time
from flask import Flask, request, jsonify 
from flask_cors import CORS
from agente_gemini import gerarCorpoLivre, gerarCircuitoEletrico, gerarMolecula, gerarPendulo

# inicialização do Flask
app = Flask(__name__)

# habilita o CORS para autorizar a conexão entre front e back 
CORS(app)

# criação da rota para o endpoint '/chat'
@app.route('/chat', methods=['POST'])

# função que recebe o pedido do usuário e retorna a resposta da IA
def processamentoResposta():
    # transforma o json recebido em um dicionário que o python consiga entender
    dados = request.json
    # pega os valores associados a chave 'prompt' dicionário
    prompt = dados.get('prompt')

    # pega os valores associados a chave 'materia' e 'area' do dicionario
    materia = dados.get('materia')
    area = dados.get('area')
    itens_selecionados = dados.get('elementos')

    itens_selecionados_conteudo = ", ".join(itens_selecionados)
    prompt_final = f"{itens_selecionados_conteudo}.{prompt}"

    if materia == 'fisica':
        if area == 'mecanica':
            resposta = gerarCorpoLivre(prompt_final)
        elif area == 'eletrica':
            resposta = gerarCircuitoEletrico(prompt_final)
        elif area == 'optica':
            print('Área indisponível para a geração de imagens')
    elif materia == 'quimica':
        resposta = gerarMolecula(prompt_final)

    # envia a resposta para o front
    return jsonify({
        'resposta': resposta
    })

# rodará o código no modo debug na porta 5000 apenas se for executado o código em si
if __name__ == '__main__':
    app.run(port=5000, debug=True)
