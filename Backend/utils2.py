import re
import pandas as pd
import spacy
import pickle
import logging  # Setting up the loggings to monitor gensim
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt='%H:%M:%S', level=logging.INFO)
from gensim.models.phrases import Phrases, Phraser
import multiprocessing
from gensim.models import Word2Vec

nlp = spacy.load("en_core_web_lg")
from suchfunktion import substring_cleaning

def cleaning(doc):
    txt = [token.lemma_ for token in doc if not token.is_stop]
    if len(txt) > 2:
        return ' '.join(txt)

def create_similarity_table():
    global lookup_table
    global w2v_model
    for word in w2v_model.vocabulary:
        try:
            similar = w2v_model.wv.most_similar(positive=[word])[:2]
            similar_words = [i[0] for i in similar]
            lookup_table[word] = similar_words
        except KeyError:
            continue

if __name__ == '__main__':
    df = pd.read_csv('../daten.csv')
    print(df.type())
    df.drop_duplicates(subset=["LONG_DESC_ENG"], inplace=True)
    print(df.columns)
    df.dropna(axis=1, inplace=True)
    df["test"]=df['LONG_DESC_ENG'].map(lambda x: x)
    df["clean"] = df['LONG_DESC_ENG'].map(substring_cleaning())
    # Removes non-alphabetic characters:
    # brief_cleaning = (re.sub("[^A-Za-z']+", ' ', str(row)).lower() for row in df['LONG_DESC_ENG'])
    # txt = [cleaning(doc) for doc in nlp.pipe(brief_cleaning, batch_size=5000, n_threads=-1)]
    # txt = [cleaning_query(doc) for doc in df['LONG_DESC_ENG'].values]
    # df_clean = pd.DataFrame({'clean': txt})
    # df_clean = df_clean.dropna().drop_duplicates()
    sent = [row.split() for row in df['clean'].values]

    # unique_words = set()
    # for text in sent:
    #     unique_words = set(unique_words).union(set(text))

    #phrases = Phrases(sent, min_count=30, progress_per=10000)
    #bigram = Phraser(phrases)
    #sentences = bigram[sent]

    w2v_model = Word2Vec(min_count=1,
                         window=5,
                         size=300,
                         alpha=0.03,
                         min_alpha=0.0007,
                         negative=5,
                         workers=multiprocessing.cpu_count() - 1)

    w2v_model.build_vocab(sent, progress_per=10000)

    # Training of the model
    w2v_model.train(sent, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1)

    # lookup tabelle erstellen
    lookup_table = {}
    infile = open('word2vec_tabelle', 'wb')
    pickle.dump(lookup_table, infile)
    infile.close()