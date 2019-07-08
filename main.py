from os import path
from base_code import graph_measures
from base_code.utils import *
from distance_net.distance_graph import *
from conversational_net.quoted_speech import *


# def build_conversational_graph(book_path, graph_path, distance):
#     return get_graph(book_path, graph_path)
#
#
# def build_distance_graph(book_path, graph_path, distance ):
#     return get_distance_graph(book_path, graph_path, distance)



def main_characters(graph):
    ord_degree = graph_measures.top_n_degree(graph)
    if len(ord_degree):
        max_degree = ord_degree[0][1]
        ord_degree = [(name, degree / max_degree) for name, degree in ord_degree if degree / max_degree >= 0.5]
    return ord_degree


def build_graph(graph_helper):
    return graph_helper.build_graph()


def build_evolution(graph_helper, try_load=True):
    filename = 'evol_graph.pkl'
    if try_load and path.exists(filename):
        evol = list(pickled_items(filename))[0]["1"]
    else:
        evol = graph_helper.build_evolution_graph()

        save_object(filename, {"1": evol})
    return [main_characters(x) for x in evol]


def run_main(file):
    data = {}
    graph = get_graph_from_file(file)
    stars = main_characters(graph.graph)
    data['stars'] = stars
    return data


if __name__ == "__main__":
    book = "Dracula"
    book = "pride and prejudice extract"
    book_path = "books/" + book
    graphs_folder = "conversational_net/graphs/conv_"
    graph_path = graphs_folder + book
    graph_path_distance = "distance_net/graph" + book
    # cg = ConversationalGraph(book_path, graph_path)
    dg = DistanceGraph(book_path, graph_path_distance, distance=100)

    # cg.build_graph()
    # dg.build_graph()
    dg.load_graph()
    stars = main_characters(dg.graph)
    for m in stars:
        print(m)
    #
    # main_evol = build_evolution(graph_)
    # data = transform_evol_list_in_dict(main_evol)
    # bar_graph(data)
