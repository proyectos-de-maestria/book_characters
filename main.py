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


def character_sustitution(graph, name):
    return sustitution_node(graph, name)


def run_main(file, grap_type='cv'):
    data = {}

    graph = get_graph_from_file(file) if grap_type == 'cv' \
        else get_graph_from_file(file)      # TODO cambiar el else a distance_net

    stars = main_characters(graph.graph)
    data['stars'] = stars

    sustitute = {}
    for node in graph.graph.nodes():
        sustitute[node] = character_sustitution(graph.graph, node)
    data['all_sustitutes'] = sustitute

    main_evol = build_evolution(graph, try_load=False)
    evol_data = transform_evol_list_in_dict(main_evol)
    p_name = bar_graph(evol_data)
    fd = open(p_name, "r") if p_name is not None else None
    data['evol'] = fd

    data['graph_file'] = graph.load_graph_as_file()

    return data


if __name__ == "__main__":
    book = "Dracula.epub"
    # book = "pride and prejudice extract"
    book_path = "books/" + book

    # file = codecs.open(book_path + ".txt", 'r', "utf-8")
    # b = run_main(file)
    # a = 0
    #


    graphs_folder = "conversational_net/graphs/distance_"
    graph_path = graphs_folder + book
    # graph_path_distance = "distance_net/graph" + book
    # graph = load_graph(graph_path)
    # graph_measures.paint_communities(graph)
    # save_graph(graph, graph_path)
    # # cg = ConversationalGraph(book_path, graph_path)
    # dg = DistanceGraph(book_path, graph_path, distance=30)
    graph = load_graph(graph_path)
    # # cg.build_graph()

    print(get_relation_type(graph, 'Jonathan Harker', 'Jonathan'))
    # # cg.load_graph()
    # print(sustitution_node(graph, 'Dracula'))
    # dg.load_graph()
    # stars = main_characters(dg.graph)
    # stars = main_characters(cg.graph)
    # for m in stars:
    #     print(m)
    # #
    # main_evol = build_evolution(cg)
    # data = transform_evol_list_in_dict(main_evol)
    # bar_graph(data)
