import os
from dotenv import load_dotenv
from google import genai
from corpoLivre import desenharCopoLivre
import json
from cirucitoEletrico import CircuitoEletrico
from molecula import Moleculas
from penduloConico import PenduloConico

# lê o arquivo .env e o deixa disponível no sistema 
load_dotenv()

# lê o valor da variável de ambiente
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY)

    
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

def gerarMolecula (prompt):
    INSTRUCAO = """
    Você é um assistente especializado em modelagem de estruturas moleculares. Sua ÚNICA função é receber a descrição de uma molécula ou estrutura atômica do usuário e retornar *exclusivamente* um objeto JSON que representa essa estrutura, aderindo estritamente ao formato de coordenadas atômicas e ligações fornecido.

    **REGRAS OBRIGATÓRIAS:**

    1.  **Formato de Saída:** Sua resposta deve ser *somente* o objeto JSON completo. Não inclua texto introdutório, explicações, código Python (como 'json.dumps()'), ou qualquer outra informação.
    2.  **Adesão ao Esquema:** O JSON deve seguir rigorosamente a estrutura:
        '{"atomos": [...], "ligações": [...]}'.

    **Instruções de Mapeamento de Campos:**

    * **'atomos':** Uma lista de objetos representando cada átomo na estrutura. A ordem é importante, pois define os índices para as ligações ('ligações').
        * Cada átomo deve ter:
            * **'elemento':** O símbolo químico do elemento (ex: "C", "H", "O").
            * **'x':** Coordenada x do átomo (número float).
            * **'y':** Coordenada y do átomo (número float).
        * **Posicionamento:** As coordenadas (x, y) devem ser inferidas para visualizar a estrutura quimicamente correta. Use distâncias e ângulos de ligação razoáveis para a geometria molecular esperada.

    * **'ligações':** Uma lista de listas representando as ligações entre os átomos.
        * Cada ligação é definida como uma lista de três valores: **[indice_atomo_1, indice_atomo_2, ordem_da_ligacao]**.
            * **indice_atomo_1/2:** Índices de base zero (0, 1, 2, ...) correspondentes à posição do átomo na lista **'atoms'**.
            * **ordem_da_ligacao:** 1 para ligação simples, 2 para dupla e 3 para tripla.

    **Exemplo de Saída Esperada (Apenas o JSON):**

    ```json
    {
    "atomos": [
        {"elemento": "H", "x": 0.5, "y": 1.5},
        {"elemento": "Cl", "x": 2.0, "y": 1.5}
    ],
    "ligações": [[0, 1, 1]]
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

    molecula = Moleculas()
    imagem_uri = molecula.desenharMolecula(resposta_dicionario)


    print(resposta_dicionario)

    return imagem_uri   

def gerarPendulo (prompt):
    INSTRUCAO = """
    Você é um assistente especializado em gerar configurações de cenários de física, especificamente para sistemas como o pêndulo cônico. Sua ÚNICA função é receber a descrição de um cenário do usuário e retornar *exclusivamente* um objeto JSON que representa essa configuração, aderindo estritamente ao formato fornecido.

    **REGRAS OBRIGATÓRIAS:**

    1.  **Formato de Saída:** Sua resposta deve ser *somente* o objeto JSON completo. Não inclua texto introdutório, explicações, código Python (como 'json.dumps()'), ou qualquer outra informação.
    2.  **Adesão ao Esquema:** O JSON deve seguir rigorosamente a estrutura:
        '{"comprimento": valor, "angulo_conico": valor, ...}'.

    **Instruções de Mapeamento de Campos (Todos os valores devem ser numéricos, exceto as cores):**

    * **'comprimento':** O comprimento do fio ou haste (em unidades de comprimento, ex: metros). Use **3.0** como padrão se omitido.
    * **'angulo_conico':** O ângulo de abertura do cone (o ângulo do fio em relação à vertical) em graus. Use **30** como padrão.
    * **'raio_massa':** O raio da massa ou esfera do pêndulo. Use **0.3** como padrão.
    * **'raio_posicoes':** O raio da trajetória circular (a projeção horizontal). Use **0.15** como padrão.
    * **'cor_massa':** A cor da massa. Deve ser uma string (ex: "blue" ou um código hexadecimal). Use **"#4169E1"** (azul) como padrão.
    * **'cor_fio':** A cor do fio/haste. Use **"black"** como padrão.
    * **'mostrar_seta_gravidade':** Um valor booleano (**True** ou **False**) que indica se a seta de força da gravidade deve ser exibida. Use **True** como padrão.

    **Exemplo de Saída Esperada (Apenas o JSON):**

    json
    {
        "comprimento": 5.0,
        "angulo_conico": 45,
        "raio_massa": 0.5,
        "raio_posicoes": 0.25,
        "cor_massa": "red",
        "cor_fio": "gray",
        "mostrar_seta_gravidade": false
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

    pendulo = PenduloConico(resposta_dicionario)

    imagem_uri = pendulo.gerar_imagem()

    return imagem_uri 