from base_code.preprocessing import get_names_by_chapters, names_in_text
from base_code.graph import *
from text_segmentation import epub_utils
from ebooklib import epub


def get_distance_graph(book, graph_name, distance):
    chapters = epub_utils.chapter_contents(book)
    names_in_chapters = get_names_by_chapters(chapters)
    graph = nx.Graph()
    for ch in chapters.keys():
        chapter_content = chapters[ch]
        for name in names_in_chapters[ch]:
            name_index = chapter_content.find(name)
            portion_text = " ".join(chapter_content.split()[name_index: name_index + distance])
            names_to_add = names_in_text(portion_text)
            add_nodes_by_distance(graph, names_to_add, name)

    save_graph(graph, graph_name)
    paint_graph(graph, graph_name)
    return graph


path = '../books/Dracula.epub'
book = epub.read_epub(path)
get_distance_graph(book, "distance_graph", 100)
epub_utils.save_text(path, book)
