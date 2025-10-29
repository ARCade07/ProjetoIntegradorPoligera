import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import io
import base64

# o parâmetro config refere-se ao json da imagem
def desenharCopoLivre(json):
    # criação do espaço da figura (fig) e do eixo (ax)
    fig, ax = plt.subplots(figsize=(10, 6))

    # limites eixo x
    ax.set_xlim(-5, 5)
    # limites eixo y
    ax.set_ylim(-5, 5)
    # garante que uma unidade no eixo x tenha as mesmas dimensões que uma unidade no eixo y
    ax.set_aspect('equal')

    # Remover eixos, grade e bordas
    ax.axis('off')

    # configurações do objeto
    # 'config' é o json
    # 'get' pega as informações dentro de um json, método nativo de dicionários python
    # as chaves vazias são o valor padrão, caso a chave 'objeto' não seja encontrada no json em questão
    objeto = json.get('objeto', {})

    # Desenhar plano inclinado se especificado
    plano = json.get('plano_inclinado', {})
    # verifica se a chave 'ativo' é true ou false (se o plano é ou não inclinado)
    if plano.get('ativo', False):
        # pega a angulação do plano
        angulo_plano = plano.get('angulo', 30)
        # cor do plano
        cor_plano = 'gray'

        # pontos plano inclinado
        comprimento_plano = 8
        # converte o angulo para radianos utilizando o numpy
        angulo_rad = np.radians(angulo_plano)

        # coordenadas dos vértices do triângulo, que nesse caso será desenhado como um quadrilatero deslocado, pra facilitar o uso de patches.Polygon
        x_plano = [-4, 4, 4, -4]
        # utilização da função seno para determinar a altura do topo do quadrilátero
        y_plano = [-3, -3 + comprimento_plano * np.sin(angulo_rad), -3, -3]

        # cria um objeto Polygon, a partir das coordenadas fornecidas
        plano_desenho = patches.Polygon(list(zip(x_plano, y_plano)),
                                     facecolor=cor_plano, edgecolor='black',
                                     linewidth=2, alpha=0.3)
        # adiciona o plano na figura
        ax.add_patch(plano_desenho)

        # desenha uma linha na superfície superior do plano para destacá-la
        ax.plot([-4, 4], [-3, -3 + comprimento_plano * np.sin(angulo_rad)],
               'k-', linewidth=3)

        # colocar o objeto no meio do plano (no meio da linha superior)
        pos_x_objeto = 0
        # Calcular y na linha do plano: y = y_inicial + (x + 4) * tan(angulo)
        pos_y_objeto = -3 + (pos_x_objeto + 4) * np.tan(angulo_rad)

        # Ajustar para colocar o objeto em cima (adicionar metade da altura)
        if objeto.get('tipo', 'retangulo') == 'retangulo':
            altura_obj = objeto.get('tamanho', [1, 1])[1]
            # Compensar pela rotação do objeto
            pos_y_objeto += altura_obj / 2 * np.cos(angulo_rad)
        else:
            raio_obj = objeto.get('tamanho', 0.5)
            pos_y_objeto += raio_obj

    # posição do objeto, caso o plano não seja inclinado
    else:
        pos_x_objeto = 0
        pos_y_objeto = 0

    # pega a forma do objeto, caso não esteja especificado será um retângulo
    tipo_objeto = objeto.get('tipo', 'retangulo')

    if tipo_objeto == 'retangulo':
        # definições do retângulo
        largura, altura = objeto.get('tamanho', [1, 1])
        cor = objeto.get('cor', 'lightblue')

        # rotaciona o retângulo caso o plano seja inclinado
        if plano.get('ativo', False):
            angulo_plano = plano.get('angulo', 30)
            angulo_rad = np.radians(angulo_plano)

            # cria um ângulo de rotação para que o retângulo gire e se alinhe com o plano
            angulo_rotacao = patches.transforms.Affine2D().rotate(angulo_rad) + ax.transData
            ret = patches.Rectangle((pos_x_objeto - largura/2, pos_y_objeto - altura/2),
                                   largura, altura, linewidth=2,
                                edgecolor='black', facecolor=cor, transform=angulo_rotacao)

        # desenha o objeto caso o plano não seja inclinado
        else:
            ret = patches.Rectangle((pos_x_objeto - largura/2, pos_y_objeto - altura/2),
                                   largura, altura, linewidth=2,
                                   edgecolor='black', facecolor=cor)
        # adiciona o retângulo no plano
        ax.add_patch(ret)

    # caso o objeto seja um círculo ao invés de um retângulo
    # elif tipo_objeto == 'circulo':
    #     raio = objeto.get('tamanho', 0.5)
    #     cor = objeto.get('cor', 'lightblue')
    #     # cria o círculo
    #     circ = patches.Circle((pos_x_objeto, pos_y_objeto), raio, linewidth=2,
    #                          edgecolor='black', facecolor=cor)
    #     # adiciona o círculo no plano
    #     ax.add_patch(circ)

    # desenha forças 
    forcas = json.get('forcas', [])

    # fixa um comprimento para o tamanho dos vetores das forças
    COMPRIMENTO_FORCA = 1.0

    for forca in forcas:
        nome = forca.get('nome', '')
        # magnitude = forca.get('magnitude', 0)
        if nome == "Atrito (Fat)":
          angulo = forca.get('angulo', 0) - 180
        else:
          angulo = forca.get('angulo', 0)   
        cor = forca.get('cor', 'red')
        ponto = forca.get('ponto_aplicacao', [0, 0])

        # conversão de graus para radianos
        angulo_rad = np.radians(angulo)

        # calculo dos componentes x e y das forças
        # lado adjacente
        dx = COMPRIMENTO_FORCA * np.cos(angulo_rad)
        # lado oposto
        dy = COMPRIMENTO_FORCA * np.sin(angulo_rad)

        # vetor das forças
        # (onde a força é aplicada em x, onde a força é aplicada em y, componente x da força, componete y da força [os outros argmentos definem o design da seta])
        ax.arrow(ponto[0] + pos_x_objeto, ponto[1] + pos_y_objeto, dx, dy,
                head_width=0.2, head_length=0.15, fc=cor, ec=cor,
                linewidth=2, length_includes_head=True)

        # calcula o posicionamento do nome da força
        label_x = ponto[0] + pos_x_objeto + dx * 1.2
        label_y = ponto[1] + pos_y_objeto + dy * 1.4

        ax.text(label_x, label_y, nome, ha='center', va='center', fontsize=10)


    # para que os rótulos não se sobreponham e caibam bem na figura
    plt.tight_layout()

    # plt.show()

    # criação temporária de um arquivo na memória RAM
    buffer = io.BytesIO()
    # como buffer não é o nome de um arquivo, os bytes da imagem são despejados dentro dele
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)

    # pega o que tem dentro do buffer
    img_data = buffer.getvalue()

    # transforma o conjunto de bytes em algo que o navegador consiga entender
    img_base64 = base64.b64encode(img_data).decode('utf-8')
    data_uri = f"data:image/png;base64,{img_base64}"

    return data_uri

    
if __name__ == "__main__":
    # Criar um exemplo de configuração
    config_exemplo ={
  "objeto": {
    "tipo": "retangulo",
    "tamanho": [1, 1],
    "cor": "gray",
    "massa": 5.0
  },
  "plano_inclinado": {
    "ativo": True,
    "angulo": 30,
  },
  "forcas": [
    {
      "nome": "Peso (P)",
      "magnitude": 49.0,
      "angulo": 270,
      "cor": "darkgreen",
      "ponto_aplicacao": [0, 0]
    },
    {
      "nome": "Normal (N)",
      "magnitude": 42.4,
      "angulo": 120,
      "cor": "blue",
      "ponto_aplicacao": [0, 0]
    },
    {
      "nome": "Atrito (Fat)",
      "magnitude": 10.0,
      "angulo": 210,
      "cor": "red",
      "ponto_aplicacao": [0, 0]
    }
  ]
}
    
url = desenharCopoLivre(config_exemplo)

print(url)