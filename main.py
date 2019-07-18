from os import path

from base_code import graph_measures
from base_code.utils import *
from distance_net.distance_graph import *
from conversational_net.quoted_speech import *


def main_characters(graph):
    ord_degree = graph_measures.top_n_degree(graph)
    if len(ord_degree):
        max_degree = ord_degree[0][1]
        ord_degree = [(name, degree / max_degree) for name, degree in ord_degree if degree / max_degree >= 0.5]
    return ord_degree


def build_graph(graph_helper):
    if graph_helper:
        return graph_helper.build_graph()


def build_evolution(graph_helper, try_load=True):
    filename = graph_helper.path + 'evol.pkl'
    if try_load and path.exists(filename):
        evol = list(pickled_items(filename))[0]["1"]
    else:
        evol = graph_helper.build_evolution_graph()

        save_object(filename, {"1": evol})
    return [main_characters(x) for x in evol]


def character_sustitution(graph, name):
    return sustitution_node(graph, name)


def main():
    print("Introduzca los comandos de consulta:")
    graph = None
    while True:
        print()
        str_comando = input(">> ")
        comando = str_comando.split(' ')
        if len(comando):
            if comando[0] == "book" and len(comando) > 1:
                book_path = text_in_fquote(str_comando)
                if path.exists(book_path):
                    print("inicializando datos...")
                    book_without_extension = ''.join(path.split(book_path)[1].split('.')[:-1])
                    print(book_without_extension)
                    if len(comando) > 2 and comando[-1] == "dist":
                        if not book_path.endswith(".epub"):
                            print("para el grafo de distancias es necesario un epub")
                            graph = None
                        else:
                            graph = DistanceGraph(book_path, 'distance_net/graph' + book_without_extension, distance=15)
                    else:
                        if book_path.endswith(".epub"):
                            file = epub.read_epub(book_path)
                            save_text(book_path, file)
                            book_path = book_path.replace(".epub", ".txt")
                        graph = ConversationalGraph(book_path,
                                                    'conversational_net/graphs/conv_' + book_without_extension)
                    build_graph(graph)
                else:
                    print("archivo no encontrado")
            elif comando[0] == "exit":
                break
            elif comando[0] == "help":
                ayuda()
            elif graph:
                if comando[0] == "stars":
                    stars = main_characters(graph.graph)
                    if len(comando) > 1:
                        if comando[1] == 'pr':      # page rank
                            pass        # TODO
                        if comando[1] == 'center':
                            stars = graph_measures.center(graph.graph)
                        if comando[1] == 'btwn':
                            stars = graph_measures.top_n_betweenness(graph.graph)
                            stars = [s for s, v in stars if float(v) > 0.5]
                    for star in stars:
                        print(star)
                elif comando[0] == 'evol':
                    main_evol = build_evolution(graph)
                    data = transform_evol_list_in_dict(main_evol)
                    bar_graph(data)
                elif comando[0] == 'cluster':
                    paint_communities(graph.graph)
                    graph.save_graph()
                    print("guardado el grafo con las comunidades en " + graph.path + ".gml")
                elif comando[0] == 'sustituir':
                    while True:
                        print("-- elegir personaje:")
                        per = input("-- ")
                        if per == 'exit':
                            break
                        if per in graph.graph.nodes():
                            print("sustituto de {0} -> {1}".format(per, character_sustitution(graph.graph, per)))
                        else:
                            pos = [x for x in graph.graph.nodes() if x.startswith(per) or x.lower().startswith(per)]
                            if len(pos):
                                print("quizas quisiste decir: " + str(pos))
                elif comando[0] == "salvar":
                    graph.save_graph()
                elif comando[0] == "relacion":
                    while True:
                        print("-- elegir primer personaje:")
                        per = input("-- ")
                        if per == 'exit':
                            break
                        if per in graph.graph.nodes():
                            print("-- elegir segundo personaje:")
                            per2 = input("-- ")
                            if per2 == 'exit':
                                break
                            if per2 in graph.graph.nodes():
                                rel = int(get_relation_type(graph.graph, per, per2))
                                print("relacion de {0} y {1} es {2}".
                                      format(per, per2, "negativa" if rel < 0 else "positiva" if rel > 0 else "neutra"))
                            else:
                                pos = [x for x in graph.graph.nodes() if x.startswith(per2) or x.lower().startswith(per2)]
                                if len(pos):
                                    print("quizas quisiste decir: " + str(pos))
                        else:
                            pos = [x for x in graph.graph.nodes() if x.startswith(per) or x.lower().startswith(per)]
                            if len(pos):
                                print("quizas quisiste decir: " + str(pos))
                    pass
                elif comando[0] == "tramas":
                    graph_path = text_in_fquote(str_comando)
                    if path.exists(graph_path) and graph_path.endswith(".gml"):
                        book2 = load_graph(graph_path)
                        sim_topics = get_similar_topics(graph.graph, book2)
                        for i, (g1, g2) in enumerate(sim_topics):
                            save_graph(g1, "{0}result1.gml".format(i))
                            save_graph(g2, "{0}result2.gml".format(i))
                            print("salvados resultados para trama {0}".format(i))
                    else:
                        print("archivo no encontrado. Debe tener extension gml")
            else:
                print("se debe cargar primero un libro con el comando book <path>")


if __name__ == "__main__":
    main()
    test = "books/pride and prejudice extract.txt"
    trama = "conversational_net/graphs/conv_Dracula.gml"
    # print(path.exists(test))
    # book = "Dracula"
    # # book = "pride and prejudice extract"
    # book_path = "books/" + book

    # file = codecs.open(book_path + ".txt", 'r', "utf-8")
    # b = run_main(file)
    # a = 0

    # graphs_folder = "conversational_net/graphs/conv_"
    # graph_path = graphs_folder + book
    # graph_path2 = graphs_folder + "pride and prejudice"
    # a = similar_topic(graph_path, graph_path2)
    # if len(a):
    #     for elem in a:
    #         print(elem[0])
    #         print(elem[1])
    #         print("-----------------s")
    # else:
    #     print("nada")

    # graph_path_distance = "distance_net/graph" + book
    # graph = load_graph(graph_path)
    # graph_measures.paint_communities(graph)
    # save_graph(graph, graph_path)
    # # cg = ConversationalGraph(book_path, graph_path)
    # # dg = DistanceGraph(book_path, graph_path_distance, distance=100)
    # graph = load_graph(graph_path)
    # # cg.build_graph()

    # print(get_relation_type(graph, 'Jonathan Harker', 'Jonathan'))
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
