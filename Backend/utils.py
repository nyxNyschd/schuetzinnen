import re
import os
import pandas as pd
import spacy
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer
import math
import pickle
from collections import Counter
import multiprocessing
from gensim.models import Word2Vec


def get_corpus():
    #long_desc_eng = pd.read_csv('../500_staging_xml_2020.csv', delimiter=',')  # <------- Backend
    #long_desc_eng = pd.read_csv('../daten.csv', delimiter=',') #<------- Backend
    #long_desc_eng = pd.read_csv(os.getcwd()+'/500_staging_xml_2020.csv', delimiter=',') #<------- Frontend
    long_desc_eng = pd.read_csv(os.getcwd()+'/daten.csv', delimiter=',') #<------- Frontend
    return pd.DataFrame(long_desc_eng)


def clean_corpus():
    nlp = spacy.load("en_core_web_lg")
    cleaned = []
    long = get_corpus()

    for i in range(len(long)):
        text = long['long_desc_eng'][i]
        text = re.sub("[^A-Za-z']+", ' ', str(text)).lower()
        lemma = [tok.lemma_ for tok in nlp(text)]
        no_punct = [tok for tok in lemma if re.match('[\w]+', tok)]
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

def list_ranking(cleaned):
    tf = tf_compute(cleaned)
    idf = idf_compute(cleaned)
    tfidf = {}
    for i, j in enumerate(tf):
        for word in j.keys():
            if word not in tfidf:
                tfidf[word] = {}
            tfidf[word][i] = round(j[word] * idf[word], 4)
    #print(tfidf)

    return tfidf


def similar_words_tabelle(cleaned):
    w2v_model = Word2Vec(min_count=1,
                         window=5,
                         size=300,
                         alpha=0.03,
                         min_alpha=0.0007,
                         negative=5,
                         workers=multiprocessing.cpu_count() - 1)

    w2v_model.build_vocab(cleaned, progress_per=10000)

    # Training of the model
    w2v_model.train(cleaned, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1)

    # lookup tabelle erstellen
    unique_words = set()
    for text in cleaned:
        unique_words = set(unique_words).union(set(text))
    lookup_table = {}
    for word in unique_words:
        try:
            similar = w2v_model.wv.most_similar(positive=[word])[:2]
            similar_words = [i[0] for i in similar]
            lookup_table[word] = similar_words
        except KeyError:
            continue

    return lookup_table

#wenn ihr mit Frontend arbeiten möchtet:
# if __name__ == 'utils':
#     docs = clean_corpus()
#     outfile1 = open('Backend/tokens', 'wb')
#     pickle.dump(docs, outfile1)
#     outfile1.close()
#
#     ranked_list = list_ranking(docs)
#     filename = 'Backend/lookup_table'
#     outfile2 = open(filename, 'wb')
#     pickle.dump(ranked_list, outfile2)
#     outfile2.close()
#
#     table_w2v = similar_words_tabelle(docs)
#     outfile3 = open('word2vec_table', 'wb')
#     pickle.dump(table_w2v, outfile3)
#     outfile3.close()

#wenn ihr mit Backend arbeiten möchtet:
if __name__ == '__main__':
    docs = clean_corpus()
    outfile1 = open('tokens', 'wb')
    pickle.dump(docs, outfile1)
    outfile1.close()

    ranked_list = list_ranking(docs)
    outfile2 = open('lookup_table', 'wb')
    pickle.dump(ranked_list, outfile2)
    outfile2.close()

    table_w2v = similar_words_tabelle(docs)
    outfile3 = open('word2vec_table', 'wb')
    pickle.dump(table_w2v, outfile3)
    outfile3.close()

