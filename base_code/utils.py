import pickle
import matplotlib.pyplot as plt


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
        plt.show()
