import pickle
import re
import spacy
from fuzzywuzzy import process
from spacy.lang.en import English
from utils import long
# import time

nlp = English()
nlp = spacy.load("en_core_web_lg")


def substring_cleaning(query):
    doc1 = nlp(query)
    for token in doc1:
        lemma = token.lemma_
        no_punct = lemma if re.match('\w+', query) else lemma
        no_zeichen = no_punct if not re.match('[\,\+\*\(\)\|\[\]\?\!\/\=\{\}\#\&\;\:\_]', query) else no_punct
        cleaned_substring = no_zeichen if not re.match('\s+', query) else no_zeichen
        return cleaned_substring


def fuzzy_logic(cleaned_query):
    highest_value = 0
    most_relevant_word = ' '
    for i in range(len(CLEANED)):
        Ratios = process.extract(cleaned_query, CLEANED[i])
        for index in range(len(Ratios)):
            if highest_value < (Ratios[index][1]) and len(Ratios[index][0]) > 2:
                temp = process.extractOne(cleaned_query, CLEANED[i])
                highest_value = temp[1]
                most_relevant_word = temp[0]
    return most_relevant_word


def all_values_containing_substring(query):
    # tic = time.perf_counter()
    cleaned_query = substring_cleaning(query)
    fuzzy = fuzzy_logic(cleaned_query)
    gotIt = []
    print("RESULT FOR YOUR SEARCH: " + cleaned_query)
    for key, values in LOOKUP_TABLE.items():
        for j in range(len(values)):
            if cleaned_query in key:
                gotIt.append(long['long_desc_eng'][values[j][0]])
                gotIt.append(".................")
    if len(gotIt) == 0:
        print("OOPS. WORD NOT FOUND: MAYBE YOU MEANT: " + fuzzy)
        for key, values in LOOKUP_TABLE.items():
            for j in range(len(values)):
                if fuzzy in key:
                    gotIt.append(long['long_desc_eng'][values[j][0]])
                    gotIt.append(".................")
    for i in range(len(gotIt)):
        print(gotIt[i])  # str(i) + " " +
    # toc = time.perf_counter()
    # print(f"Suchdauer {toc - tic:0.4f}")
    return gotIt[:9]


if __name__ == 'backend.suchfunktion':
    infile1 = open('backend/tokens', 'rb')
    CLEANED = pickle.load(infile1)
    infile1.close()
    infile2 = open('backend/lookup_table', 'rb')
    LOOKUP_TABLE = pickle.load(infile2)
    infile2.close()

# if __name__ == '__main__':
#     infile1 = open('tokens', 'rb')
#     CLEANED = pickle.load(infile1)
#     infile1.close()
#     infile2 = open('lookup_table', 'rb')
#     LOOKUP_TABLE = pickle.load(infile2)
#     infile2.close()
#     all_values_containing_substring('compatition')
