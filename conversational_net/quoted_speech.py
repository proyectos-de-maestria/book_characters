from conversational_net.quotes_utils import split_in_pairs
from base_code.preprocessing import names_in_text
from base_code.graph import *
from base_code.correferents import Correferents


def get_conversational_graph(text, graph_name):
    full_talks = split_in_pairs(text)
    # for i in full_talks:
    #     print("----------")
    #     print(i[0])
    #     print("-- DOS --")
    #     print(i[1])

    conversation_names = []             # names that are mentioned in the conversation
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
        add_nodes(graph, names)

    for i in range(len(conversation_names)):
        for name in conversation_names[i]:
            connect_n_to_nodes(graph, no_talk_names[i], name)

    save_graph(graph, graph_name)
    paint_graph(graph, graph_name)
    return graph


if __name__ == '__main__':
    # book_name = "pride and prejudice extract"
    book_name = "pride and prejudice"
    t = open("../books/" + book_name + ".txt", encoding="utf8")
    rd = t.read()

    get_conversational_graph(rd, "./graphs/conv_" + book_name)
