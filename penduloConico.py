import matplotlib
# utilização de um ambiente não interativo
# dessa forma o matplotlib gerará os gráficos apenas na memória e não tentará abrir uma janela para mostrá-lo
matplotlib.use("Agg")
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class PenduloConico:
    def __init__(self, config_file):
        
        with open(config_file, 'r') as f:
            config = json.load(f)

        self.L = config.get('comprimento', 3.0)
        self.theta = np.radians(config.get('angulo_conico', 30))
        self.raio_massa = config.get('raio_massa', 0.3)
        self.raio_posicoes = config.get('raio_posicoes', 0.15)
        self.cor_massa = config.get('cor_massa', '#4169E1')
        self.cor_fio = 'black'
        self.mostrar_gravidade = True

    def gerar_imagem(self, arquivo_saida='pendulo_conico.png'):
        """
        Gera a imagem do pêndulo cônico.
        """
        fig, ax = plt.subplots(figsize=(6, 6))

        # topo
        x_topo = 0
        y_topo = 0

        # comprimento L
        h = -self.L * np.cos(self.theta)

        # Raio do círculo horizontal
        r = self.L * np.sin(self.theta)

        # posição central do pêndulo
        x_massa = 0
        y_massa = h

        # posições extremas do pêndulo
        x_esq = -r
        y_esq = h

        x_dir = r
        y_dir = h

        # linha lateral
        ax.plot([x_topo, x_esq], [y_topo, y_esq], 'k--', linewidth=1.5, alpha=0.6)
        ax.plot([x_topo, x_dir], [y_topo, y_dir], 'k--', linewidth=1.5, alpha=0.6)

        # linha central
        ax.plot([x_topo, x_massa], [y_topo, y_massa], 'k-', linewidth=2)

        # representação da trajetória do pêndulo
        circle_base = patches.Circle((0, h), r, fill=False, edgecolor='gray',
                                    linestyle=':', linewidth=1.5, alpha=0.5)
        ax.add_patch(circle_base)

        # desenha a esfera na posição lateral
        circle_esq = patches.Circle((x_esq, y_esq), self.raio_posicoes,
                                   fill=False, edgecolor='black', linewidth=1.5)
        ax.add_patch(circle_esq)

        circle_dir = patches.Circle((x_dir, y_dir), self.raio_posicoes,
                                   fill=False, edgecolor='black', linewidth=1.5)
        ax.add_patch(circle_dir)

        # desenha a esfera na posição inicial
        circle_massa = patches.Circle((x_massa, y_massa), self.raio_massa,
                                     facecolor=self.cor_massa, edgecolor='black',
                                     linewidth=2)
        ax.add_patch(circle_massa)

        # desenha o ponto no topo
        ax.plot(x_topo, y_topo, 'ko', markersize=8)

        # rótulo 
        meio_fio_x = (x_topo + x_massa) / 2 + 0.3
        meio_fio_y = (y_topo + y_massa) / 2
        ax.text(meio_fio_x, meio_fio_y, 'ℓ', fontsize=20,
               verticalalignment='center')

        # seta da gravidade
        if self.mostrar_gravidade:
            seta_x = r + 0.8
            seta_y = h + 0.5
            ax.arrow(seta_x, seta_y, 0, -1.0,
                    head_width=0.2, head_length=0.2,
                    fc='black', ec='black', linewidth=2)
            ax.text(seta_x + 0.4, seta_y - 0.5, 'g', fontsize=18)

        # rótulo 'm' para a  massa 
        ax.text(x_massa, y_massa - 0.7, 'm', fontsize=16,
               horizontalalignment='center')

        ax.set_aspect('equal')
        ax.set_xlim(-r - 1.5, r + 1.5)
        ax.set_ylim(h - 1, 0.5)
        ax.axis('off')

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    config_exemplo = {
        "comprimento": 3.0,
        "angulo_conico": 30,
        "raio_massa": 0.3,
        "raio_posicoes": 0.15,
        "cor_massa": "#4169E1",
        "cor_fio": "black",
        "mostrar_seta_gravidade": True
    }


    with open('pendulo_config.json', 'w') as f:
        json.dump(config_exemplo, f, indent=4)

    pendulo = PenduloConico('pendulo_config.json')
    pendulo.gerar_imagem('pendulo_conico.png')