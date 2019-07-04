from conversational_net.quotes_utils import split_in_pairs
from base_code.preprocessing import names_in_text
from base_code.graph import *
from base_code.correferents import Correferents


def get_conversational_graph(text):
    full_talks = split_in_pairs(text)

    # names that are mentioned in the conversation
    conversation_names = []
    # names that are mentioned out of the conversation.
    # These most be the ones involved in th dialog.
    no_talk_names = []
    cor = Correferents(text)
    for talk, no_talk in full_talks:
        tn = names_in_text(talk)
        ntn = names_in_text(no_talk)
        all_names = list(tn.keys())
        all_names.extend(ntn.keys())
        sc = cor.remove_correferents(tn, all_names)
        scn = cor.remove_correferents(ntn, all_names)
        conversation_names.append(sc)
        no_talk_names.append(scn)

    graph = nx.Graph()
    for names in no_talk_names:
        add_kn(graph, names)

    for i in range(len(conversation_names)):
        for name in conversation_names[i]:
            connect_n_to_nodes(graph, no_talk_names[i], name)

    return graph.to_undirected()


if __name__ == '__main__':
    # book_name = "pride and prejudice extract"
    # book_name = "pride and prejudice"
    book_name = "Dracula"
    t = open("../books/" + book_name + ".txt", encoding="utf8")
    rd = t.read()

    graph_name = "./graphs/conv_" + book_name
    graph = get_conversational_graph(rd)
    save_graph(graph, graph_name)
    # paint_graph(graph, graph_name)
