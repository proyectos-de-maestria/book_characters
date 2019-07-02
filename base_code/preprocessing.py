import en_core_web_sm


def spacy_names(text):
    res = {}
    step = 1000000
    if len(text) > step:
        nlp = en_core_web_sm.load()

        for i in range(step, len(text), step):
            doc = nlp(text[i - step:i])
            for entity in doc.ents:
                if entity.label_ == 'PERSON' or entity.label_ == 'NORP':
                    res[entity.lemma_] = 1 + (1 if res.__contains__(entity.lemma_) else 0)
                # print(entity.lemma_ + entity.label_)
    else:
        res = names_in_text(text)
    return res


def get_names_in_doc(doc):
    res = {}
    # get all possible names
    for entity in doc.ents:
        if entity.label_ == 'PERSON' or entity.label_ == 'NORP':
            name = entity.lemma_
            if len(name) > 2:
                res[name] = 1 + (0 if not res.__contains__(name) else res[name])
    return res


def names_in_text(text):
    # text = text.replace('\n', '')
    nlp = en_core_web_sm.load()
    doc = nlp(text)
    # get all possible names
    pos_names = get_names_in_doc(doc)

    # res = {}
    # for name in pos_names.keys():
    #     # if name[0].isupper():
    #     res[name] = pos_names[name]
    return pos_names


def get_names_by_chapters(chapters):
    names_in_chapters = {}
    for ch in chapters:
        names = names_in_text(chapters[ch])
        names_in_chapters[ch] = names
    return names_in_chapters
