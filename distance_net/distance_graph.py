from base_code.preprocessing import get_names_by_chapters, names_in_text
from base_code.graph import *
from text_segmentation import epub_utils
from ebooklib import epub


class DistanceGraph(GraphHelper):

    def __init__(self, book_path, graph_path, distance):
        self.book_path = book_path
        self.book = epub.read_epub(self.book_path)
        text = epub_utils.get_text(self.book)
        super( ).__init__(book_path, graph_path, text)
        self.distance = distance
        self.distance_partition = self.__get_names_by_portion__()

    def __get_names_by_portion__(self):
        chapters = epub_utils.chapter_contents(self.book)
        names_in_chapters = get_names_by_chapters(chapters)
        distance_partition = []
        for ch in chapters.keys( ):
            chapter_content = chapters[ch]
            for name in names_in_chapters[ch]:
                name_index = chapter_content.find(name)
                portion_text = " ".join(chapter_content[name_index:].split( )[:self.distance])
                index = name_index - self.distance if name_index - self.distance > 0 else 0
                better_portion = " ".join(chapter_content[index:].split()[:self.distance])
                names_in_portion = names_in_text(portion_text)
                names_correct = self.correferent.remove_correferents(names_in_portion, better_portion)
                distance_partition.append((name, names_correct))
        return distance_partition

    def build_evolution_graph(self):
        self.evol_graphs = []
        times_to_build = len(self.distance_partition) // self.evol_number
        graph = nx.Graph( )

        for i in range(len(self.distance_partition)):
            add_nodes_by_distance(graph, self.distance_partition[i][1], self.distance_partition[i][0])
            if i % times_to_build == 0 and i != 0:
                self.evol_graphs.append(graph.copy( ))
        self.evol_graphs.append(graph.copy( ))

        return self.evol_graphs

    def build_graph(self):
        self.graph = nx.Graph( )
        names_to_add = self.__get_names_by_portion__()
        for name, names_correct in names_to_add:
            add_nodes_by_distance(self.graph, names_correct, name)
        self.save_graph()
        return self.graph

#
# def get_distance_graph(book_path, distance, graph_path="graph"):
#     return DistanceGraph(book, graph_path, distance)

#
# #
# path = '../books/Dracula.epub'
# book = epub.read_epub(path)
# graph = DistanceGraph(book, path, 100)
# graph = graph.build_graph( )
# # circular_tree(graph)
