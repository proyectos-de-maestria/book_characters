import pickle
import matplotlib.pyplot as plt
from numpy import zeros
import codecs
import base64
import re


def pickled_items(filename):
    """ Unpickle a file of pickled data. """
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


def save_object(filename, object):
    with open(filename, 'wb') as gfile:
        pickle.dump(object, gfile)


def transform_evol_list_in_dict(main_evol):
    data = {}    # transform evolution in dictionary with name:evolution list
    for m in main_evol:
        for name, _ in m:
            data[name] = []
    for it, m in enumerate(main_evol):
        it += 1
        for name, norm_degree in m:
            data[name].append(norm_degree)
        # all list must have it size. If not, fill with 0
        for n in data.keys():
            if len(data[n]) < it:
                data[n].append(0)
    return data


def bar_graph(data):
    if len(data.keys()):
        fig_name = 'evol.png'
        start_x = 0
        for name in data.keys():
            x_list = [start_x + len(data.keys())*i for i in range(len(data[name]))]
            plt.bar(x_list, data[name], width=1, label=name)
            # plt.plot(x_list, data[name], label=name)
            start_x += 1

        # x = [len(data.keys())*i - 0.5 for i in range(len(data.keys()))]
        x = [len(data.keys())*i - 0.5 for i in range(len(data[name]))]
        ymin = [0]
        ymax = [0.2]
        plt.vlines(x, ymin, ymax, color='black', linewidth=2)

        plt.legend(loc='upper left')
        plt.ylabel('% de grado del nodo')
        plt.xlabel('evolución en el tiempo (las líneas negras son un nuevo segmento temporal)')
        plt.title("Evolución de los personajes")
        plt.savefig(fig_name)
        plt.show()
        return fig_name


def from_DtoD(com):
    res = {}
    for r, v in com.items():
        if v in res.keys():
            res[v].append(r)
        else:
            res[v] = [r]
    return res


def get_closest_ady(ady_sorted, num):
    if not len(ady_sorted):
        print("lista de adyacencia vacia")
        return -1, []
    if len(ady_sorted) == 1:
        return ady_sorted[0]
    if len(ady_sorted) == 2:
        return ady_sorted[0] if abs(len(ady_sorted[0][1]) - num) < abs(len(ady_sorted[1][1]) - num) else ady_sorted[1]
    split_index = len(ady_sorted)//2
    if abs(len(ady_sorted[split_index][1]) - num) < abs(len(ady_sorted[split_index + 1][1]) - num):
        return get_closest_ady(ady_sorted[:split_index + 1], num)
    else:
        return get_closest_ady(ady_sorted[split_index + 1:], num)


def hamming(matrix1, matrix2):
    max_matrix = matrix2
    min_matrix = matrix1
    if len(matrix1) > len(matrix2):
        max_matrix = matrix1
        min_matrix = matrix2
    z = zeros((len(max_matrix), len(max_matrix)))
    z[:len(min_matrix), :len(min_matrix)] = min_matrix
    # min_matrix = \
    #     csr_matrix((min_matrix.data, min_matrix.indices, min_matrix.indptr))
    return count_ones(abs(max_matrix - z))


def write_file(file, book_path):
    filed = codecs.open(book_path, "w")
    base64.decode(file, filed)
    # text = file.read()
    # text = text if isinstance(text, str) else base64.de text.decode("utf-8")
    # filed.write(text)
    print(file.read())
    filed.close()


def count_ones(matrix):
    ones = 0
    for row in matrix.A:
        for elem in row:
            if elem == 1:
                ones += 1
    return ones


def text_in_fquote(text):
    book_path = re.search("\"[^\"]*\"", text)
    if book_path:
        index = book_path.span()
        book_path = text[index[0] + 1:index[1] - 1]
    return book_path if book_path else "-"


def ayuda():
    print("inicializar los datos del libro usando el comando book <path>")
    print("<path> puede ser un path absoluto o relativo al proyecto. Debe ir entre comillas dobles.")
    print()
    print("se pueden consultar los datos del libro a traves de los comandos stars, evol, ")
    print("cluster, sustituir, relacion, tramas. Ademas, se puede guardar el gml del grafo ")
    print("haciendo uso del comando salvar. Para finalizar la ejecucion del programa, escribir exit.")
    print()
    print("-- stars: puede recibir como parametro el criterio para elegir los personajes principales. ")
    print("Por defecto, se calcula usando los grados de cada nodo. Parametros: ")
    print("<center> (centros del grafo),")
    print("<btwn> (betweenness de los nodos)")
    print()
    print("-- evol: calcula la evolucion de los personajes principales y muestra un grafico de barra con la progresion")
    print()
    print("-- cluster: agrega a los nodos del grafo un parametro community. El grafo se guarda en una direccion ")
    print("que se muestra y luego puede ser analizado haciendo uso de softwares como Gephi")
    print()
    print("-- sustituir: entra un nuevo prompt donde se espera el nombre de un personaje. Para cada entrada ")
    print("se computa su posible sustituto en la historia. Se puede volver al prompt original escribiendo exit")
    print()
    print("-- relacion: ")
    print()
    print("-- tramas: recibe como parametro la ruta de un archivo gml entre comillas. La extension debe estar ")
    print("inlcuida en el nombre. Calcula las tramas similares y guarda los resultados en archivos para su ")
    print("posterior analisis en Gephi.")
