import time
from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore

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

    # envia a resposta para o front
    return jsonify({
        'message': f"Seu prompt foi {prompt}"
    })

# rodará o código no modo debug na porta 5000 apenas se for executado o código em si
if __name__ == '__main__':
    app.run(port=5000, debug=True)
