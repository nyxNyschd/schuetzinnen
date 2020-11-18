import pandas as pd
import spacy
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer

nlp = English()
tokenizer = Tokenizer(nlp.vocab)

long_desc_eng = pd.read_csv('long_staging_xml_2020.csv',
                             delimiter=',')
shorty = pd.DataFrame(long_desc_eng)
nlp = spacy.load("en_core_web_lg")

for i in range(len(shorty)):
    text = shorty['long_desc_eng'][i]
    df = pd.DataFrame([[tok.text, tok.lemma_, tok.pos_, tok.tag_, tok.dep_, tok.shape_, tok.is_alpha, tok.is_stop]
                       for tok in nlp(text)])
    df.columns = ['text', 'lemma', 'pos', 'tag', 'dep', 'shape', 'is_alpha', 'is_stop']
    print(text)
    print(df)

for i in range(len(shorty)):
    text = shorty['long_desc_eng'][i]
    df1 = pd.DataFrame([[tok.text, tok.like_url, tok.is_currency, tok.ent_id_, tok.ent_iob_, tok.ent_type_,
                         tok.whitespace_] for tok in nlp(text)])
    df1.columns = ['text', 'like_url', 'is_currency', 'ent_id_', 'ent_iob_', 'ent_type', 'whitespace_']
    print(df1)

    for ent in nlp(text).ents:
        print(ent.text, ent.label_, ':', spacy.explain(ent.label_))
    print('_________________________________________________________________________________________________________')
