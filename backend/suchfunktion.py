import pickle
import re
import spacy
from fuzzywuzzy import process
from spacy.lang.en import English
from utils import long
# import time

nlp = English()
nlp = spacy.load("en_core_web_lg")


def substring_cleaning(substring):
    cleaned_query = []
    lemma = [tok.lemma_ for tok in nlp(substring)]
    no_punct = [tok for tok in lemma if re.match('\w+', tok)]
    no_zeichen = [tok for tok in no_punct if not re.match('\. \+ \* \( \) \[ \] \- \$ \|', tok)]
    no_numbers = [tok for tok in no_zeichen if not re.match('\d+', tok)]
    no_whitespaces = [tok for tok in no_numbers if not re.match('\s+', tok)]
    for word in no_whitespaces:
        lexeme = nlp.vocab[word]
        if not lexeme.is_stop:
            cleaned_query.append(word)
    return cleaned_query


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


def merge_dict_summ(dict1, dict2):
    # print({k: index[query[0]].get(k, 0) + index[query[1]].get(k, 0) for k in set(index[query[0]]) | set(index[query[1]])}
    return {k: dict1.get(k, 0) + dict2.get(k, 0) for k in set(dict1) | set(dict2)}


def all_values_containing_substring(query):
    # tic = time.perf_counter()
    cleaned_query = substring_cleaning(query)
    print(cleaned_query)
    result = {}
    gotIt = []

    for word in cleaned_query:
        if word in LOOKUP_TABLE.keys():
            # print(word, LOOKUP_TABLE[word])
            # for i in LOOKUP_TABLE[word].keys():
            #     print(i, long['long_desc_eng'][i])
            result = merge_dict_summ(result, LOOKUP_TABLE[word])
        else:
            fuzzy = fuzzy_logic(word)
            print(fuzzy)
            result = merge_dict_summ(result, LOOKUP_TABLE[fuzzy])
    result = sorted(result, key=result.get, reverse=True)
    print(result)
    for i in result:
        gotIt.append(long['long_desc_eng'][i])
        gotIt.append("••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
    for i in range(len(gotIt)):
        print(gotIt[i])
    return gotIt
    # toc = time.perf_counter()
    # print(f"Suchdauer {toc - tic:0.4f}")


# Main fürs Frontend
if __name__ == 'backend.suchfunktion':
    infile1 = open('backend/tokens', 'rb')
    CLEANED = pickle.load(infile1)
    infile1.close()
    infile2 = open('backend/lookup_table', 'rb')
    LOOKUP_TABLE = pickle.load(infile2)
    infile2.close()

# Main fürs Backend
# if __name__ == '__main__':
#     infile1 = open('tokens', 'rb')
#     CLEANED = pickle.load(infile1)
#     infile1.close()
#     infile2 = open('lookup_table', 'rb')
#     LOOKUP_TABLE = pickle.load(infile2)
#     infile2.close()
#     all_values_containing_substring('public sector bodies')
