import re
from base_code.preprocessing import get_sentiment_classification


def split_in_quotes(text):
    quotes = re.findall(r"“([^”]*)”", text)
    quotes.extend(re.findall(r"\"([^\"]*)\"", text))
    return quotes


def split_in_sentences(text):
    # paragraphs are divided with \n
    paragraph = text.split("\n")
    if len(paragraph) and is_empty(paragraph[-1]):
        paragraph = paragraph[:-1]
    return paragraph
    # # sentences that end in a dot
    # return re.findall("([^.]*)[.]", text)


def get_sentences_before_quote(text, quotes):
    all_sentences = []

    if not len(quotes):
        return []
    q_index = text.find(quotes[0])
    if q_index == -1:
        print("First quote does not exist")
        return
    sentences_before = split_in_sentences(text[:q_index])
    info = {"quote": quotes[0],
            "before": clean(sentences_before[-1]) if len(sentences_before) else "",
            "after": -1}
    all_sentences.append(info)

    q_index += len(quotes[0])  # sum len to get starting position of text before quote
    for i in range(1, len(quotes)):
        next_quote_index = text[q_index:].find(quotes[i])
        if next_quote_index == -1:
            print(str(i) + " quote does not exist")
            return []
        next_quote_index += q_index  # plus q_index cause is the start of the search
        seq_len = next_quote_index - q_index
        sentence = clean(text[q_index:next_quote_index])
        # if seq_len is bigger than 100 then the quotes are not related
        if seq_len > 100:
            # there is no after for the old sentence
            sentences_before = split_in_sentences(sentence)
            info = {"quote": quotes[i],
                    "before": clean(sentences_before[-1]) if len(sentences_before) else "",
                    "after": -1}
            all_sentences.append(info)
        else:
            info = {"quote": quotes[i], "before": "" if is_empty(sentence) else sentence, "after": -1}
            all_sentences[-1]["after"] = "" if is_empty(sentence) else sentence
            all_sentences.append(info)
        q_index = next_quote_index + len(quotes[i])

    return all_sentences


def split_in_full_conversation(text):
    res = [""]
    quotes = split_in_quotes(text)
    sentences = get_sentences_before_quote(text, quotes)
    for sentence in sentences:
        res[-1] += sentence["before"] + "\n" + sentence["quote"] + "\n"
        if sentence["after"] == -1:  # to much space between two consecutive quotes
            res.append("")
    return res


def split_in_pairs(text):
    # get (dialog, non dialog) pairs from conversations that are close
    res = []
    quotes = split_in_quotes(text)
    sentences = get_sentences_before_quote(text, quotes)
    before = ""
    quote = ""
    full_conversation = ""
    for sentence in sentences:
        if sentence["before"] != "":
            before += sentence["before"] + "\n"
        quote += sentence["quote"] + "\n"
        full_conversation += sentence["before"] + "\n" + sentence["quote"] + "\n"
        if sentence["after"] == -1:  # to much space between two consecutive quotes
            classification = get_sentiment_classification(full_conversation)
            res.append((quote, before, classification))
            before = ""
            quote = ""
            full_conversation = ""
    return res


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
        return clean(s[:len(s) - 1])
    return s
