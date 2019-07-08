import networkx as nx
from networkx.readwrite import gml
import matplotlib.pyplot as plt
from collections import Counter

from base_code.correferents import Correferents


def add_kn(graph, nodes):
    nodes = Counter(nodes)
    if len(nodes.keys()) > 1:
        add_nodes_to_graph(nodes, graph)

        names = nodes.keys()
        edges_kn = [(x, y) for x in names for y in names if x != y]

        graph.add_edges_from(edges_kn, color='red')


def add_nodes_to_graph(nodes, graph):
    for name, count in nodes.items():
        node_count = (graph.node[name]['count'] if name in graph else 1) + count
        graph.add_node(name, count=node_count)


def connect_n_to_nodes(graph, nodes, n):
    nodes = Counter(nodes)

    names = nodes.keys()
    edges = [(x, n) for x in names if x != n]

    if len(edges):          # only add it to the graph if there is at least one edge
        node_count = graph.node[n]['count'] if n in graph else 1
        graph.add_node(n, count=node_count)
        add_nodes_to_graph(nodes, graph)

        graph.add_edges_from(edges, color='red')


def add_nodes_by_distance(graph, nodes, node):
    nodes[node] = 1
    nodes = Counter(nodes)

    names = nodes.keys()
    edges = [(node, x, 1 + graph.edges[node, x]['weight']) if graph.has_edge(node, x) else (node, x, 1) for x in names
             if node != x]
    if len(edges):
        for name, count in nodes.items():
            node_count = (graph.node[name]['count'] if name in graph else 0) + count
            graph.add_node(name, count=node_count)

    graph.add_weighted_edges_from(edges)


def paint_graph(graph, name):
    pos = nx.circular_layout(graph)
    # pos = nx.spring_layout(graph, k=0.70,iterations=20)
    # nodes
    nx.draw_networkx_nodes(graph, pos, node_size=150, alpha=0.8)
    # edges
    nx.draw_networkx_edges(graph, pos)

    labels = {}
    for node in graph.node.keys():
        labels[node] = node
    nx.draw_networkx_labels(graph, pos, labels, font_size=8, font_color='red', font_weight='bold')

    plt.axis('off')
    plt.savefig(name + ".png")        # save as png
    plt.show()


def save_graph(graph, name):
    gml.write_gml(graph, name + ".gml")


def load_graph(name):
    return gml.read_gml(name + ".gml")


class GraphHelper:

    def __init__(self, book_path, graph_path, text, evol_number=10):
        self.book_path = book_path
        # text = open(book_path + ".txt", encoding="utf8")
        # self.text = text.read( )
        self.text = text
        self.path = graph_path
        self.correferent = Correferents(self.text)
        self.graph = None
        self.evol_graphs = []
        self.evol_number = evol_number

    def build_graph(self):
        pass

    def build_evolution_graph(self):
        pass

    def save_graph(self):
        save_graph(self.graph, self.path)

    def load_graph(self):
        self.graph = load_graph(self.path)
