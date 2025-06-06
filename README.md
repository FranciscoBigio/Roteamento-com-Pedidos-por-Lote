# Roteamento-com-Pedidos-por-Lote
Em grandes centros de distribuição, a eficiência nos processos de coleta de itens (picking) impacta diretamente na produtividade e nos custos logísticos. Este projeto visa desenvolver um sistema que, a partir de um mapa de um armazém modelado como grafo, calcule automaticamente a rota mais curta para o processo de Picking por Lote. Baseado no algoritmo de Dijkstra, o sistema gera lotes de pedidos de forma aleatória, calcula a sequência ótima de vértices a serem visitados e exibe, em uma interface gráfica interativa (Tkinter + NetworkX + Matplotlib), o caminho otimizado para o operador logístico seguir.

🎯 Objetivos
Automatizar o cálculo de rotas curtas para picking de múltiplos pedidos, agrupados em lote.

Visibilizar, em tempo real, o grafo do armazém e destacar a rota gerada de maneira clara e interativa.

Oferecer flexibilidade de cenários por meio de geração aleatória de pedidos, permitindo testes e simulações variadas.

Demonstrar o uso de estruturas de dados avançadas (fila de prioridade, manipulação de grafos, combinações de vértices) e bibliotecas gráficas em Python.

⚙️ Funcionalidades
Modelagem do armazém como grafo: nós representam pontos de coleta (áreas de picking) e os vértices, as conexões com pesos (distâncias).

Geração aleatória de pedidos: cada lote contém de 3 a 5 pedidos, com 1 a 2 itens por pedido, selecionados aleatoriamente.

Cálculo automático de rota:

Uso do algoritmo de Dijkstra para encontrar subcaminhos ótimos entre vértices.

Permuta de combinações de vértices (via itertools) para definir a sequência de coleta que minimize o custo total.

Interface gráfica (GUI):

Tkinter: cria janelas, botões e canvas para exibir pedidos e permitir interações.

NetworkX + Matplotlib + FigureCanvasTkAgg: desenha o grafo do armazém dentro da janela do Tkinter e destaca a rota resultante.

Demonstração de cores:

Arestas exclusivas da rota em vermelho sólido.

Arestas repetidas (ida e volta) em roxo sólido.

Nós de picking em laranja.

Início do percurso (Entrada) em verde e final (Saída) em azul.

Exibição dinâmica de pedidos: todos os pedidos do lote são listados horizontalmente em um Canvas rolável, mantendo a sequência de criação.

Responsividade da interface: ajustes para que componentes se redimensionem, mantendo legibilidade e posicionamento correto dos nós ao redimensionar a janela.

Logs de custo total: ao calcular a rota, exibe na interface (próximo ao grafo) o custo total (soma de todos os pesos percorridos).

🛠 Tecnologias e Bibliotecas Utilizadas
Linguagem de Programação: Python 3.8+

Interface Gráfica:

tkinter

FigureCanvasTkAgg (para integrar gráficos Matplotlib)

Manipulação de Grafos: networkx

Plotagem de Grafos: matplotlib

Estruturas de Dados e Funções Auxiliares:

heapq (fila de prioridade para Dijkstra)

itertools (geração de permutações/combinações de nós)

copy (para duplicar grafos sem alterar o original)

random (para seleção aleatória de itens/pedidos)
