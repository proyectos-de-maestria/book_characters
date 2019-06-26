from conversational_net.string_utils import split_in_full_conversation


def get_conversational_graph(text):
    full_talks = split_in_full_conversation(text)
    for i in full_talks:
        print("----------")
        print(i)


if __name__ == '__main__':
    t = open("../books/pride and prejudice extract.txt", encoding="utf8")
    rd = t.read()
    # print(rd)
    get_conversational_graph(rd)
