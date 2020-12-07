import math
import re
from collections import Counter
import pandas as pd
import spacy
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer
from fuzzywuzzy import process

nlp = English()
tokenizer = Tokenizer(nlp.vocab)
long_desc_eng = pd.read_csv('long_staging_xml_2020.csv', delimiter=',')
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


# print(cleaned)

def substring_cleaning(substring):
    doc1 = nlp(substring)
    for token in doc1:
        lemma = token.lemma_
        no_punct = lemma if re.match('\w+', substring) else lemma
        no_zeichen = no_punct if not re.match('[\,\+\*\(\)\|\[\]\?\!\/\=\{\}\#\&\;\:\_]', substring) else no_punct
        cleaned_substring = no_zeichen if not re.match('\s+', substring) else no_zeichen
        return cleaned_substring


def fuzzy_logic(substring):
    highest_value = 0
    most_relevant_word = ' '
    for i in range(len(cleaned)):
        Ratios = process.extract(substring, cleaned[i])
        for index in range(len(Ratios)):
            if highest_value < (Ratios[index][1]) and len(Ratios[index][0]) > 2:
                temp = process.extractOne(substring, cleaned[i])
                highest_value = temp[1]
                most_relevant_word = temp[0]
    return most_relevant_word


def list_ranking(list):
    ranked_list = []
    corpus_tf = []

    for text in list:
        tf_text = Counter(text)
        tf_text = {i: tf_text[i] / float(len(text)) for i in tf_text}
        corpus_tf.append(tf_text)

    unique_words = set()
    for text in list:
        unique_words = set(unique_words).union(set(text))

    word_idf = {}
    for word in unique_words:
        word_idf[word] = math.log10(len(list) / sum([1.0 for i in cleaned if word in i]))

    tfidf = {}
    for i, text_tf in enumerate(corpus_tf):
        for word in text_tf.keys():
            if word not in tfidf:
                tfidf[word] = {}
            tfidf[word][i] = round(text_tf[word] * word_idf[word], 4)

    for index, valuesList in tfidf.items():
        for values in valuesList.items():
            sort_orders = sorted(valuesList.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
            tfidf[index] = sort_orders.copy()

    # for index, values in tfidf.items():
    #     for j in range(len(values)):
    #         if substring in index:
    #             #print(values[j][0])
    #             ranked_list.append(list[tfidf[substring][j][0]])
    return tfidf


def all_values_containing_substring(substring):
    fuzzy = fuzzy_logic(substring)
    cleaned_searched_word = substring_cleaning(fuzzy)
    print("Das relevanteste Wort: " + cleaned_searched_word)
    ranked_dict = list_ranking(cleaned)
    gotIt = []
    # for index, values in ranked_dict.items():
    #     print(index, values)
    for s, list in ranked_dict.items():
        for j in range(len(list)):
            if cleaned_searched_word in s:
                gotIt.append(shorty['long_desc_eng'][list[j][0]])
                gotIt.append("_____________________________________________________________________________")
    for index in range(len(gotIt)):
        print(gotIt[index])
        return gotIt


#all_values_containing_substring("limit")
