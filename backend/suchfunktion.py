import pickle
import re
import spacy
from fuzzywuzzy import process
from backend.utils import get_corpus

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

def merge_dict_summ(dict1, dict2):
    # print({k: index[query[0]].get(k, 0) + index[query[1]].get(k, 0) for k in set(index[query[0]]) | set(index[query[1]])}
    return {k: dict1.get(k, 0) + dict2.get(k, 0) for k in set(dict1) | set(dict2)}

def preprocess_query(query_words):
    return [w if w in LOOKUP_TABLE.keys() else fuzzy_logic(w) for w in query_words]

def main_search(query):
    result = {}

    for word in query:
        if word in LOOKUP_TABLE.keys():
            result = merge_dict_summ(result, LOOKUP_TABLE[word])
    result = sorted(result, key=result.get, reverse=True)
    long = get_corpus()

    return [long['long_desc_eng'][i] for i in result]

def similar_search(query):
    print(query)

    similar_words = []
    for word in query:
        if word in WORD2VEC_TABLE:
            similar_words += WORD2VEC_TABLE[word]
    print(similar_words)

    return main_search(similar_words)

#wenn ihr mit Frontend arbeiten möchtet:
if __name__ == 'Backend.suchfunktion':
    infile1 = open('Backend/tokens', 'rb')
    CLEANED = pickle.load(infile1)
    infile1.close()
    infile2 = open('Backend/lookup_table', 'rb')
    LOOKUP_TABLE = pickle.load(infile2)
    infile2.close()
    infile3 = open('Backend/word2vec_table', 'rb')
    WORD2VEC_TABLE = pickle.load(infile3)
    infile3.close()

#wenn ihr mit Backend arbeiten möchtet:
# if __name__ == '__main__':
#     infile1 = open('tokens', 'rb')
#     CLEANED = pickle.load(infile1)
#     infile1.close()
#     infile2 = open('lookup_table', 'rb')
#     LOOKUP_TABLE = pickle.load(infile2)
#     infile2.close()
#     main_search('permanent daily')