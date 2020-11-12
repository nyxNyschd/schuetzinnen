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

for i in range(len(shorty)):
    text = shorty['SHORT_DESC_ENG'][i]
    df = pd.DataFrame([[tok.text, tok.lemma_, tok.pos_, tok.tag_, tok.dep_,
                        tok.shape_, tok.is_alpha, tok.is_stop] for tok in nlp(text)])
    df.columns = ['text', 'lemma', 'pos', 'tag', 'dep', 'shape', 'is_alpha', 'is_stop']
    print(text)
    print(df)

    for ent in nlp(text).ents:
        print(ent.text, ent.label_, ':', spacy.explain(ent.label_))
    print('_________________________________________________________________________________________________________')

