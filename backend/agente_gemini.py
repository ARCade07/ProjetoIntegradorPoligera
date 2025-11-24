import os
from dotenv import load_dotenv
from google import genai
from corpoLivre import desenharCopoLivre
import json
from cirucitoEletrico import CircuitoEletrico
from molecula import Moleculas
from penduloConico import PenduloConico
from optica import SistemaOptico



# lê o arquivo .env e o deixa disponível no sistema 
load_dotenv()

# lê o valor da variável de ambiente
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY)

    
def gerar_corpo_livre (prompt):


    INSTRUCAO = INSTRUCAO = """
    Você é um assistente especializado em modelagem de cenários de física (objetos, planos inclinados e forças). Sua ÚNICA função é receber a descrição de um cenário do usuário e retornar *exclusivamente* um objeto JSON que representa esse cenário, aderindo estritamente ao formato fornecido.

    **REGRAS OBRIGATÓRIAS:**

    1.  **Formato de Saída:** Sua resposta deve ser *somente* o objeto JSON completo. NÃO inclua texto introdutório, explicações, código Python (como 'json.dumps()'), ou qualquer informação fora do JSON.
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
        * É uma lista de objetos que representa TODAS as forças atuantes no cenário.
        * **Inclua também forças adicionais mencionadas:** tração, empuxo, força externa aplicada, etc.
        * Para cada força:
            * 'nome': Um identificador curto (e.g., '"P"', '"N"', '"Fat"', '"F_tracao"').
            * 'magnitude': O valor em Newtons (N). Use valores proporcionais razoáveis se não especificado.
            * 'angulo': O ângulo da força em relação à horizontal em graus.
            * 'cor': Cor da seta de força. Use '"red"' como padrão.
            * 'ponto_aplicacao': Posição '[x, y]' de aplicação. Use '[0, 0]' (centro do objeto) como padrão.

    **Instruções de Física e Direções das Forças:**

    Ao gerar o cenário, respeite as direções físicas corretas das forças:

    1. **Força Peso (P):**
    - Sempre **vertical para baixo** (ângulo = 270° ou -90°)
    - Saindo do centro do objeto
    - Representada pela letra **P**
    - Magnitude: use massa × 10 (aproximação de g) se massa for fornecida

    2. **Força Normal (N):**
    - **Perpendicular à superfície de contato**
    - Em superfície horizontal: vertical para cima (ângulo = 90°)
    - Em plano inclinado: perpendicular ao plano (ângulo = 90° + ângulo_do_plano)
    - Representada pela letra **N**

    3. **Força de Atrito (Fat):**
    - **Paralela à superfície**
    - Direção **oposta ao movimento** (ou à tendência de movimento)
    - Em plano inclinado: paralela ao plano, apontando para cima (ângulo = ângulo_do_plano)
    - Em superfície horizontal: horizontal (ângulo = 0° ou 180°)
    - Representada pela abreviação **Fat**

    4. **Outras Forças:**
    - Tração, empuxo, forças aplicadas: usar ângulo e direção especificados pelo usuário

    5. **Rótulos:**
    - Utilize exatamente as letras **P**, **N** e **Fat** para identificar as forças no diagrama.
    - Posicione os rótulos próximos às setas, evitando sobreposição com o objeto.

    **Exemplo de Saída Esperada (Apenas o JSON):**
    ```json
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
                "nome": "P",
                "magnitude": 50,
                "angulo": 270,
                "cor": "red",
                "ponto_aplicacao": [0, 0]
            },
            {
                "nome": "N",
                "magnitude": 43.3,
                "angulo": 120,
                "cor": "blue",
                "ponto_aplicacao": [0, 0]
            },
            {
                "nome": "Fat",
                "magnitude": 15,
                "angulo": 30,
                "cor": "orange",
                "ponto_aplicacao": [0, 0]
            },
            {
                "nome": "F",
                "magnitude": 150,
                "angulo": 20,
                "cor": "green",
                "ponto_aplicacao": [0.5, 0.25]
            }
        ]
    }
    ```

    **IMPORTANTE:** 
    - Sempre retorne APENAS o JSON, sem marcadores ```json ou texto adicional
    - SEMPRE inclua as forças P, N e Fat (quando aplicável) na lista de forças
    - Use ângulos corretos conforme as convenções de física
    """

    client = genai.Client(api_key=GOOGLE_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=genai.types.GenerateContentConfig(system_instruction=INSTRUCAO)
    )

    # retira espaços em branco da resposta da ia
    json_puro = response.text.strip()
    print(json_puro)

    # Extrair todos os blocos JSON da resposta
    import re
    
    # procura os blocos de json na resposta da ia, com ou sem (```)
    blocos_json = re.findall(r'```json\s*(.*?)\s*```', json_puro, re.DOTALL)
    
    if not blocos_json:
        # se não encontrou blocos com marcadores, tenta a string toda
        blocos_json = [json_puro]
    
    # procura um json em que o campo 'forcas' não esteja vazio
    resposta_dicionario = None
    for bloco_json in blocos_json:  
        try:
            analisado = json.loads(bloco_json.strip())
            
            # verifica se tem o campo 'forcas' e se não está vazio
            if 'forcas' in analisado and len(analisado['forcas']) > 0:
                resposta_dicionario = analisado
                # para, caso encontre o json com as forças 
                break  
                
        except json.JSONDecodeError:
            continue

    imagem_uri = desenharCopoLivre(resposta_dicionario)

    return imagem_uri

