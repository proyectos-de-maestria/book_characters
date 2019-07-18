from conversational_net.quotes_utils import split_in_pairs
from base_code.preprocessing import names_in_text
from base_code.graph import *
from text_segmentation.epub_utils import save_text
from base_code.utils import write_file
from ebooklib import epub


class ConversationalGraph(GraphHelper):
    def __init__(self, book_path, graph_path):
        if not book_path.endswith(".txt"):
            book_path += ".txt"
        text = open(book_path, encoding="utf8").read()
        super().__init__(book_path, graph_path, text)
        self.conversation_names, self.no_talk_names, self.sentiments = self.__talk_ntalk_names__()
        # self.build_graph()

    def __talk_ntalk_names__(self):
        full_talks = split_in_pairs(self.text)
        # names that are mentioned in the conversation
        conversation_names = []
        # names that are mentioned out of the conversation.
        # These most be the ones involved in th dialog.
        no_talk_names = []
        # sentiment in conversation
        sentiments = []
        for talk, no_talk, sentiment in full_talks:
            tn = names_in_text(talk)
            ntn = names_in_text(no_talk)
            all_names = list(tn.keys())
            all_names.extend(ntn.keys())
            sc = self.correferent.remove_correferents(tn, all_names)
            scn = self.correferent.remove_correferents(ntn, all_names)
            conversation_names.append(sc)
            no_talk_names.append(scn)
            sentiments.append(sentiment)
        return conversation_names, no_talk_names, sentiments

    def build_graph(self):
        self.graph = nx.Graph()
        for i, names in enumerate(self.no_talk_names):
            add_kn(self.graph, names, self.sentiments[i])
        for i in range(len(self.conversation_names)):
            for name in self.conversation_names[i]:
                connect_n_to_nodes(self.graph, self.no_talk_names[i], name, self.sentiments[i])
        self.save_graph()
        return self.graph.to_undirected()

    def build_evolution_graph(self):
        self.evol_graphs = []

        times_to_build = len(self.conversation_names) // self.evol_number + 1           # avoiding zero

        graph = nx.Graph()
        for i in range(len(self.conversation_names)):
            add_kn(graph, self.no_talk_names[i], self.sentiments[i])
            for name in self.conversation_names[i]:
                connect_n_to_nodes(graph, self.no_talk_names[i], name, self.sentiments[i])
            if i % times_to_build == 0 and i != 0:
                self.evol_graphs.append(graph.copy())
        self.evol_graphs.append(graph.copy())
        return self.evol_graphs


def get_graph(book_path, graph_path="graph"):
    if not book_path.endswith(".txt"):
        book_path += ".txt"
    graph = ConversationalGraph(book_path, graph_path)
    graph.build_graph()
    return graph


def get_graph_from_file(file):
    book_path = file.name.split("/")[-1]
    print(book_path)
    if file.name.endswith("epub"):
        write_file(file, book_path)
        # epub.write_epub(book_path, file)
        file = epub.read_epub(book_path)
        save_text(book_path, file)
    else:
        write_file(file, book_path)
        # filed = codecs.open(book_path, "w", "utf-8")
        # text = file.read()
        # text = text if isinstance(text, str) else text.decode("utf-8")
        # filed.write(text)
        # filed.close()
    return get_graph(book_path)


if __name__ == '__main__':
    # book_name = "pride and prejudice extract"
    # book_name = "pride and prejudice"
    book = "Dracula"

    # graph = get_graph(book)
    # graph.save_graph()
    # save_graph(graph, graph_name)
    # paint_graph(graph, graph_name)
