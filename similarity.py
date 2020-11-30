import re

import jieba
import pandas as pd
import spacy
from gensim import corpora, similarities
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer
from fuzzywuzzy import process
from gensim import models
nlp = English()
tokenizer = Tokenizer(nlp.vocab)
long_desc_eng = pd.read_csv('C:/Users/buhal/Downloads/long_staging_xml_2020.csv', delimiter=',')
shorty = pd.DataFrame(long_desc_eng)
nlp = spacy.load("en_core_web_lg")

cleaned = []
for i in range(len(shorty)):
    text = shorty['long_desc_eng'][i]
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

dictionary = corpora.Dictionary(cleaned)
feature_cnt = len(dictionary.token2id)
#Wörter und Anzahl von Texte, wo es vorkommt
print(dictionary.token2id)
#(word_id, word_count)
corpus = [dictionary.doc2bow(text) for text in cleaned]
print(corpus)


tfidf = models.TfidfModel(corpus)
# for document in tfidf[corpus]:
#     print(document)
keyword = "authority"
kw_vector = dictionary.doc2bow(jieba.lcut(keyword))
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features = feature_cnt)
sim = index[tfidf[kw_vector]]
for i in range(len(sim)):
    if sim[i] != 0.0:
        print('keyword is similar to text%d: %.4f' % (i + 1, sim[i]))