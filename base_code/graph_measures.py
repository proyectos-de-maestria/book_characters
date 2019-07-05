import networkx as nx
from operator import itemgetter

from base_code.graph import load_graph


def top_n_degree(graph, n=10):
    degree_dict = dict(graph.degree(graph.nodes()))
    sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)
    return sorted_degree[:n]


def top_n_evcentrality(graph, n=10):
    centrality = nx.eigenvector_centrality(graph)
    sorted_ev = sorted(((v, '{:0.2f}'.format(c)) for v, c in centrality.items()), key=itemgetter(1), reverse=True)
    return sorted_ev[:n]


def top_n_betweenness(graph, n=10):
    betweenness_dict = nx.betweenness_centrality(graph)
    sorted_betweenness = sorted(((v, '{:0.2f}'.format(c)) for v, c in betweenness_dict.items()),
                                key=itemgetter(1), reverse=True)
    return sorted_betweenness[:n]


if __name__ == '__main__':
    graph_name = "Dracula.epub"
    graph = load_graph("../books/" + graph_name)
    graph = graph.to_undirected()
    print("Top 10 nodes by degree:")
    for n in top_n_degree(graph):
        print(n)

    print("------------------------------------------------------")
    print("Top 10 nodes by eigenvector centrality:")
    for n in top_n_evcentrality(graph):
        print(n)

    print("------------------------------------------------------")
    print("Top 10 nodes by betweenness centrality:")
    for n in top_n_betweenness(graph):
        print(n)
