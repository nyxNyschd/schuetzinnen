import re
import pandas as pd
import spacy
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer
import math
import pickle
from collections import Counter

nlp = English()
tokenizer = Tokenizer(nlp.vocab)
long_desc_eng = pd.read_csv('../500_staging_xml_2020.csv', delimiter=',')
long = pd.DataFrame(long_desc_eng)
nlp = spacy.load("en_core_web_lg")

cleaned = []

def clean_corpus():
    for i in range(len(long)):
        text = long['long_desc_eng'][i]
        lemma = [tok.lemma_ for tok in nlp(text)]
        no_punct = [tok for tok in lemma if re.match('\w+', tok)]
        no_zeichen = [tok for tok in no_punct if not re.match('\. \+ \* \( \) \[ \] \- \$ \|', tok)]
        no_whitespaces = [tok for tok in no_zeichen if not re.match('\s+', tok)]
        filtered_sentence = []
        for word in no_whitespaces:
            lexeme = nlp.vocab[word]
            if not lexeme.is_stop:
                filtered_sentence.append(word)
        cleaned.append(filtered_sentence)
    return cleaned

def tf_compute(cleaned):
    corpus_tf = []

    for text in cleaned:
        tf_text = Counter(text)
        tf_text = {i: tf_text[i] / float(len(text)) for i in tf_text}
        corpus_tf.append(tf_text)

    return corpus_tf

def idf_compute(cleaned):
    unique_words = set()
    for text in cleaned:
        unique_words = set(unique_words).union(set(text))

    word_idf = {}
    for word in unique_words:
        word_idf[word] = math.log10(len(cleaned) / sum([1.0 for i in cleaned if word in i]))

    return word_idf

def list_ranking():
    tf = tf_compute(cleaned)
    idf = idf_compute(cleaned)
    tfidf = {}
    for i, j in enumerate(tf):
        for word in j.keys():
            if word not in tfidf:
                tfidf[word] = {}
            tfidf[word][i] = round(j[word] * idf[word], 4)

    for index, valuesList in tfidf.items():
        for values in valuesList.items():
            sort_orders = sorted(valuesList.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
            tfidf[index] = sort_orders.copy()


    return tfidf

if __name__ == '__main__':
    docs = clean_corpus()
    outfile1 = open('tokens', 'wb')
    pickle.dump(docs, outfile1)

    ranked_list = list_ranking()
    filename = 'lookup_table'
    outfile2 = open(filename, 'wb')
    pickle.dump(ranked_list, outfile2)
