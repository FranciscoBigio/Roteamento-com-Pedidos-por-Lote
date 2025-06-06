# =========================================
# File: main.py
# =========================================
import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import heapq
from collections import Counter
import itertools
import copy
import random

# -----------------------------------------
# Mapeamento de nós para objetos
# -----------------------------------------
OBJETO_POR_NO = {
    'A1': 'caneta',
    'A2': 'caderno',
    'A3': 'lapis',
    'A4': 'resma',
    'B1': 'borracha',
    'B2': 'estojo',
    'B3': 'apontador',
    'B4': 'agenda',
    'C1': 'cola',
    'C2': 'tesoura',
    'C3': 'corretivo',
    'C4': 'clip',
    'D1': 'regua',
    'D2': 'calculadora',
    'D3': 'lapisera',
    'D4': 'postit',
    'E1': 'pilha',
    'E2': 'mouse',
    'E3': 'teclado',
    'E4': 'monitor'
}
NO_POR_OBJETO = {v: k for k, v in OBJETO_POR_NO.items()}
ITENS_DISPONIVEIS = list(NO_POR_OBJETO.keys())

# -----------------------------------------
# Funções de Dijkstra
# -----------------------------------------
def dijkstra(grafo, inicio):
    distancias = {no: float('inf') for no in grafo}
    distancias[inicio] = 0
    fila = [(0, inicio)]
    caminho = {}

    while fila:
        dist_atual, no_atual = heapq.heappop(fila)
        if dist_atual > distancias[no_atual]:
            continue
        for vizinho, peso in grafo[no_atual].items():
            nova_dist = dist_atual + peso
            if nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                heapq.heappush(fila, (nova_dist, vizinho))
                caminho[vizinho] = no_atual
    return distancias, caminho


def reconstruir_caminho(origem, destino, caminho):
    rota = [destino]
    atual = destino
    while atual in caminho:
        atual = caminho[atual]
        rota.insert(0, atual)
    return rota

# -----------------------------------------
# Função para criar grafo do armazém (mapa)
# -----------------------------------------
def criar_grafo_armazen():
    grafo = {
        'Entrada': {'A1': 6, 'B1': 6, 'C1': 6, 'D1': 6,'E1': 6},
        'A1': {'A2': 2, 'B1': 2},
        'A2': {'A3': 2, 'B2': 2},
        'A3': {'A4': 2, 'B3': 2},
        'A4': {'B4': 2, 'Saída': 6},
        'B1': {'B2': 2, 'C1': 2},
        'B2': {'B3': 2, 'C2': 2},
        'B3': {'B4': 2, 'C3': 2},
        'B4': {'C4': 2, 'Saída': 6},
        'C1': {'C2': 2, 'D1': 2},
        'C2': {'C3': 2, 'D2': 2},
        'C3': {'C4': 2, 'D3': 2},
        'C4': {'D4': 2, 'Saída': 6},
        'D1': {'D2': 2, 'E1': 2},
        'D2': {'D3': 2, 'E2': 2},
        'D3': {'D4': 2, 'E3': 2},
        'D4': {'E4': 2, 'Saída': 6},
        'E1': {'E2': 2},
        'E2': {'E3': 2,},
        'E3': {'E4': 2,},
        'E4': {'Saída': 6},
        'Saída': {}
    }
    grafo_bidirecional = copy.deepcopy(grafo)
    for u, vizinhos in grafo.items():
        for v, peso in vizinhos.items():
            if v not in grafo_bidirecional:
                grafo_bidirecional[v] = {}
            if u not in grafo_bidirecional[v]:
                grafo_bidirecional[v][u] = peso
    return grafo_bidirecional

