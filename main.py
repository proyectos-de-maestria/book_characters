from os import path

from conversational_net.quoted_speech import get_conversational_graph
from base_code.graph import save_graph, load_graph
from base_code import graph_measures


def build_conversational_graph(book_name, book_folder="books/"):
    t = open(book_folder + book_name + ".txt", encoding="utf8")
    rd = t.read()

    return get_conversational_graph(rd)


def main_characters(graph):
    ord_degree = graph_measures.top_n_degree(graph)
    max_degree = ord_degree[0][1]
    ord_degree = [(name, degree/max_degree) for name, degree in ord_degree if degree/max_degree >= 0.5]
    return ord_degree


if __name__ == "__main__":
    book = "Dracula"
    graphs_folder = "conversational_net/graphs/conv_"
    graph_path = graphs_folder + book
    if path.exists(graph_path + ".gml"):
        c_graph = load_graph(graph_path)
    else:
        c_raph = build_conversational_graph(book)
        save_graph(c_raph, graph_path)

    stars = main_characters(c_graph)
    for n in stars:
        print(n)