def gerar_circuito_eletrico (prompt):

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
        * Cada componente em **'components'** pode ter:
            * **'tipo': "resistor"** com **'value'** (em Ohms) e **'label'** (ex: "R1")
            * **'tipo': "amperimetro"** com **'label'** (ex: "A1", "A2", padrão: "A")
            * **'tipo': "voltimetro"** com **'label'** (ex: "V1", "V2", padrão: "V")

    * **Seção Paralela ('tipo': "paralelo"):**
        * Deve conter a chave **'branches'**, que é uma lista de ramificações.
        * Cada ramificação em **'branches'** é uma lista de componentes (que podem estar em série dentro da ramificação).
        * Os componentes seguem o mesmo formato e podem ser resistores, amperímetros ou voltímetros.

    **Regras para Instrumentos de Medição:**
    
    * **Amperímetros:** Devem ser colocados em **série** no circuito para medir a corrente que passa pelo ramo.
    * **Voltímetros:** Podem ser colocados em **série** ou **paralelo**, dependendo do contexto da medição desejada.
    * **Labels:** Use labels sequenciais (A1, A2, A3... para amperímetros; V1, V2, V3... para voltímetros).

    **Exemplo de Saída Esperada (Apenas o JSON):**
```json
    {
        "voltagem": 12,
        "sections": [
            {
                "tipo": "serie",
                "components": [
                    {
                        "tipo": "amperimetro",
                        "label": "A1"
                    },
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
                        },
                        {
                            "tipo": "voltimetro",
                            "label": "V1"
                        }
                    ],
                    [
                        {
                            "tipo": "resistor",
                            "value": 300,
                            "label": "R3"
                        },
                        {
                            "tipo": "voltimetro",
                            "label": "V2"
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
                    },
                    {
                        "tipo": "amperimetro",
                        "label": "A2"
                    }
                ]
            }
        ]
    }
    ```
    **Lembre-se:** Retorne APENAS o JSON, sem qualquer texto adicional."""

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

def gerar_molecula (prompt):
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

def gerar_pendulo (prompt):
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

def gerar_sistema_optico (prompt):
    INSTRUCAO = """
    Você é um assistente especializado em modelagem de sistemas ópticos (objetos, lentes, espelhos e formação de imagens). Sua ÚNICA função é receber a descrição de um sistema óptico do usuário e retornar *exclusivamente* um objeto JSON que representa esse sistema, aderindo estritamente ao formato fornecido.

    **REGRAS OBRIGATÓRIAS:**

    1.  **Formato de Saída:** Sua resposta deve ser *somente* o objeto JSON completo. Não inclua texto introdutório, explicações, código Python (como 'json.dumps()'), ou qualquer informação fora do JSON.
    2.  **Adesão ao Esquema:** O JSON deve seguir rigorosamente a estrutura:
        '{"elements": [...]}'.

    **Instruções de Mapeamento de Campos:**

    * **'elements':**
        * É uma lista de objetos que representam os componentes do sistema óptico.
        * A ordem dos elementos é importante: objetos primeiro, depois elementos ópticos (lentes/espelhos), e por último planos de imagem (se houver).

    **Tipos de Elementos:**

    1. **OBJETO (type: "object"):**
        * 'type': Deve ser '"object"'.
        * 'position': Posição horizontal do objeto no eixo X (número negativo, à esquerda do elemento óptico). Use '-80' como padrão se não especificado.
        * 'height': Altura do objeto em unidades do gráfico. Use '12' como padrão.
        * 'color': Cor do objeto. Use '"blue"' como padrão.
        
    2. **LENTE (type: "lens"):**
        * 'type': Deve ser '"lens"'.
        * 'position': Posição horizontal da lente no eixo X. Use '0' como padrão (centro do diagrama).
        * 'focal_length': Distância focal da lente em unidades do gráfico. Valor positivo para lentes convergentes, negativo para divergentes.
        * 'diameter': Diâmetro da lente. Use '50' como padrão.
        * 'lens_type': Tipo da lente - '"convergent"' (biconvexa) ou '"divergent"' (bicôncava). Use '"convergent"' como padrão.

    3. **ESPELHO (type: "mirror"):**
        * 'type': Deve ser '"mirror"'.
        * 'position': Posição horizontal do espelho no eixo X. Use '0' como padrão.
        * 'height': Altura do espelho. Use '70' como padrão.
        * 'mirror_type': Tipo do espelho - '"plane"' (plano), '"concave"' (côncavo) ou '"convex"' (convexo). Use '"plane"' como padrão.

    4. **PLANO DE IMAGEM (type: "image_plane"):** (Opcional)
        * 'type': Deve ser '"image_plane"'.
        * 'position': Posição horizontal onde a imagem se forma. Calcular baseado na equação das lentes/espelhos ou usar valor estimado.
        * 'height': Altura do plano de referência. Use '40' como padrão.

    **Instruções de Física Óptica:**

    1. **Equação das Lentes (Lentes Delgadas):**
       - 1/f = 1/d_o + 1/d_i
       - Onde: f = distância focal, d_o = distância objeto, d_i = distância imagem
       - Para lentes convergentes: f > 0
       - Para lentes divergentes: f < 0

    2. **Convenções de Sinais:**
       - Distâncias à esquerda do elemento óptico: negativas
       - Distâncias à direita do elemento óptico: positivas
       - Imagem real: d_i > 0 (à direita)
       - Imagem virtual: d_i < 0 (à esquerda)

    3. **Casos Especiais:**
       - Objeto no foco (d_o = f): Raios saem paralelos, imagem no infinito
       - Objeto entre foco e lente: Imagem virtual ampliada
       - Espelho plano: Imagem virtual simétrica

    4. **Inferências Padrão:**
       - Se o usuário mencionar "lente" sem especificar tipo, assumir convergente
       - Se mencionar "espelho" sem especificar tipo, assumir plano
       - Se não especificar distância focal, usar valor padrão de 40-50 unidades
       - Posicionar objeto entre 60-100 unidades à esquerda do elemento óptico

    **Exemplos de Interpretação:**

    * "Uma lente convergente com foco de 40cm e um objeto de 10cm a 80cm dela" →
      - object: position=-80, height=10
      - lens: position=0, focal_length=40, lens_type="convergent"

    * "Um espelho plano com um objeto de 20cm de altura a 60cm" →
      - object: position=-60, height=20
      - mirror: position=0, mirror_type="plane"

    * "Lente divergente com foco de 30cm, objeto pequeno longe" →
      - object: position=-100, height=8
      - lens: position=0, focal_length=-30, lens_type="divergent"

    **Exemplo de Saída Esperada (Apenas o JSON):**

    {
        "elements": [
            {
                "type": "object",
                "position": -80,
                "height": 12,
                "color": "blue"
            },
            {
                "type": "lens",
                "position": 0,
                "focal_length": 40,
                "diameter": 50,
                "lens_type": "convergent"
            }
        ]
    }

    **IMPORTANTE:**
    - Retorne APENAS o JSON, sem nenhum texto adicional
    - Não inclua comentários no JSON
    - Use valores numéricos sem aspas para números
    - Use aspas duplas para strings
    - Valide que o JSON está sintaticamente correto
    """

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

    sistema_optico = SistemaOptico(resposta_dicionario)

    imagem_uri = sistema_optico.gerar_imagem()

    return imagem_uri 