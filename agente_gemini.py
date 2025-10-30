import os
import types
from dotenv import load_dotenv
from google import genai
from corpoLivre import desenharCopoLivre
import json
from cirucitoEletrico import CircuitoEletrico

# lê o arquivo .env e o deixa disponível no sistema 
load_dotenv()

# lê o valor da variável de ambiente
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY)

def resposta_ia(prompt):

    # especificação do modelo a ser utilizado
    modelo = "gemini-2.5-flash"

    # criação do chat
    chat = client.chats.create(model= modelo)
    resposta = chat.send_message(prompt)

    return resposta.text

def criacaoImagemRealista(prompt):

    MELHORADOR_PROMPT = """
    Você é um motor de geração de imagens de nível especialista.
    Sua única tarefa é receber o prompt do usuário e gerar uma imagem, 
    seguindo duas diretrizes principais: MELHORIA e SEGURANÇA.

    ## 1. DIRETRIZ DE MELHORIA (O que fazer)

    Quando o prompt do usuário for seguro, sua tarefa é melhorá-lo 
    secretamente para criar uma arte fotorrealista e impressionante.

    * **Regras de Melhoria:**
        * Adicione detalhes cinematográficos: iluminação (ex: "luz de borda", "hora dourada"), ângulo da câmera (ex: "plano geral", "close-up extremo").
        * Especifique texturas e materiais: (ex: "couro áspero", "metal cromado reflexivo", "pele escamosa detalhada").
        * Defina o ambiente: (ex: "rua de paralelepípedos molhada", "céu de tempestade", "interior de biblioteca empoeirada").
        * Sempre adicione termos de alta qualidade: "fotorrealista, 8K, alta definição, nitidez, cinematográfico".

    * **Exemplo de Melhoria:**
        * Usuário envia: "um tigre"
        * Você melhora internamente para: "Um close-up fotorrealista de um tigre de bengala, pelagem laranja e preta nítida, olhos amarelos penetrantes, bigodes detalhados, luz do sol filtrada pela selva, 8K, cinematográfico."

    ## 2. DIRETRIZ DE SEGURANÇA (O que NUNCA fazer)

    Você **NÃO DEVE** gerar imagens que se enquadrem nestas categorias:
    * **Conteúdo Explícito:** Imagens pornográficas, nudez explícita ou sexualmente sugestivas.
    * **Violência Gráfica:** Imagens de sangue, gore, ferimentos graves, automutilação ou violência extrema.
    * **Discurso de Ódio:** Conteúdo que promova ódio, discriminação ou assédio contra qualquer grupo com base em raça, etnia, religião, gênero, orientação sexual ou deficiência.
    * **Violação de Direitos Autorais:** Tentativas diretas de replicar personagens ou logotipos protegidos por direitos autorais (ex: "Mickey Mouse da Disney").
    * **Desinformação e Deepfakes:** Criação de imagens de figuras públicas em contextos enganosos, falsos ou difamatórios.

    * **Ação de Segurança:**
        * Se o prompt do usuário violar clara e diretamente qualquer uma dessas regras, você deve **RECUSAR** a geração.
        * (A API que você está usando provavelmente retornará um erro de 'segurança' ou 'conteúdo bloqueado' quando você fizer isso).

    NUNCA converse com o usuário. NUNCA responda em texto (a menos que seja uma mensagem de erro da plataforma).
    Sua função é: receber prompt -> aplicar diretrizes -> gerar imagem (ou falhar por segurança).
    """
    
    modelo = "gemini-2.5-flash-image"

    # instruções que serão passadas de como a imagem deverá ser criada
    chat_config = types.GenerateContentConfig(system_instruction=MELHORADOR_PROMPT)

    chat = client.chats.create(model=modelo, config=chat_config)
    resposta = chat.send_message(prompt)

    # hasattr verifica se um objeto possui determinado atributo
    if hasattr(resposta, 'image_url'):
        return resposta.image_url
    elif hasattr(resposta, 'data') and resposta.data:
        return resposta.data[0].url
    
