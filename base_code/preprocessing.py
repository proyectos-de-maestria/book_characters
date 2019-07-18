import en_core_web_sm
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def spacy_names(text):
    res = {}
    step = 1000000
    if len(text) > step:
        nlp = en_core_web_sm.load( )

        for i in range(step, len(text), step):
            doc = nlp(text[i - step:i])
            for entity in doc.ents:
                if entity.label_ == 'PERSON':
                    res[entity.lemma_] = 1 + (1 if res.__contains__(entity.lemma_) else 0)
                # print(entity.lemma_ + entity.label_)
    else:
        res = names_in_text(text)
    return res


def get_names_in_doc(doc):
    res = {}
    # get all possible names
    for entity in doc.ents:
        if entity.label_ == 'PERSON':
            name = entity.lemma_
            if len(name) > 2:
                res[name] = 1 + (0 if not res.__contains__(name) else res[name])
    return res


def get_sentiment_classification(text):
    sentences = nltk.sent_tokenize(text)
    sid = SentimentIntensityAnalyzer( )
    sentiment = 0
    for sentence in sentences:
        ss = sid.polarity_scores(sentence)
        maxi = max(ss.values())
        if ss['pos'] and ss['pos'] == maxi:
            sentiment += 1
        elif ss['neg'] and ss['neg'] == maxi:
            sentiment -= 1
    if sentiment:
        return 1 if sentiment > 0 else -1
    else:
        return sentiment



def names_in_text(text):
    # text = text.replace('\n', '')
    nlp = en_core_web_sm.load( )
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

