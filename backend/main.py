import time
import requests
from flask import Flask, request, jsonify 
from flask_cors import CORS
from agente_gemini import gerar_corpo_livre, gerar_circuito_eletrico, gerar_molecula, gerar_pendulo, gerar_sistema_optico
# from agente_gemini import gerarCorpoLivre, gerarCircuitoEletrico, gerarMolecula, gerarPendulo
from imagemRealista import gerar_imgem_realista

# inicialização do Flask
app = Flask(__name__)

# habilita o CORS para autorizar a conexão entre front e back 
CORS(app, supports_credentials=True)

def salvar_no_node(prompt, imagem_base64, user_id):
    url = "http://localhost:3000/historico/salvar"

    payload = {
        "userId": user_id,
        "prompt": prompt,
        "imageBase64": imagem_base64
    }

    return requests.post(url, json=payload)
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
    itens_selecionados = dados.get('elementos', [])
    tipo_imagem_selecionada = dados.get('tipo')
    print(tipo_imagem_selecionada)

    if itens_selecionados:
        itens_selecionados_conteudo = ", ".join(itens_selecionados)
        prompt_final = f"{itens_selecionados_conteudo}.{prompt}"
    else:
        prompt_final = prompt

    try:
        if tipo_imagem_selecionada == "Realista":
            resposta = gerar_imgem_realista(prompt_final)
        elif tipo_imagem_selecionada == "Técnico":
            if materia == 'fisica':
                if area == 'mecanica':
                    for i in itens_selecionados:
                        if i == 'pendulo':
                            resposta = gerar_pendulo(prompt_final)
                        else:
                            resposta = gerar_corpo_livre(prompt_final)
                elif area == 'eletrica':
                    resposta = gerar_circuito_eletrico(prompt_final)
                elif area == 'optica':
                    resposta = gerar_sistema_optico(prompt_final)
            elif materia == 'quimica':
                resposta = gerar_molecula(prompt_final)

        # verifica se a resposta for none, se é uma mensagem de erro ou se não começa com data:image
        if resposta is None or (isinstance(resposta, str) and not resposta.startswith('data:image')):
            return jsonify({
                'erro': True,
                'mensagem': resposta if resposta else 'Erro ao gerar imagem'
            }), 400

        # envia a resposta para o front
        user_id = dados.get("userId")
        salvar_no_node(prompt, resposta, user_id)
        return jsonify({
            'resposta': resposta
        })
    except Exception as e:
        print(f'Erro no processamento: {str(e)}')
        return jsonify({
            'erro': True,
            'mensagem': f'Erro inesperado: {str(e)}'
        }), 500



# rodará o código no modo debug na porta 5000 apenas se for executado o código em si
if __name__ == '__main__':
    app.run(port=5000, debug=True)