# -----------------------------------------
# Classe de interface e lógica de plotagem
# -----------------------------------------
class InterfaceApp:
    def __init__(self, master):
        self.master = master
        master.title("Roteamento com Pedidos por Lote")

        self.base_grafo = criar_grafo_armazen()
        self.grafo = copy.deepcopy(self.base_grafo)
        self.origem = 'Entrada'
        self.destino = 'Saída'
        self.rota = []
        self.nos_selecionados = []
        self.custo_total = None

        # Label de instrução
        instrucao = "Roteamento com Pedidos por Lote"
        self.label_info = tk.Label(master, text=instrucao, font=("Arial", 12), justify="center")
        self.label_info.pack(pady=5)

        # Área para exibir legenda de nós à esquerda (sigla + nome do objeto)
        legend_text = "\n".join([f"{no} - {OBJETO_POR_NO[no].capitalize()}"
                                 for no in sorted(OBJETO_POR_NO)])
        self.legend_label = tk.Label(master, text=legend_text, font=("Arial", 10), justify="left")
        self.legend_label.pack(side=tk.LEFT, padx=10)

        # Frame contendo canvas + scrollbar horizontal para pedidos
        self.pedidos_scroll_frame = ttk.Frame(master)
        self.pedidos_scroll_frame.pack(fill="x", padx=10, pady=5)

        self.pedidos_canvas = tk.Canvas(self.pedidos_scroll_frame, height=30)
        self.pedidos_scroll_x = ttk.Scrollbar(
            self.pedidos_scroll_frame,
            orient="horizontal",
            command=self.pedidos_canvas.xview
        )
        self.pedidos_canvas.configure(xscrollcommand=self.pedidos_scroll_x.set)

        self.pedidos_scroll_x.pack(side="bottom", fill="x")
        self.pedidos_canvas.pack(side="left", fill="x", expand=True)

        self.pedidos_inner_frame = ttk.Frame(self.pedidos_canvas)
        self.pedidos_canvas.create_window((0, 0), window=self.pedidos_inner_frame, anchor="nw")

        self.pedidos_label = ttk.Label(self.pedidos_inner_frame, text="Pedidos:", font=("Arial", 14), justify="center")
        self.pedidos_label.pack(side="top")

        # Botão para gerar novo lote
        self.botao_calcular = tk.Button(
            master,
            text="Calcular Novo Lote",
            command=self.gerar_lote_e_calcular,
            font=("Arial", 11),
            bg="#007bff",
            fg="white",
            padx=10,
            pady=10
        )
        self.botao_calcular.pack(pady=5)

        # Label para status (exibe rota e custo)
        self.status = tk.Label(master, text="", font=("Arial", 13))
        self.status.pack(pady=5)

        # Frame contendo canvas para o gráfico
        self.frame_plot = tk.Frame(master, bd=2, relief=tk.SUNKEN)
        self.frame_plot.pack(padx=10, pady=10, fill='both', expand=True)

        # Canvas do Matplotlib (não rolável)
        self.fig, self.ax = plt.subplots()
        self.canvas_mpl = FigureCanvasTkAgg(self.fig, master=self.frame_plot)
        self.plot_widget = self.canvas_mpl.get_tk_widget()
        self.plot_widget.pack(fill="both", expand=True)

        # Primeiro desenho do grafo
        self.desenhar_grafo_base()

    def gerar_lote_e_calcular(self):
        # Gera 5 pedidos aleatórios (1-2 itens)
        pedidos = []
        all_pontos = []
        self.nos_selecionados = []
        for _ in range(5):
            qtd = random.randint(1, 2)
            itens = random.sample(ITENS_DISPONIVEIS, qtd)
            pedidos.append(itens)
            for obj in itens:
                no = NO_POR_OBJETO[obj]
                if no not in all_pontos:
                    all_pontos.append(no)
                    self.nos_selecionados.append(no)

        # Exibe pedidos lado a lado (inicial maiúscula)
        pedidos_texto = [f"Pedido {idx+1}: {', '.join([item.capitalize() for item in itens])}"
                         for idx, itens in enumerate(pedidos)]
        texto_pedidos = " | ".join(pedidos_texto)
        self.pedidos_label.config(text=texto_pedidos)
        self.pedidos_canvas.update_idletasks()
        self.pedidos_canvas.config(scrollregion=self.pedidos_canvas.bbox("all"))

        # Calcula rota
        melhor_rota, melhor_custo = self.calcular_melhor_rota(all_pontos)
        if melhor_rota:
            texto_status = f"Rota (custo {melhor_custo}): {' → '.join(melhor_rota)}"
            self.status.config(text=texto_status)
        else:
            self.status.config(text="Não foi possível encontrar rota válida.")

        self.rota = melhor_rota or []
        self.desenhar_grafo_base()

    def calcular_melhor_rota(self, pontos):
        if not pontos:
            dist, caminho = dijkstra(self.grafo, self.origem)
            if self.destino in dist:
                return reconstruir_caminho(self.origem, self.destino, caminho), dist[self.destino]
            else:
                return None, None

        melhor_rota = None
        melhor_custo = float('inf')

        for perm in itertools.permutations(pontos):
            custo = 0
            rota_total = []
            atual = self.origem
            valido = True

            for p in perm:
                dist, caminho = dijkstra(self.grafo, atual)
                if p in dist:
                    sub = reconstruir_caminho(atual, p, caminho)
                    if rota_total:
                        rota_total += sub[1:]
                    else:
                        rota_total += sub
                    custo += dist[p]
                    atual = p
                else:
                    valido = False
                    break

            if not valido:
                continue

            dist, caminho = dijkstra(self.grafo, atual)
            if self.destino in dist:
                sub = reconstruir_caminho(atual, self.destino, caminho)
                rota_total += sub[1:]
                custo += dist[self.destino]
            else:
                continue

            if custo < melhor_custo:
                melhor_custo = custo
                melhor_rota = rota_total

        return melhor_rota, (melhor_custo if melhor_custo < float('inf') else None)

    def desenhar_grafo_base(self):
        self.ax.clear()
        G = nx.DiGraph()
        for no, vizinhos in self.grafo.items():
            for v, peso in vizinhos.items():
                G.add_edge(no, v, weight=peso)

        pos = {
            'Entrada': (-3,11),
            'A1': (1,17), 'A2': (4,17), 'A3': (7,17), 'A4': (10,17),
            'B1': (1,14), 'B2': (4,14), 'B3': (7,14), 'B4': (10,14),
            'C1': (1,11), 'C2': (4,11), 'C3': (7,11), 'C4': (10,11),
            'D1': (1,8), 'D2': (4,8), 'D3': (7,8), 'D4': (10,8),
            'E1': (1,5),  'E2': (4,5),  'E3': (7,5),  'E4': (10,5),
            'Saída': (14,11)
        }

        nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=1500, ax=self.ax)
        nx.draw_networkx_labels(G, pos, font_size=14, font_family='Arial', ax=self.ax)
        nx.draw_networkx_edges(G, pos, edge_color='gray', width=2, ax=self.ax)

        for (u, v, d) in G.edges(data=True):
            x1, y1 = pos[u]
            x2, y2 = pos[v]
            xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
            if abs(x1 - x2) < 0.1:
                self.ax.text(xm + 0.3, ym, str(d['weight']), fontsize=12,
                             fontfamily='Arial', ha='left', va='center')
            else:
                self.ax.text(xm, ym + 0.4, str(d['weight']), fontsize=12,
                             fontfamily='Arial', ha='center', va='bottom')

        if self.nos_selecionados:
            nx.draw_networkx_nodes(G, pos, nodelist=self.nos_selecionados,
                                   node_color='orange', node_size=1500, ax=self.ax)

        if self.rota:
            pares_rota = list(zip(self.rota, self.rota[1:]))
            contador = Counter(tuple(sorted(p)) for p in pares_rota)
            for u, v in pares_rota:
                key = tuple(sorted((u, v)))
                cor = 'purple' if contador[key] > 1 else 'red'
                style = 'solid' if cor == 'purple' else 'solid'
                nx.draw_networkx_edges(G, pos, edgelist=[(u, v)],
                                       edge_color=cor, style=style, width=4, ax=self.ax)

            nx.draw_networkx_nodes(G, pos, nodelist=[self.rota[0]],
                                   node_color='green', node_size=1500, ax=self.ax)
            nx.draw_networkx_nodes(G, pos, nodelist=[self.rota[-1]],
                                   node_color='blue', node_size=1500, ax=self.ax)

        handles = []
        handles.append(plt.Line2D([], [], marker='o', color='orange',
                                  linestyle='None', markersize=10,
                                  label='Pontos de Picking'))
        handles.append(plt.Line2D([], [], color='red', linewidth=4,
                                  linestyle='solid', label='Melhor Rota Possível'))
        handles.append(plt.Line2D([], [], color='purple', linewidth=4,
                                  linestyle='solid',
                                  label='Rota Bidirecional / Repetida'))

        self.ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(-0.15, 1.0), fontsize=6.8, framealpha=0.6)


        self.ax.set_title("Mapa do Armazém com Pedidos", fontsize=15)
        self.ax.axis('off')
        self.canvas_mpl.draw()


# -----------------------------------------
# Execução principal
# -----------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceApp(root)
    root.mainloop()