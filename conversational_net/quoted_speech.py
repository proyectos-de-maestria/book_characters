from conversational_net.string_utils import split_in_quotes, get_sentences_before_quote


def get_conversational_graph(text):
    quotes = split_in_quotes(text)
    # result = re.findall(r"“([^”]*)”", rd)
    print(quotes)
    print()
    print()
    sentences = get_sentences_before_quote(text, quotes)
    for s in sentences:
        print("----------")
        print(s)
    print(len(sentences) == len(quotes))


if __name__ == '__main__':
    t = open("../books/pride and prejudice extract.txt", encoding="utf8")
    rd = t.read()
    # print(rd)
    get_conversational_graph(rd)
