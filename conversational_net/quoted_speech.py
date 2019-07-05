from conversational_net.quotes_utils import split_in_pairs
from base_code.preprocessing import names_in_text
from base_code.graph import *
from base_code.correferents import Correferents


def __talk_ntalk_names__(text):
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
    return conversation_names, no_talk_names


def get_conversational_graph(text):
    conversation_names, no_talk_names = __talk_ntalk_names__(text)

    graph = nx.Graph()
    for names in no_talk_names:
        add_kn(graph, names)
    for i in range(len(conversation_names)):
        for name in conversation_names[i]:
            connect_n_to_nodes(graph, no_talk_names[i], name)

    return graph.to_undirected()


def evolution_talk_graph(text, evol_number=10):
    graphs = []

    conversation_names, no_talk_names = __talk_ntalk_names__(text)
    times_to_build = len(conversation_names) // evol_number

    graph = nx.Graph()
    for i in range(len(conversation_names)):
        add_kn(graph, no_talk_names[i])
        for name in conversation_names[i]:
            connect_n_to_nodes(graph, no_talk_names[i], name)
        if i % times_to_build == 0 and i != 0:
            graphs.append(graph.copy())
    graphs.append(graph.copy())
    return graphs


if __name__ == '__main__':
    # book_name = "pride and prejudice extract"
    # book_name = "pride and prejudice"
    book_name = "Dracula"
    t = open("../books/" + book_name + ".txt", encoding="utf8")
    rd = t.read()

    graph_name = "./graphs/conv_" + book_name
    _graph = get_conversational_graph(rd)
    save_graph(_graph, graph_name)
    # paint_graph(graph, graph_name)
