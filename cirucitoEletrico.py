import matplotlib.pyplot as plt
import io
import base64

class CircuitoEletrico:

    def __init__(self, json_config):
        
        self.config = json_config

        # cria uma figura e o conjunto de eixos
        self.fig, self.ax = plt.subplots(figsize=(6, 6))

        # Contador global de resistores
        self.resistor_count = 0

    def desenharResistor(self, x, y, label, orientacao='horizontal'):
        
        if orientacao == 'horizontal':
            # linha inicial
            self.ax.plot([x, x + 0.3], [y, y], 'k-', linewidth=2)
            # zigue-zague do resistor
            zigzag_x = [x + 0.3, x + 0.4, x + 0.5, x + 0.6, x + 0.7, x + 0.8, x + 0.9]
            zigzag_y = [y, y + 0.15, y - 0.15, y + 0.15, y - 0.15, y + 0.15, y]
            self.ax.plot(zigzag_x, zigzag_y, 'k-', linewidth=2)
            # linha final
            self.ax.plot([x + 0.9, x + 1.2], [y, y], 'k-', linewidth=2)
            # identificação do resistor
            self.ax.text(x + 0.6, y + 0.3, label, ha='center', fontsize=10)
            return x + 1.2, y
        else:
            # linha inicial
            self.ax.plot([x, x], [y, y - 0.3], 'k-', linewidth=2)
            # zigue-zague do resistor
            zigzag_x = [x, x + 0.15, x - 0.15, x + 0.15, x - 0.15, x + 0.15, x]
            zigzag_y = [y - 0.3, y - 0.4, y - 0.5, y - 0.6, y - 0.7, y - 0.8, y - 0.9]
            self.ax.plot(zigzag_x, zigzag_y, 'k-', linewidth=2)
            # linha final
            self.ax.plot([x, x], [y - 0.9, y - 1.2], 'k-', linewidth=2)
            # identificação do resistor
            self.ax.text(x + 0.3, y - 0.6, label, ha='left', fontsize=10)
            return x, y - 1.2

    def desenharBateria(self, x, y, voltagem, orientacao='horizontal'):
        
        # caso a bateria possua orintação horizontal
        if orientacao == 'horizontal':
            # Linha inicial
            self.ax.plot([x, x + 0.3], [y, y], 'k-', linewidth=2)
            # Terminal negativo (linha curta)
            self.ax.plot([x + 0.3, x + 0.3], [y - 0.15, y + 0.15], 'k-', linewidth=3)
            # Terminal positivo (linha longa)
            self.ax.plot([x + 0.5, x + 0.5], [y - 0.25, y + 0.25], 'k-', linewidth=3)
            # Linha final
            self.ax.plot([x + 0.5, x + 0.8], [y, y], 'k-', linewidth=2)
            # Label com voltagem
            self.ax.text(x + 0.4, y + 0.6, f'{voltagem}V', ha='center', fontsize=10)
            # Sinais + e -
            self.ax.text(x + 0.5, y + 0.35, '+', ha='center', fontsize=12, fontweight='bold')
            self.ax.text(x + 0.3, y + 0.35, '-', ha='center', fontsize=12, fontweight='bold')
            return x + 0.8, y
        # caso a bateria possua orientação vertical
        else:
            self.ax.plot([x, x], [y, y - 0.3], 'k-', linewidth=2)
            self.ax.plot([x - 0.15, x + 0.15], [y - 0.3, y - 0.3], 'k-', linewidth=3)
            self.ax.plot([x - 0.25, x + 0.25], [y - 0.5, y - 0.5], 'k-', linewidth=3)
            self.ax.plot([x, x], [y - 0.5, y - 0.8], 'k-', linewidth=2)
            self.ax.text(x + 0.4, y - 0.4, f'{voltagem}V', ha='left', fontsize=10)
            return x, y - 0.8

    def desenharFio(self, x1, y1, x2, y2):
        
        self.ax.plot([x1, x2], [y1, y2], 'k-', linewidth=2)

    def desenharAmperimetro(self, x, y, label='A', orientacao='horizontal'):
        
        if orientacao == 'horizontal':
            # linha inicial
            self.ax.plot([x, x + 0.2], [y, y], 'k-', linewidth=2)
            # círculo do amperímetro
            circulo = plt.Circle((x + 0.5, y), 0.3, fill=False, edgecolor='black', linewidth=2)
            self.ax.add_patch(circulo)
            # rótulo do amperímetro
            self.ax.text(x + 0.5, y, label, ha='center', va='center', fontsize=14, fontweight='bold')
            # Linha final
            self.ax.plot([x + 0.8, x + 1.0], [y, y], 'k-', linewidth=2)
            return x + 1.0, y
        else:
            # linha inicial
            self.ax.plot([x, x], [y, y - 0.2], 'k-', linewidth=2)
            # círculo do amperímetro
            circulo = plt.Circle((x, y - 0.5), 0.3, fill=False, edgecolor='black', linewidth=2)
            self.ax.add_patch(circulo)
            # rótulo do amperímetro
            self.ax.text(x, y - 0.5, label, ha='center', va='center', fontsize=14, fontweight='bold')
            # linha final
            self.ax.plot([x, x], [y - 0.8, y - 1.0], 'k-', linewidth=2)
            return x, y - 1.0

    def desenharVoltimetro(self, x, y, label='V', orientacao='horizontal'):
        
        if orientacao == 'horizontal':
            # linha inicial
            self.ax.plot([x, x + 0.2], [y, y], 'k-', linewidth=2)
            # círculo do voltímetro
            circulo = plt.Circle((x + 0.5, y), 0.3, fill=False, edgecolor='black', linewidth=2)
            self.ax.add_patch(circulo)
            # rótulo do voltímetro
            self.ax.text(x + 0.5, y, label, ha='center', va='center', fontsize=14, fontweight='bold')
            # linha final
            self.ax.plot([x + 0.8, x + 1.0], [y, y], 'k-', linewidth=2)
            return x + 1.0, y
        else:
            # linha inicial
            self.ax.plot([x, x], [y, y - 0.2], 'k-', linewidth=2)
            # círculo do voltímetro
            circulo = plt.Circle((x, y - 0.5), 0.3, fill=False, edgecolor='black', linewidth=2)
            self.ax.add_patch(circulo)
            # rótulo do voltímetro
            self.ax.text(x, y - 0.5, label, ha='center', va='center', fontsize=14, fontweight='bold')
            # linha final
            self.ax.plot([x, x], [y - 0.8, y - 1.0], 'k-', linewidth=2)
            return x, y - 1.0

    def gerarCircuito(self):
        
        sections = self.config.get('sections', [])
        x, y = 1, 5

        # Desenha a bateria
        voltagem = self.config.get('voltagem', 12)
        x, y = self.desenharBateria(x, y, voltagem)

        # Processa cada seção do circuito
        for section in sections:
            if section['tipo'] == 'serie':
                # Adiciona componentes em série
                for componente in section['components']:
                    if isinstance(componente, dict):
                        comp_type = componente.get('tipo', 'resistor')
                        if comp_type == 'resistor':
                            self.resistor_count += 1
                            label = f"R{self.resistor_count}\n{componente['value']}Ω"
                            x, y = self.desenharResistor(x, y, label)
                        elif comp_type == 'amperimetro':
                            label = componente.get('label', 'A')
                            x, y = self.desenharAmperimetro(x, y, label)
                        elif comp_type == 'voltimetro':
                            label = componente.get('label', 'V')
                            x, y = self.desenharVoltimetro(x, y, label)
                    else:
                        # Compatibilidade com formato antigo (apenas valores de resistores)
                        self.resistor_count += 1
                        label = f"R{self.resistor_count}\n{componente}Ω"
                        x, y = self.desenharResistor(x, y, label)

            elif section['tipo'] == 'paralelo':
                # Ponto de divisão
                junction_x = x + 0.5
                self.desenharFio(x, y, junction_x, y)

                # Desenha ramos paralelos
                branches = section['branches']
                num_branches = len(branches)
                spacing = 1.2

                max_branch_x = junction_x

                for i, branch_componentes in enumerate(branches):
                    branch_y = y - (i - (num_branches-1)/2) * spacing

                    # Linha vertical até o ramo
                    self.desenharFio(junction_x, y, junction_x, branch_y)

                    # Desenha componentes do ramo
                    branch_x = junction_x
                    for componente in branch_componentes:
                        # método isinstance verifica se um objeto é de determinado tipo, nesse caso verifica se 'component' é do tipo dicionário
                        if isinstance(componente, dict):
                            comp_type = componente.get('tipo', 'resistor')
                            if comp_type == 'resistor':
                                self.resistor_count += 1
                                label = f"R{self.resistor_count}\n{componente['value']}Ω"
                                branch_x, branch_y = self.desenharResistor(branch_x, branch_y, label)
                            elif comp_type == 'amperimetro':
                                label = componente.get('label', 'A')
                                branch_x, branch_y = self.desenharAmperimetro(branch_x, branch_y, label)
                            elif comp_type == 'voltimetro':
                                label = componente.get('label', 'V')
                                branch_x, branch_y = self.desenharVoltimetro(branch_x, branch_y, label)
                        else:
                            # Compatibilidade com formato antigo (apenas valores)
                            self.resistor_count += 1
                            label = f"R{self.resistor_count}\n{componente}Ω"
                            branch_x, branch_y = self.desenharResistor(branch_x, branch_y, label)

                    max_branch_x = max(max_branch_x, branch_x)

                    # Conecta ao ponto de junção final
                    end_junction_x = max_branch_x + 0.5
                    self.desenharFio(branch_x, branch_y, end_junction_x, branch_y)
                    self.desenharFio(end_junction_x, branch_y, end_junction_x, y)

                # Atualiza posição
                x = end_junction_x

        # Fecha o circuito
        self.desenharFio(x, y, x + 0.5, y)
        self.desenharFio(x + 0.5, y, x + 0.5, y - 3)
        self.desenharFio(x + 0.5, y - 3, 1, y - 3)
        self.desenharFio(1, y - 3, 1, y)
        
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        plt.tight_layout()
        # plt.show()

        # criação temporária de um arquivo na memória RAM
        buffer = io.BytesIO()
        # como buffer não é o nome de um arquivo, os bytes da imagem são despejados dentro dele
        plt.savefig(buffer, format='png', bbox_inches='tight')
        plt.close()  

        # pega o que tem dentro do buffer
        img_data = buffer.getvalue()

        # transforma o conjunto de bytes em algo que o navegador consiga entender
        img_base64 = base64.b64encode(img_data).decode('utf-8')
        data_uri = f"data:image/png;base64,{img_base64}"

        return data_uri

circuito_teste = {
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
}

circuito_eletrico = CircuitoEletrico(circuito_teste)
uri = circuito_eletrico.gerarCircuito()

print(uri)

