from conversational_net.quotes_utils import split_in_pairs
from base_code.preprocessing import names_in_text
from base_code.graph import *
from text_segmentation.epub_utils import save_text
import codecs


class ConversationalGraph(GraphHelper):

    def __init__(self, text, graph_path):
        super().__init__(text, graph_path)
        self.conversation_names, self.no_talk_names = self.__talk_ntalk_names__()
        self.build_graph()

    def __talk_ntalk_names__(self):
        full_talks = split_in_pairs(self.text)
        # names that are mentioned in the conversation
        conversation_names = []
        # names that are mentioned out of the conversation.
        # These most be the ones involved in th dialog.
        no_talk_names = []
        for talk, no_talk in full_talks:
            tn = names_in_text(talk)
            ntn = names_in_text(no_talk)
            all_names = list(tn.keys())
            all_names.extend(ntn.keys())
            sc = self.correferent.remove_correferents(tn, all_names)
            scn = self.correferent.remove_correferents(ntn, all_names)
            conversation_names.append(sc)
            no_talk_names.append(scn)
        return conversation_names, no_talk_names

    def build_graph(self):
        self.graph = nx.Graph()
        for names in self.no_talk_names:
            add_kn(self.graph, names)
        for i in range(len(self.conversation_names)):
            for name in self.conversation_names[i]:
                connect_n_to_nodes(self.graph, self.no_talk_names[i], name)

        return self.graph.to_undirected()

    def build_evolution_graph(self):
        self.evol_graphs = []

        times_to_build = len(self.conversation_names) // self.evol_number

        graph = nx.Graph()
        for i in range(len(self.conversation_names)):
            add_kn(graph, self.no_talk_names[i])
            for name in self.conversation_names[i]:
                connect_n_to_nodes(graph, self.no_talk_names[i], name)
            if i % times_to_build == 0 and i != 0:
                self.evol_graphs.append(graph.copy())
        self.evol_graphs.append(graph.copy())
        return self.evol_graphs


def get_graph(book_path, graph_path="graph"):
    t = open(book_path + ".txt", encoding="utf8")
    rd = t.read()

    return ConversationalGraph(rd, graph_path)


def get_graph_from_file(file):
    book_path = file.name
    print(book_path)
    if file.name.endswith("epub"):
        save_text(book_path, file)
    else:
        filed = codecs.open(book_path, "w", "utf-8")
        text = file.read().decode("utf-8")
        filed.write(text)
        filed.close()
    return get_graph(book_path)


if __name__ == '__main__':
    # book_name = "pride and prejudice extract"
    # book_name = "pride and prejudice"
    book = "Dracula"

    # graph = get_graph(book)
    # graph.save_graph()
    # save_graph(graph, graph_name)
    # paint_graph(graph, graph_name)
