import re
import pandas as pd
import spacy
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer

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
    print(i, filtered_sentence)