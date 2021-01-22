import pickle
import re
from turtle import pd

import spacy
from fuzzywuzzy import process
from spacy.lang.en import English
from utils import data_df
nlp = English()
nlp = spacy.load("en_core_web_lg")


def cleaning_query(substring):
    cleaned_query = []
    lemma = [tok.lemma_ for tok in nlp(substring)]
    no_punct = [tok for tok in lemma if re.match('\w+', tok)]
    no_zeichen = [tok for tok in no_punct if not re.match('\. \+ \* \( \) \[ \] \- \$ \|', tok)]
    #no_numbers = [tok for tok in no_zeichen if not re.match('\d+', tok)]
    no_whitespaces = [tok for tok in no_zeichen if not re.match('\s+', tok)]
    for word in no_whitespaces:
        lexeme = nlp.vocab[word]
        if not lexeme.is_stop:
            cleaned_query.append(word)
    return cleaned_query

def fuzzy_logic(substring):
    highest_value = 0
    most_relevant_word = ' '
    for i in range(len(CLEANED)):
        Ratios = process.extract(substring, CLEANED[i])
        for index in range(len(Ratios)):
            if highest_value < (Ratios[index][1]) and len(Ratios[index][0]) > 2:
                temp = process.extractOne(substring, CLEANED[i])
                highest_value = temp[1]
                most_relevant_word = temp[0]
    return most_relevant_word

def merge_index_sum(dict1, dict2):
    return {k: dict1.get(k, 0) + dict2.get(k, 0) for k in set(dict1) | set(dict2)}

def main_search(query):
    cleaned_query = cleaning_query(query)
    print(cleaned_query)
    result = {}
    for word in cleaned_query:
        if word in LOOKUP_TABLE.keys():
            #print(word, LOOKUP_TABLE[word])
            # for i in LOOKUP_TABLE[word].keys():
            #     print(i, long['long_desc_eng'][i])
            result = merge_index_sum(result, LOOKUP_TABLE[word])
        else:
            fuzzy = fuzzy_logic(word)
            print(fuzzy)
            result = merge_index_sum(result, LOOKUP_TABLE[fuzzy])
    result = sorted(result, key=result.get, reverse=True)
    print(result)

    gotIt = data_df.iloc[result, 0:13]

    # for i in result:
    #     gotIt.append(data_df['long_desc_eng'][i])
    #     gotIt.append('•••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••')
    # for i in range(len(gotIt)):
    #     print(gotIt[i])
    #return gotIt
    print(gotIt)

#wenn ihr mit Frontend arbeiten möchtet:
# if __name__ == 'Backend.suchfunktion':
#     infile1 = open('Backend/tokens', 'rb')
#     CLEANED = pickle.load(infile1)
#     infile1.close()
#     infile2 = open('Backend/lookup_table', 'rb')
#     LOOKUP_TABLE = pickle.load(infile2)
#     infile2.close()



#wenn ihr mit Backend arbeiten möchtet:
if __name__ == '__main__':
    infile1 = open('tokens', 'rb')
    CLEANED = pickle.load(infile1)
    infile1.close()
    infile2 = open('lookup_table', 'rb')
    LOOKUP_TABLE = pickle.load(infile2)
    infile2.close()
    main_search('1343400')
