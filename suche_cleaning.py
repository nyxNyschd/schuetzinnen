import re
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


def substring_cleaning(substring):
    doc1 = nlp(substring)
    for token in doc1:
        lemma = token.lemma_
        no_punct = lemma if re.match('\w+', substring) else lemma
        no_zeichen = no_punct if not re.match('[\,\+\*\(\)\|\[\]\?\!\/\=\{\}\#\&\;\:\_]', substring) else no_punct
        no_whitespaces = no_zeichen if not re.match('\s+', substring) else no_zeichen
        print(no_whitespaces)
        return no_whitespaces


def all_values_containing_substring(substring):
    cleaned_suchwort = substring_cleaning(substring)
    list = cleaned
    gotIt = []
    for i, s in enumerate(list):
        if cleaned_suchwort in s:
            Ratios = process.extract(cleaned_suchwort, list[i])
            print(Ratios)
            gotIt.append(shorty['long_desc_eng'][i])
            gotIt.append("_____________________________________________________________________________")
    for index in range(len(gotIt)):
        print(gotIt[index])


# def all_values_containing_substring(substring):
#     Ratios = process.extract(substring, list[i])
#     print(Ratios)
#     list = cleaned
#     gotIt = []
#     for i, s in enumerate(list):
#         if cleaned_suchwort in s:
#             gotIt.append(shorty['long_desc_eng'][i])
#             gotIt.append("_____________________________________________________________________________")
#     for index in range(len(gotIt)):
#         print(gotIt[index])


#all_values_containing_substring("measurs")


# nächste entwicklungsschritte:
# fehlererkennung fuzzy logic
# akzente normalisieren mit tagging
# textähnlichkeiten similarity modul

def fuzzy_logic(substring):
    for i in range(len(cleaned)):
        #if
            Ratios = process.extract(substring, cleaned[i])
            print(Ratios)
    return Ratios


fuzzy_logic('meazure')

# str2Match = "proceduer"
# print(str2Match)
# strOptions = cleaned[i]
# print(strOptions)
# Ratios = process.extract(str2Match, strOptions)
# print(Ratios)
# highest = process.extractOne(str2Match, strOptions)
# print(highest)
# for index in range(len(Ratios)):
#     print(Ratios[index])
