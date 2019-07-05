from os import path

from conversational_net.quoted_speech import get_conversational_graph, evolution_talk_graph
from base_code.graph import save_graph, load_graph
from base_code import graph_measures
from base_code.utils import *


def build_conversational_graph(book_name, book_folder="books/"):
    t = open(book_folder + book_name + ".txt", encoding="utf8")
    rd = t.read()

    return get_conversational_graph(rd)


def main_characters(graph):
    ord_degree = graph_measures.top_n_degree(graph)
    if len(ord_degree):
        max_degree = ord_degree[0][1]
        ord_degree = [(name, degree/max_degree) for name, degree in ord_degree if degree/max_degree >= 0.5]
    return ord_degree


def build_evolution_conv(book_name, book_folder="books/", try_load=True):
    filename = 'evol_graph.pkl'
    if try_load and path.exists(filename):
        evol = list(pickled_items(filename))[0]["1"]
    else:
        t = open(book_folder + book_name + ".txt", encoding="utf8")
        rd = t.read()

        evol = evolution_talk_graph(rd)

        save_object(filename, {"1": evol})
    return [main_characters(x) for x in evol]


if __name__ == "__main__":
    book = "Dracula"
    graphs_folder = "conversational_net/graphs/conv_"
    graph_path = graphs_folder + book
    if path.exists(graph_path + ".gml"):
        c_graph = load_graph(graph_path)
    else:
        c_raph = build_conversational_graph(book)
        save_graph(c_raph, graph_path)

    # stars = main_characters(c_graph)
    # for n in stars:
    #     print(n)

    main_evol = build_evolution_conv(book)
    data = transform_evol_list_in_dict(main_evol)
    bar_graph(data)
