import re
import pandas as pd
import spacy
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer
import pandas as pd
import math
from collections import Counter

nlp = English()
tokenizer = Tokenizer(nlp.vocab)
long_desc_eng = pd.read_csv('../500_staging_xml_2020.csv', delimiter=',')

shorty = pd.DataFrame(long_desc_eng)
nlp = spacy.load("en_core_web_lg")
cleaned = []
for i in range(len(shorty)):
    text = shorty['long_desc_eng'][i]
    lemma = [tok.lemma_ for tok in nlp(text)]
    no_punct = [tok for tok in lemma if re.match('\w+', tok)]
    no_zeichen = [tok for tok in no_punct if not re.match('\. \+ \* \( \) \[ \] \- \$ \|', tok)]
    no_numbers = [tok for tok in no_zeichen if not re.match('\d+', tok)]
    no_whitespaces = [tok for tok in no_numbers if not re.match('\s+', tok)]
    filtered_sentence = []
    for word in no_whitespaces:
        lexeme = nlp.vocab[word]
        if not lexeme.is_stop:
            filtered_sentence.append(word)
    cleaned.append(filtered_sentence)

# for index in range(len(cleaned)):
#    print(cleaned[index])

# def all_values_containing_substring(substring):
#     list = cleaned
#     #print(list)
#     gotIt = []
#     for i, s in enumerate(list):
#         if substring in s:
#               gotIt.append(shorty['SHORT_DESC_ENG'][i])
#               gotIt.append("_____________________________________________________________________________")
#     for index in range(len(gotIt)):
#         print(gotIt[index])
#
# all_values_containing_substring("concern")

corpus_tf = []


def compute_tf(text):
    # text = text.split()
    tf_text = Counter(text)
    tf_text = {i: tf_text[i] / float(len(text)) for i in tf_text}
    return tf_text


for text in cleaned:
    corpus_tf.append(compute_tf(text))

unic_words = set()
for text in cleaned:
    unic_words = set(unic_words).union(set(text))


def compute_idf(word, cleaned):
    return math.log10(len(cleaned) / sum([1.0 for i in cleaned if word in i]))


word_idf = {}
for word in unic_words:
    word_idf[word] = compute_idf(word, cleaned)

tfidf = {}
for i, text_tf in enumerate(corpus_tf):
    for word in text_tf.keys():
        if word not in tfidf:
            tfidf[word] = {}
        tfidf[word][i] = round(text_tf[word] * word_idf[word], 4)

# for index, valuesList in tfidf.items():
#     for values in valuesList.items():
#         sort_orders = sorted(valuesList.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
#         tfidf[index] = sort_orders.copy()
# anzahl_vocab = 0
for x, y in tfidf.items():
    print(x,y)

