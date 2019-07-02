import networkx as nx
from networkx.readwrite import gml
import matplotlib.pyplot as plt
from collections import Counter


def add_nodes(graph, nodes):
    nodes = Counter(nodes)

    for name, count in nodes.items():
        node_count = (graph.node[name]['count'] if name in graph else 0) + count
        graph.add_node(name, count=node_count)

    names = nodes.keys()
    edges_kn = [(x, y) for x in names for y in names if x != y]

    graph.add_edges_from(edges_kn, color='red')


def connect_n_to_nodes(graph, nodes, n):
    nodes = Counter(nodes)

    names = nodes.keys()
    edges = [(x, n) for x in names if x != n]

    if len(edges):          # only add it to the graph if there is at least one edge
        node_count = graph.node[n]['count'] if n in graph else 0
        graph.add_node(n, count=node_count)

        graph.add_edges_from(edges, color='red')


def add_nodes_by_distance(graph, nodes, node):
    nodes[node] = 1
    nodes = Counter(nodes)

    for name, count in nodes.items():
        node_count = (graph.node[name]['count'] if name in graph else 0) + count
        graph.add_node(name, count=node_count)

    names = nodes.keys()
    edges = [(node, x) for x in names]

    graph.add_edges_from(edges, color='red')


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
