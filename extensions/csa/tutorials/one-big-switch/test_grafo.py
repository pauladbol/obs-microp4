from collections import defaultdict

class Grafo(object):

    def __init__(self, arestas, direcionado=False):
        self.adj = defaultdict(set)
        self.direcionado = direcionado
        self.adiciona_arestas(arestas)


    def get_vertices(self):
        return list(self.adj.keys())


    def get_arestas(self):
        return [(k, v) for k in self.adj.keys() for v in self.adj[k]]


    def adiciona_arestas(self, arestas):
        for u, v in arestas:
            self.adiciona_arco(u, v)


    def adiciona_arco(self, u, v):
        self.adj[u].add(v)
        if not self.direcionado:
            self.adj[v].add(u)


    def existe_aresta(self, u, v):
        return u in self.adj and v in self.adj[u]

    def get_dependencias(self, v):
        dependencias = set()
        for vt in self.adj:
            if v in self.adj[vt]:
                dependencias.add(vt)
        return dependencias


    def __len__(self):
        return len(self.adj)


    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self.adj))


    def __getitem__(self, v):
        return self.adj[v]


arestas = [('ethernet', 'ipv4'), ('ethernet', 'ipv6'), ('ipv4', ''), ('ipv6', '')]

grafo = Grafo(arestas, direcionado=True)
print("adj " + str(grafo.adj))
print(" arestas " + str(grafo.get_arestas()))
print(" vertices " + str(grafo.get_vertices()))
print(" dependencias " + str(grafo.get_dependencias('ipv4')))

# def ord_topo(grafo):


# def ordenacao_topologica(grafo):
#     tempo = 0
#     def dfs_recursiva(grafo, vertice, tempo):
#         visitados.add(vertice)
#         for vizinho in grafo[vertice]:
#             if vizinho not in visitados:
#                 dfs_recursiva(grafo, vizinho)
#         tempo += 1
#         ordem_topologica[vertice] = tempo

#     visitados = set()
#     ordem_topologica = [0] * len(grafo)
    
#     for vertice in grafo:
#         if not vertice in visitados:
#             dfs_recursiva(grafo, vertice, tempo)
#     ordem_topologica.reverse()
    # return ordem_topologica

# grafo2 = [
#     [1, 2],
# ]

# ordem = ordenacao_topologica(grafo)
# print(ordem)