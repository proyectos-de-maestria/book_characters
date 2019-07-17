import networkx as nx
from operator import itemgetter
import community


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


def center(graph):
    components = max(nx.connected_components(graph))
    return nx.algorithms.center(graph.subgraph(components))


def paint_communities(graph, paint=True):
    communities = community.best_partition(graph)
    if paint:
        size = float(len(set(communities.values())))
        count = 0
        for com in set(communities.values()):
            count = count + 1.
            list_nodes = [nodes for nodes in communities.keys()
                          if communities[nodes] == com]
            for node in list_nodes:
                # graph.add_node(node, com_color=count/size)
                graph.nodes[node]['color'] = count / size

    return communities
