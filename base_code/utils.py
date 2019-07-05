import pickle


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
