from conversational_net.quotes_utils import split_in_full_conversation
from base_code.preprocessing import names_in_text
from base_code.graph import *


def get_conversational_graph(text, graph_name):
    full_talks = split_in_full_conversation(text)
    for i in full_talks:
        print("----------")
        print(i)
    conv_names = []
    for talk in full_talks:
        conv_names.append(names_in_text(talk))

    graph = nx.Graph()
    for names in conv_names:
        add_nodes(graph, names)

    save_graph(graph, graph_name)
    paint_graph(graph, graph_name)
    return graph


if __name__ == '__main__':
    book_name = "pride and prejudice extract"
    t = open("../books/" + book_name + ".txt", encoding="utf8")
    rd = t.read()

    get_conversational_graph(rd, "./graphs/conv_" + book_name)