def gerarCorpoLivre (prompt):


    INSTRUCAO = """
    Você é um assistente especializado em modelagem de cenários de física (objetos, planos inclinados e forças). Sua ÚNICA função é receber a descrição de um cenário do usuário e retornar *exclusivamente* um objeto JSON que representa esse cenário, aderindo estritamente ao formato fornecido.

    **REGRAS OBRIGATÓRIAS:**

    1.  **Formato de Saída:** Sua resposta deve ser *somente* o objeto JSON completo. Não inclua texto introdutório, explicações, código Python (como 'json.dumps()'), ou qualquer informação fora do JSON.
    2.  **Adesão ao Esquema:** O JSON deve seguir rigorosamente a estrutura:
        '{"objeto": {...}, "plano_inclinado": {...}, "forcas": [...]}'.

    **Instruções de Mapeamento de Campos:**

    * **'objeto':**
        * 'tipo': Deve ser '"retangulo"' ou '"circulo"'. Inferir da descrição do usuário (ex: "bloco" ou "caixa" implica '"retangulo"'; "bola" ou "esfera" implica '"circulo"').
        * 'tamanho':
            * Se 'tipo' for '"retangulo"', use uma lista '[largura, altura]' (em unidades consistentes, ex: metros).
            * Se 'tipo' for '"circulo"', use o valor do raio (em unidades consistentes).
        * 'cor': Cor do objeto. Use '"blue"' como padrão se não for especificado.
        * 'massa': A massa em kg. Se não for especificada, este campo é opcional, mas se for incluído, deve ser um número.

    * **'plano_inclinado':**
        * 'ativo': 'true' se o usuário descrever uma rampa, superfície angulada, ou plano inclinado; caso contrário, 'false'.
        * 'angulo': O ângulo de inclinação em graus (0 a 90). Use '30' como padrão se 'ativo' for 'true' e o ângulo for omitido. Use '0' se 'ativo' for 'false'.
        * 'cor': Cor do plano. Use '"gray"' como padrão.

    * **'forcas':**
        * É uma lista de objetos. Inclua apenas forças ativas mencionadas (Ex: tração, empuxo, atrito, força externa). **Não inclua** Peso e Normal nesta lista, a menos que o usuário explicitamente peça para representá-las.
        * Para cada força:
            * 'nome': Um identificador curto (e.g., '"F_tracao"', '"Atrito"').
            * 'magnitude': O valor em Newtons (N).
            * 'angulo': O ângulo da força em relação à horizontal em graus.
            * 'cor': Cor da seta de força. Use '"red"' como padrão.
            * 'ponto_aplicacao': Posição '[x, y]' de aplicação. Use '[0, 0]' (centro do objeto) se não for especificado. Se for um objeto circular, 'y' deve ser 0.

    **Exemplo de Saída Esperada (Apenas o JSON):**

    json
    {
        "objeto": {
            "tipo": "retangulo",
            "tamanho": [1.0, 0.5],
            "cor": "blue",
            "massa": 5.0
        },
        "plano_inclinado": {
            "ativo": true,
            "angulo": 30,
            "cor": "gray"
        },
        "forcas": [
            {
                "nome": "F_Puxar",
                "magnitude": 150,
                "angulo": 20,
                "cor": "red",
                "ponto_aplicacao": [0.5, 0.25]
            }
        ]
    } """

    client = genai.Client(api_key=GOOGLE_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=genai.types.GenerateContentConfig(system_instruction=INSTRUCAO)
    )

    # retira espaços em branco da resposta da ia
    json_puro = response.text.strip()

    # remove as crases e a palavra json caso elas estejam no começo da resposta
    if json_puro.startswith("```"):
        json_puro = json_puro.strip("`")
        json_puro = json_puro.replace("json", "", 1).strip()

    # tenta converter o json para dicionário
    try:
        resposta_dicionario = json.loads(json_puro)
    except json.JSONDecodeError:
        print("A respota gerada não é um json válido!")
        print(json_puro)
        return None

    imagem_uri = desenharCopoLivre(resposta_dicionario)

    return imagem_uri

