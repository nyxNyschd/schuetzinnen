import re
import pandas as pd
import spacy
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer
import math
from collections import Counter

nlp = English()
tokenizer = Tokenizer(nlp.vocab)

# read data from csv-file
short_desc_eng = pd.read_csv('cpv_short_desc_eng.csv', delimiter=',')
# create dataframe containing all entries of 'short_desc_eng', which can be handed over to spacy pipeline
shorty = pd.DataFrame(short_desc_eng)
# hand over column 'short_desc_eng' as dataframe
short_desc = shorty['short_desc_eng']

nlp = spacy.load("en_core_web_sm")

cleaned = []
def clean_text():
    for i in range(len(shorty)):
        text = short_desc[i]
        lemma = [tok.lemma_ for tok in nlp(text)]
        no_punct = [tok for tok in lemma if re.match('\w+', tok)]
        no_zeichen = [tok for tok in no_punct if not re.match('\. \+ \* \( \) \[ \] \- \$ \|', tok)]
        no_numbers = [tok for tok in no_zeichen if not re.match('\d+', tok)]
        no_whitespaces = [tok for tok in no_numbers if not re.match('\s+', tok)]
        filtered_sentence = []
        for word1 in no_whitespaces:
            lexeme = nlp.vocab[word1]
            if not lexeme.is_stop:
                filtered_sentence.append(word1)
        cleaned.append(filtered_sentence)
    print(cleaned)


# def all_values_containing_substring(substring):
#     list
#     print(list)
#     gotIt = []
#     for i, s in enumerate(list):
#         if substring in s:
#               gotIt.append(list[i])
#               gotIt.append("_____________________________________________________________________________")
#     #print(gotIt)
#     #return gotIt

all_values_containing_substring("competition")

# def compute_tf(text):
#     tf_text = Counter(text)
#     tf_text = {i: tf_text[i] / float(len(text)) for i in tf_text}
#     return tf_text
#
# corpus_tf = []
#
# #erstellen eines corpus für tfidf
# for text in cleaned:
#     corpus_tf.append(compute_tf(text))
#
#     #warum macht ihr hier ein dataframe?
#     #cleaned_frame = pd.DataFrame(corpus_tf)
#
# #herausfiltern aller duplikate
#     unic_words = set()
# for text in cleaned:
#     unic_words = set(unic_words).union(set(text))
#
#
# # #berechnung des idf -werts  --> ab hier eingabe eines suchwortes relevant
# # def compute_idf(suchwort):
# #
#     #zählt gewichtung des wortvorkommens(deshalb mit duplikaten)
#     idf = math.log10(len(cleaned) / sum([1.0 for i in cleaned if suchwort in i]))
#     word_idf = {}; #das ist hier ein dictionary
#
#     #sucht vorkommen des worts im gesamtcorpus (ohne duplikate)
#     for suchwort in unic_words:
#         word_idf[suchwort] = idf
#
#     #wozu bracuht ihr dieses dataframe?
#     final_frame = pd.DataFrame([word_idf])
#
#     index = []
#     for text_tf in corpus_tf:
#         #warum sind die indizes dieser liste plötzlich ein dict?
#         for suchwort in text_tf:
#             if suchwort not in index:
#                 index[suchwort] = []
#            # index[suchwort][j] = text_tf[suchwort] * word_idf[suchwort]
#    # return corpus_tf[text_tf].values()
#
#
# compute_idf("estimate")
#
# # query = 'competition'
# # if query in index:
# #     for i in index[query].keys():
# #         print(i, short_desc[i])
# # else:
# #     print("Es gibt kein Satz mit dem Wort " + query)
