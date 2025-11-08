import time
import requests
import json
import os

def gerarImgemRealista(prompt):
    
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
            "image_size": "auto"
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
            return None
        
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
                        print("[ERRO] resultJson está vazio")
                        return None
                    
                    # converte o json em um dicionário python
                    url_dicionario = json.loads(url_json)
                    final_url = url_dicionario['resultUrls'][0]
                    return final_url
                    
                elif state == "waiting" or state == "running":
                    continue
                    
                elif state == "failed":
                    mensagem_state_falha = data.get("failMsg", "erro")
                    print(f"Tarefa falhou: {mensagem_state_falha}")
                    return None
                    
                else:
                    print('Estado não tratado')
                
            else:
                return f'{image_json.get("code")}: erro ao gerar imagem'
        
        return f"EMPO EXPIRADO"
        
    except Exception as e:
        return e