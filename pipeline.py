import re
import pandas as pd
import spacy
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer
import math
from collections import Counter

nlp = English()
tokenizer = Tokenizer(nlp.vocab)

short_desc_eng = pd.read_csv('/Users/larakiyicioglu/Documents/Semester3/Schuetzinnen/new_new_staging_xml_2020.csv',
                             delimiter=',')
shorty = pd.DataFrame(short_desc_eng)
nlp = spacy.load("en_core_web_sm")

cleaned = []
for i in range(len(shorty)):
    text = shorty['SHORT_DESC_ENG'][i]
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
corpus_tf = []


def compute_tf(text):
    tf_text = Counter(text)
    tf_text = {i: tf_text[i] / float(len(text)) for i in tf_text}
    return tf_text


for text in cleaned:
    corpus_tf.append(compute_tf(text))
    pd.DataFrame(corpus_tf)
    unic_words = set()
for text in cleaned:
    unic_words = set(unic_words).union(set(text))


def compute_idf(word, cleaned):
    return math.log10(len(cleaned) / sum([1.0 for i in cleaned if word in i]))


word_idf = {};
for word in unic_words:
    word_idf[word] = compute_idf(word, cleaned)

pd.DataFrame([word_idf])
index = {}
for i, text_tf in enumerate(corpus_tf):
    for word in text_tf.keys():
        if word not in index:
            index[word] = {}
        index[word][i] = text_tf[word] * word_idf[word]

query = 'competition'
if query in index:
    for i in index[query].keys():
        print(i, shorty['SHORT_DESC_ENG'][i])
else:
    print("Es gibt kein Satz mit dem Wort " + query)
