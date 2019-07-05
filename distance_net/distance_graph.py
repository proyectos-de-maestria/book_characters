from base_code.preprocessing import get_names_by_chapters, names_in_text
from base_code.graph import *
from base_code.correferents import Correferents
from text_segmentation import epub_utils
from ebooklib import epub


def get_distance_graph(book, graph_name, distance):
    text = epub_utils.get_text(book)
    cor = Correferents(text)

    chapters = epub_utils.chapter_contents(book)
    names_in_chapters = get_names_by_chapters(chapters)
    graph = nx.Graph()
    for ch in chapters.keys():
        chapter_content = chapters[ch]
        for name in names_in_chapters[ch]:
            name_index = chapter_content.find(name)
            portion_text = " ".join(chapter_content[name_index:].split( )[:distance])
            index = name_index - distance if name_index - distance > 0 else 0
            better_portion = " ".join(chapter_content[index:].split()[:distance])
            names_to_add = names_in_text(portion_text)
            names_correct = cor.remove_correferents(names_to_add, better_portion)
            add_nodes_by_distance(graph, names_correct, name)

    save_graph(graph, graph_name)
    paint_graph(graph, graph_name)
    return graph


path = '../books/Dracula.epub'
book = epub.read_epub(path)
get_distance_graph(book, path, 100)
epub_utils.save_text(path, book)
# circular_tree(graph)
