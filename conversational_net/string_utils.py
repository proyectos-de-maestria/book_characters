import re


def split_in_quotes(text):
    quotes = re.findall(r"“([^”]*)”", text)
    return quotes


def split_in_sentences(text):
    # sentences that end in a dot
    return re.findall("([^.]*)[.]", text)


def get_sentences_before_quote(text, quotes):
    all_sentences = []

    q_index = text.find(quotes[0])
    if q_index == -1:
        print("First quote does not exist")
        return
    sentences_before = split_in_sentences(text[:q_index])
    all_sentences.append(clean(sentences_before[-1]))
    # print(all_sentences[0])

    q_index += len(quotes[0])          # sum len to get starting position of text before quote
    for i in range(1, len(quotes)):
        next_quote_index = text[q_index:].find(quotes[i])
        if next_quote_index == -1:
            print(str(i) + " quote does not exist")
            return []
        next_quote_index += q_index       # plus q_index cause is the start of the search
        seq_len = next_quote_index - q_index
        # if seq_len is bigger than 100 then the quotes are not related
        if seq_len <= 0 or seq_len > 100:
            all_sentences.append([])
        else:
            sentence = clean(text[q_index:next_quote_index])
            if is_empty(sentence):
                sentence = []
            all_sentences.append(sentence)
        q_index = next_quote_index + len(quotes[i])

    return all_sentences


def is_empty(s):
    return re.fullmatch("[ \n“”]*", s) is not None


def clean(s):
    search_tuple = (" ", "“", "”")
    if is_empty(s):
        return s
    if s.startswith(search_tuple):
        return clean(s[1:])
    if '\n' in s:
        return clean(s.replace("\n", " "))
    if s.endswith(search_tuple):
        return clean(s[:len(s)-1])
    return s
