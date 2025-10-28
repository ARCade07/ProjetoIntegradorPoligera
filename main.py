import time
from flask import Flask, request, jsonify 
from flask_cors import CORS
from agente_gemini import resposta_ia

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

    resposta = resposta_ia(prompt)

    # envia a resposta para o front
    return jsonify({
        'message': f"{resposta}"
    })

# rodará o código no modo debug na porta 5000 apenas se for executado o código em si
if __name__ == '__main__':
    app.run(port=5000, debug=True)