def gerarCircuitoEletrico (prompt):

    INSTRUCAO = """
    Você é um assistente especializado em modelagem de circuitos elétricos (resistivos). Sua ÚNICA função é receber a descrição de um circuito do usuário e retornar *exclusivamente* um objeto JSON que representa esse circuito, aderindo estritamente ao formato de estrutura de lista de seções fornecido, utilizando chaves em português.

    **REGRAS OBRIGATÓRIAS:**

    1.  **Formato de Saída:** Sua resposta deve ser *somente* o objeto JSON completo. Não inclua texto introdutório, explicações, código Python (como 'json.dumps()'), ou qualquer outra informação.
    2.  **Adesão ao Esquema:** O JSON deve seguir rigorosamente a estrutura:
        '{"voltagem": valor, "sections": [...]}'.

    **Instruções de Mapeamento de Campos:**

    * **'voltagem':** Valor numérico da tensão da fonte de alimentação em Volts (V). Use **12** como padrão se não for especificado.
    * **'sections':** Uma lista de seções que compõem o circuito principal.
        * Cada seção deve ter um **'tipo'** que é **"serie"** ou **"paralelo"**.

    * **Seção de Série ('tipo': "serie"):**
        * Deve conter a chave **'components'**, que é uma lista de componentes em série.
        * Cada componente em **'components'** deve ter **'tipo': "resistor"** (padrão), **'value'** (em Ohms) e **'label'** (ex: "R1").

    * **Seção Paralela ('tipo': "paralelo"):**
        * Deve conter a chave **'branches'**, que é uma lista de ramificações.
        * Cada ramificação em **'branches'** é uma lista de componentes (que podem estar em série dentro da ramificação).
        * Os componentes seguem o mesmo formato: **'tipo': "resistor"**, **'value'**, e **'label'**.

    **Exemplo de Saída Esperada (Apenas o JSON):**

    ```json
    {
        "voltagem": 12,
        "sections": [
            {
                "tipo": "serie",
                "components": [
                    {
                        "tipo": "resistor",
                        "value": 100,
                        "label": "R1"
                    }
                ]
            },
            {
                "tipo": "paralelo",
                "branches": [
                    [
                        {
                            "tipo": "resistor",
                            "value": 200,
                            "label": "R2"
                        }
                    ],
                    [
                        {
                            "tipo": "resistor",
                            "value": 300,
                            "label": "R3"
                        }
                    ],
                    [
                        {
                            "tipo": "resistor",
                            "value": 400,
                            "label": "R4"
                        }
                    ]
                ]
            },
            {
                "tipo": "serie",
                "components": [
                    {
                        "tipo": "resistor",
                        "value": 50,
                        "label": "R5"
                    }
                ]
            }
        ]
    }"""

    client = genai.Client(api_key=GOOGLE_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=genai.types.GenerateContentConfig(system_instruction=INSTRUCAO)
    )

    # retira espaços em branco da resposta da ia
    json_puro = response.text.strip()

    # remove as crases e a palavra json caso elas estejam no começo da resposta
    if json_puro.startswith("```"):
        json_puro = json_puro.strip("`")
        json_puro = json_puro.replace("json", "", 1).strip()

    # tenta converter o json para dicionário
    try:
        resposta_dicionario = json.loads(json_puro)
    except json.JSONDecodeError:
        print("A respota gerada não é um json válido!")
        print(json_puro)
        return None
    
    circuito_eletrico = CircuitoEletrico(resposta_dicionario)

    imagem_uri = circuito_eletrico.gerarCircuito()

    return imagem_uri    