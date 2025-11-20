import time
import requests
import json
import os
import base64

def gerar_imgem_realista(prompt):
    
    KIE_API_KEY = os.getenv("KIE_API_KEY")

    # primeiro é necessario fazer uma requisão post para a API, que responderá (no formato json) se recebeu a requisição e o taskId
    URL = "https://api.kie.ai/api/v1/jobs/createTask"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {KIE_API_KEY}"
    }

    payload = {
        "model": "google/nano-banana",
        "input": {
            "prompt": prompt,
            "output_format": "jpeg",
            "image_size": "16:9"
        }
    }

    try:
        response = requests.post(URL, headers=headers, data=json.dumps(payload), timeout=10)
        
        response.raise_for_status()
        requisicao_json = response.json()
        
        # pegar o taskId
        if requisicao_json.get("code") == 200:
            task_id = requisicao_json["data"].get("taskId")
        else:
            print(f'ERRO: {requisicao_json.get("message")}')
            return requisicao_json.get("message")
        
        # utiliando o taskId é necessario fazer consultas sobre o status da tarefa
        # esse processo rebe o nome de polling
        URL_QUERY = "https://api.kie.ai/api/v1/jobs/recordInfo"
        params = {"taskId": task_id}
        headers_query = {"Authorization": f"Bearer {KIE_API_KEY}"}

        contador = 1
        # faz 30 requisições com delay até que a imagem esteja pronta
        while contador < 30:
            time.sleep(2)
            
            response= requests.get(URL_QUERY, headers=headers_query, params=params, timeout=10)
            
            response.raise_for_status()
            image_json = response.json()

            if image_json.get("code") == 200:
                data = image_json["data"]
                state = data.get("state")
                
                # checa se a geração da imagem foi concluida com sucesso
                if state == "success":
                    url_json = data.get("resultJson", "")
                    
                    if not url_json:
                        print("resultJson vazio")
                        return "resultJson vazio"
                    
                    # converte o json em um dicionário python
                    url_dicionario = json.loads(url_json)
                    url = url_dicionario['resultUrls'][0]

                    imagem_baixada = requests.get(url, timeout=30)
                    imagem_baixada.raise_for_status

                    img_base64 = base64.b64encode(imagem_baixada.content).decode('utf-8')
                    uri = f"data:image/png;base64,{img_base64}"
                    print("Imagem convertida para base64")

                    return uri
                    
                elif state == "waiting" or state == "running":
                    contador += 1
                    continue
                    
                elif state == "failed":
                    mensagem_state_falha = data.get("failMsg", "erro")
                    print(f"Tarefa falhou: {mensagem_state_falha}")
                    return mensagem_state_falha
                    
                else:
                    erro_msg = f'Estado não tratado: {state}'
                    print(erro_msg)
                    contador += 1
                    continue
                
            else:
                erro_msg = f'Código {image_json.get("code")}: erro ao consultar status'
                print(erro_msg)
                return erro_msg
        
        return f"TEMPO EXPIRADO"
        
    except requests.exceptions.RequestException as e:
        erro_msg = f"Erro de requisição: {str(e)}"
        print(erro_msg)
        return erro_msg
    except Exception as e:
        erro_msg = f"Erro inesperado: {str(e)}"
        print(erro_msg)
        return erro_msg