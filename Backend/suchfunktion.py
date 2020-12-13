import pickle
import re
import spacy
from fuzzywuzzy import process
from spacy.lang.en import English
from utils import long
nlp = English()
nlp = spacy.load("en_core_web_lg")


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
    print(__name__)
    most_relevant_word = ' '
    for i in range(len(CLEANED)):
        Ratios = process.extract(substring, CLEANED[i])
        for index in range(len(Ratios)):
            if highest_value < (Ratios[index][1]) and len(Ratios[index][0]) > 2:
                temp = process.extractOne(substring, CLEANED[i])
                highest_value = temp[1]
                most_relevant_word = temp[0]
    return most_relevant_word

def main_search(query):
    cleaned_query = substring_cleaning(query)
    fuzzy = fuzzy_logic(cleaned_query)
    gotIt = []
    for key, values in LOOKUP_TABLE.items():
        for index in range(len(values)):
            if cleaned_query in key:
                gotIt.append(long['long_desc_eng'][values[index][0]])
                #gotIt.append("..........................")
    if len(gotIt) == 0:
        #print("OOPS. WORD NOT FOUND: MAYBE YOU MEANT: " + fuzzy)
        for key, values in LOOKUP_TABLE.items():
            for index in range(len(values)):
                if fuzzy in key:
                    gotIt.append(long['long_desc_eng'][values[index][0]])
                    #gotIt.append("..........................")
    # for i in range(len(gotIt)):
    #     print(str(i) + " " + gotIt[i])
    return gotIt[:9]

if __name__ == 'Backend.suchfunktion':
    infile1 = open('Backend/tokens', 'rb')
    CLEANED = pickle.load(infile1)
    infile1.close()
    infile2 = open('Backend/lookup_table', 'rb')
    LOOKUP_TABLE = pickle.load(infile2)
    infile2.close()





