import networkx as nx
from networkx.readwrite import gml
import matplotlib.pyplot as plt
from collections import Counter
from networkx.algorithms import community
import community

from base_code.correferents import Correferents


def add_kn(graph, nodes):
    nodes = Counter(nodes)
    if len(nodes.keys( )) > 1:
        add_nodes_to_graph(nodes, graph)

        names = nodes.keys( )
        edges_kn = [(x, y) for x in names for y in names if x != y]

        graph.add_edges_from(edges_kn, color='red')


def add_nodes_to_graph(nodes, graph):
    for name, count in nodes.items( ):
        node_count = (graph.node[name]['count'] if name in graph else 1) + count
        graph.add_node(name, count=node_count)


def connect_n_to_nodes(graph, nodes, n):
    nodes = Counter(nodes)

    names = nodes.keys( )
    edges = [(x, n) for x in names if x != n]

    if len(edges):  # only add it to the graph if there is at least one edge
        node_count = graph.node[n]['count'] if n in graph else 1
        graph.add_node(n, count=node_count)
        add_nodes_to_graph(nodes, graph)

        graph.add_edges_from(edges, color='red')


def add_nodes_by_distance(graph, nodes, node, classiffication):
    nodes[node] = 1
    nodes = Counter(nodes)

    names = nodes.keys( )
    edges = [(node, x, {'weight': 1 + graph.edges[node, x]['weight'], 'class': classiffication + graph.edges[node, x]['class']})
             if graph.has_edge(node, x) else (node, x,  {'weight': 1, 'class': classiffication})
             for x in names if node != x]
    if len(edges):
        for name, count in nodes.items( ):
            node_count = (graph.node[name]['count'] if name in graph else 0) + count
            graph.add_node(name, count=node_count)

    graph.update(edges=edges)
    # graph.add_weighted_edges_from(edges)



def get_common_neighbors(node_a, node_b, graph):
    return nx.common_neighbors(graph, node_a, node_b)


def paint_graph(graph, name):
    pos = nx.circular_layout(graph)
    # pos = nx.spring_layout(graph, k=0.70,iterations=20)
    # nodes
    nx.draw_networkx_nodes(graph, pos, node_size=150, alpha=0.8)
    # edges
    nx.draw_networkx_edges(graph, pos)

    labels = {}
    for node in graph.node.keys( ):
        labels[node] = node
    nx.draw_networkx_labels(graph, pos, labels, font_size=8, font_color='red', font_weight='bold')

    plt.axis('off')
    plt.savefig(name + ".png")  # save as png
    plt.show( )


def get_communities(graph, modularity=False, fluid=False):
    k = len([key for key in graph.node.keys( )]) / 10
    if modularity:
        return community.greedy_modularity_communities(graph)
    if fluid:
        return community.asyn_fluidc(graph, k)
    else:  # how work
        return community.girvan_newman(graph)


def get_partitions(communities):
    result = {}
    for key in communities.keys( ):
        value = communities[key]
        if value in result.keys( ):
            result[value].append(key)
        else:
            result[value] = [key]
    return result


def sustitution_node(graph, name):
    neighbors_name = [i for (i, j) in graph.adj[name].items( )]
    min = len(graph.node.keys( ))
    result = 'No hay'
    for node in graph.node.keys( ):

        neighbors_node = [i for (i, j) in graph.adj[node].items( )]
        dif = [a for a in neighbors_name if a not in neighbors_node]
        dif.extend([a for a in neighbors_node if a not in neighbors_name])
        neighbors_node.extend(neighbors_name)
        total = len(set(neighbors_node))
        if len(dif) < min and name != node and len(dif) / total < 0.5:
            min = len(dif)
            result = node
    return result


def relation_types(graph):
    relations = {}

    for (u, v, d) in graph.edges(data='weight'):
        relations[u] = d if u not in relations.keys() else relations[u] + d
        relations[v] = d if v not in relations.keys() else relations[v] + d


    for (u, v, d) in graph.edges(data='weight'):
        relation_value = d/(relations[u]+relations[v])
        # if relation_value > 0.4:
        print(u, 'related with', v, relation_value)


def get_similar_topics(graph_1, graph_2):
    pass


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

    def load_graph_as_file(self):
        self.save_graph( )
        return open(self.path + ".gml", 'r')
