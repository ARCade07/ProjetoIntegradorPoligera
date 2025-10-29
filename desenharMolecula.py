import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
import io
import base64

class Moleculas:
    def __init__(self):
        # cores padrão átomos
        self.cor_atomo = {
            'H': '#FFFFFF',  
            'C': '#909090',  
            'N': '#3050F8',  
            'O': '#FF0D0D',  
            'S': '#FFFF30',  
            'P': '#FF8000',  
            'Cl': '#1FF01F', 
        }

        # tamanho padrão átomos
        self.raio_atomo = {
            'H': 0.3,
            'C': 0.4,
            'N': 0.4,
            'O': 0.4,
            'S': 0.5,
            'P': 0.4,
            'Cl': 0.5,
        }

    def desenharMolecula(self, json_molecula):
        """
        {
            "atomos": [{"elemento": "C", "x": 0, "y": 0}, ...],
            "ligações": [[0, 1, 1], [1, 2, 2], ...]
        }
        """
        atomos = json_molecula['atomos']
        ligacoes = json_molecula['ligações']

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_aspect('equal')

        # desenha as ligções primeiro para que depois os átomos possom sobrepô-las
        for ligacao in ligacoes:
            i, j, tipo_ligacao = ligacao
            x1, y1 = atomos[i]['x'], atomos[i]['y']
            x2, y2 = atomos[j]['x'], atomos[j]['y']

            if tipo_ligacao == 1:
                # ligação simples
                ax.plot([x1, x2], [y1, y2], 'k-', linewidth=3, zorder=1)
            elif tipo_ligacao == 2:
                # ligação dupla
                dx = x2 - x1
                dy = y2 - y1
                length = np.sqrt(dx**2 + dy**2)
                offset_x = -dy / length * 0.1
                offset_y = dx / length * 0.1

                ax.plot([x1 + offset_x, x2 + offset_x],
                       [y1 + offset_y, y2 + offset_y], 'k-', linewidth=2, zorder=1)
                ax.plot([x1 - offset_x, x2 - offset_x],
                       [y1 - offset_y, y2 - offset_y], 'k-', linewidth=2, zorder=1)
            elif tipo_ligacao == 3:
                # ligação tripla
                dx = x2 - x1
                dy = y2 - y1
                length = np.sqrt(dx**2 + dy**2)
                offset_x = -dy / length * 0.15
                offset_y = dx / length * 0.15

                ax.plot([x1, x2], [y1, y2], 'k-', linewidth=2, zorder=1)
                ax.plot([x1 + offset_x, x2 + offset_x],
                       [y1 + offset_y, y2 + offset_y], 'k-', linewidth=2, zorder=1)
                ax.plot([x1 - offset_x, x2 - offset_x],
                       [y1 - offset_y, y2 - offset_y], 'k-', linewidth=2, zorder=1)

        # desenhar átomos
        for atomo in atomos:
            elemento = atomo['elemento']
            x, y = atomo['x'], atomo['y']
            raio = self.raio_atomo.get(elemento, 0.4)
            cor = self.cor_atomo.get(elemento, '#FF00FF')

            circle = Circle((x, y), raio, color=cor, ec='black',
                          linewidth=2, zorder=2)
            ax.add_patch(circle)

            # sigla elemento
            ax.text(x, y, elemento, ha='center', va='center',
                   fontsize=14, fontweight='bold', zorder=3)

        ax.set_xlim(-2, 5)
        ax.set_ylim(-2, 4)
        ax.axis('off')

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

    def carregarJson(self, json):
        json_molecula = json
        self.desenharMolecula(json_molecula)

        return self.desenharMolecula(json_molecula)


if __name__ == "__main__":
    molecula = Moleculas()

    acido_cloridrico = {
  "atomos": [
    {"elemento": "H", "x": 0.5, "y": 1.5},
    {"elemento": "Cl", "x": 2.0, "y": 1.5}
  ],
  "ligações": [[0, 1, 1]]
}
    
    uri = molecula.carregarJson(acido_cloridrico)
    print(uri)