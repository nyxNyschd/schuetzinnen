import re
import pandas as pd
import spacy
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer

nlp = English()
tokenizer = Tokenizer(nlp.vocab)
long_desc_eng = pd.read_csv('long_staging_xml_2020.csv', delimiter=',')
shorty = pd.DataFrame(long_desc_eng)
nlp = spacy.load("en_core_web_sm")

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


def substring_cleaning(substring):
    doc1 = nlp(substring)
    for token in doc1:
        lemma = token.lemma_
        no_punct = lemma if re.match('\w+', substring) else lemma
        no_zeichen = no_punct if not re.match('\. \+ \* \( \) \[ \$ \|', substring) else no_punct
        no_numbers = no_zeichen if not re.match('\d+', substring) else no_zeichen
        no_whitespaces = no_numbers if not re.match('\s+', substring) else no_numbers
        #print(no_whitespaces)
        return no_whitespaces


#substring_cleaning('works.')


def all_values_containing_substring(substring):
    cleaned_suchwort = substring_cleaning(substring)
    list = cleaned
    gotIt = []
    for i, s in enumerate(list):
        if cleaned_suchwort in s:
            gotIt.append(shorty['long_desc_eng'][i])
            gotIt.append("_____________________________________________________________________________")
    for index in range(len(gotIt)):
        print(gotIt[index])


all_values_containing_substring("works78")
