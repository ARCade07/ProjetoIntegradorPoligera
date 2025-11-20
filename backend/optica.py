import json
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO


class SistemaOptico:

    def __init__(self, json_data):
        self.data = json.loads(json_data) if isinstance(json_data, str) else json_data
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.setup_axes()

    def setup_axes(self):
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
        self.ax.axhline(y=0, color='gray', linewidth=0.8, alpha=0.5)
        
        # remove bordas e valores dos eixos
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
    def gerar_imagem(self):
        
        elementos = self.data.get("elements", [])

        # Primeiro, processar objetos e elementos ópticos
        object_data = None
        lens_data = None
        mirror_data = None

        for elemento in elementos:
            elem_tipo = elemento.get("type")

            if elem_tipo == "object":
                object_data = elemento
                self.desenhar_objeto(elemento)

            elif elem_tipo == "lens":
                lens_data = elemento
                self.desenhar_lente(elemento)

            elif elem_tipo == "mirror":
                mirror_data = elemento
                self.desenhar_espelho(elemento)

            elif elem_tipo == "image_plane":
                self.desenhar_imagem_plana(elemento)

        # Calcular e desenhar raios com física correta
        if object_data and lens_data:
            self.raios_lente(object_data, lens_data)
        elif object_data and mirror_data:
            self.raios_espelho(object_data, mirror_data)

        self.ax.margins(0.15)
        plt.tight_layout()
        
        # Salvar em buffer de memória
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buffer.seek(0)
        
        # Converter para base64
        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        data_uri = f"data:image/png;base64,{img_base64}"
        
        plt.close()
        
        return data_uri

    def desenhar_objeto(self, element):
        x = element.get("position", -100)
        h = element.get("height", 10)
        color = element.get("color", "blue")

        # Seta do objeto
        self.ax.annotate('', xy=(x, h), xytext=(x, 0),
                        arrowprops=dict(arrowstyle='->', lw=2.5, color=color))
        self.ax.plot([x, x], [0, h], color=color, linewidth=2.5)
        self.ax.text(x - 8, h/2, 'O', fontsize=12, fontweight='bold',
                    color=color, ha='right')

    def desenhar_lente(self, element):
        x = element.get("position", 0)
        d = element.get("diameter", 30)
        f = element.get("focal_length", 50)
        lens_type = element.get("lens_type", "convergent")

        r = d / 2

        # Desenhar forma da lente
        y = np.linspace(-r, r, 100)

        if lens_type == "convergent":
            # Biconvexa
            curv = 0.15 * r
            x_left = x - curv * np.sqrt(np.maximum(0, 1 - (y/r)**2))
            x_right = x + curv * np.sqrt(np.maximum(0, 1 - (y/r)**2))
        else:
            # Bicôncava
            curv = 0.15 * r
            x_left = x + curv * np.sqrt(np.maximum(0, 1 - (y/r)**2))
            x_right = x - curv * np.sqrt(np.maximum(0, 1 - (y/r)**2))

        self.ax.fill_betweenx(y, x_left, x_right, alpha=0.25, color='cyan',
                             edgecolor='blue', linewidth=2)
        self.ax.plot([x, x], [-r, r], 'b-', linewidth=2)

        # Focos
        if f > 0:
            self.ax.plot(x + f, 0, 'ro', markersize=6, zorder=10)
            self.ax.text(x + f, -4, 'F', ha='center', fontsize=10,
                        color='red', fontweight='bold')
            self.ax.plot(x - f, 0, 'ro', markersize=6, zorder=10)
            self.ax.text(x - f, -4, "F'", ha='center', fontsize=10,
                        color='red', fontweight='bold')


    def desenhar_espelho(self, element):
        x = element.get("position", 0)
        h = element.get("height", 50)
        mirror_type = element.get("mirror_type", "plane")

        if mirror_type == "plane":
            # Espelho plano
            self.ax.plot([x, x], [-h/2, h/2], 'k-', linewidth=3.5, solid_capstyle='butt')

            # Hachuras (padrão de espelho)
            for i in np.arange(-h/2, h/2, 5):
                self.ax.plot([x, x + 3], [i, i + 3], 'k-', linewidth=1)


    def desenhar_imagem_plana(self, element):
        x = element.get("position", 60)
        h = element.get("height", 40)

        self.ax.plot([x, x], [-h/2, h/2], 'k-', linewidth=2.5)
        self.ax.text(x, -h/2 - 5, 'Imagem', ha='center', fontsize=9, fontweight='bold')

    def raios_lente(self, obj_element, lens_element):
        x_obj = obj_element.get("position", -100)
        h_obj = obj_element.get("height", 10)
        x_lens = lens_element.get("position", 0)
        f = lens_element.get("focal_length", 50)
        d_lens = lens_element.get("diameter", 30)

        # Usar equação das lentes: 1/f = 1/do + 1/di
        do = abs(x_lens - x_obj)  # distância objeto

        # Calcular distância da imagem
        if do != f:
            di = (f * do) / (do - f)
            x_img = x_lens + di

            # Calcular altura da imagem: hi/ho = -di/do
            h_img = -(h_obj * di) / do
        else:
            # Objeto no foco - raios saem paralelos
            di = float('inf')
            x_img = x_lens + 150
            h_img = 0

        # Raio 1: Paralelo ao eixo, passa pelo foco
        y_lens_1 = h_obj
        if abs(y_lens_1) <= d_lens/2:
            self.ax.plot([x_obj, x_lens], [h_obj, h_obj], 'r-', linewidth=1.5, alpha=0.8)
            if di != float('inf'):
                self.ax.plot([x_lens, x_img], [h_obj, h_img], 'r-', linewidth=1.5, alpha=0.8)
            else:
                self.ax.plot([x_lens, x_lens + 150], [h_obj, h_obj], 'r--', linewidth=1.5, alpha=0.8)

        # Raio 2: Passa pelo centro óptico (não desvia)
        if di != float('inf'):
            self.ax.plot([x_obj, x_img], [h_obj, h_img], 'b-', linewidth=1.5, alpha=0.8)
        else:
            self.ax.plot([x_obj, x_lens + 150], [h_obj, h_obj * (x_lens + 150 - x_obj) / (x_lens - x_obj)],
                        'b-', linewidth=1.5, alpha=0.8)

        # Raio 3: Passa pelo foco, sai paralelo
        x_focus = x_lens - f
        if x_obj < x_focus < x_lens:
            # Calcular altura onde raio atinge lente
            slope = (0 - h_obj) / (x_focus - x_obj)
            y_at_lens = h_obj + slope * (x_lens - x_obj)

            if abs(y_at_lens) <= d_lens/2:
                self.ax.plot([x_obj, x_lens], [h_obj, y_at_lens], 'g-', linewidth=1.5, alpha=0.8)
                if di != float('inf'):
                    self.ax.plot([x_lens, x_img], [y_at_lens, h_img], 'g-', linewidth=1.5, alpha=0.8)
                else:
                    self.ax.plot([x_lens, x_lens + 150], [y_at_lens, y_at_lens], 'g--', linewidth=1.5, alpha=0.8)

        # Desenhar imagem
        if di != float('inf') and abs(h_img) > 0.1:
            if h_img < 0:
                # Imagem invertida
                self.ax.annotate('', xy=(x_img, h_img), xytext=(x_img, 0),
                               arrowprops=dict(arrowstyle='->', lw=2, color='purple'))
                self.ax.plot([x_img, x_img], [0, h_img], 'purple', linewidth=2)
                self.ax.text(x_img + 5, h_img/2, "I", fontsize=11, fontweight='bold', color='purple')
            else:
                # Imagem direita
                self.ax.annotate('', xy=(x_img, h_img), xytext=(x_img, 0),
                               arrowprops=dict(arrowstyle='->', lw=2, color='purple'))
                self.ax.plot([x_img, x_img], [0, h_img], 'purple', linewidth=2)
                self.ax.text(x_img + 5, h_img/2, "I", fontsize=11, fontweight='bold', color='purple')

    def raios_espelho(self, obj_element, mirror_element):
        x_obj = obj_element.get("position", -50)
        h_obj = obj_element.get("height", 20)
        x_mirror = mirror_element.get("position", 0)
        mirror_type = mirror_element.get("mirror_type", "plane")

        if mirror_type == "plane":
            # Espelho plano: imagem virtual simétrica
            x_img = x_mirror + (x_mirror - x_obj)
            h_img = h_obj

            # Raio 1: Do topo do objeto ao topo do espelho
            y_mirror_1 = h_obj * 0.5
            self.ax.plot([x_obj, x_mirror], [h_obj, y_mirror_1], 'r-', linewidth=1.5, alpha=0.8)

            # Raio refletido
            angle_in = np.arctan2(y_mirror_1 - h_obj, x_mirror - x_obj)
            angle_out = np.pi - angle_in
            x_end = x_mirror + 100
            y_end = y_mirror_1 + 100 * np.tan(angle_out)
            self.ax.plot([x_mirror, x_end], [y_mirror_1, y_end], 'r-', linewidth=1.5, alpha=0.8)

            # Prolongamento virtual
            self.ax.plot([x_mirror, x_img], [y_mirror_1, h_img], 'r--', linewidth=1.5, alpha=0.5)

            # Raio 2: Do topo através do ponto médio
            y_mirror_2 = 0
            self.ax.plot([x_obj, x_mirror], [h_obj, y_mirror_2], 'b-', linewidth=1.5, alpha=0.8)

            # Raio refletido
            angle_in2 = np.arctan2(y_mirror_2 - h_obj, x_mirror - x_obj)
            angle_out2 = np.pi - angle_in2
            y_end2 = y_mirror_2 + 100 * np.tan(angle_out2)
            self.ax.plot([x_mirror, x_end], [y_mirror_2, y_end2], 'b-', linewidth=1.5, alpha=0.8)

            # Prolongamento virtual
            self.ax.plot([x_mirror, x_img], [y_mirror_2, h_img], 'b--', linewidth=1.5, alpha=0.5)

            # Desenhar imagem virtual
            self.ax.plot([x_img, x_img], [0, h_img], 'purple', linewidth=2, linestyle='--', alpha=0.6)
            self.ax.annotate('', xy=(x_img, h_img), xytext=(x_img, 0),
                           arrowprops=dict(arrowstyle='->', lw=2, color='purple', alpha=0.6, linestyle='dashed'))
            self.ax.text(x_img + 5, h_img/2, "I", fontsize=10, fontweight='bold',
                        color='purple', alpha=0.7)
            
