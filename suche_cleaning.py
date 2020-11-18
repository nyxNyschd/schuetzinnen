# import re
# import pandas as pd
# import spacy
# from spacy.lang.en import English
# from spacy.tokenizer import Tokenizer
#
# nlp = English()
# tokenizer = Tokenizer(nlp.vocab)
#
# long_desc_eng = pd.read_csv('long_staging_xml_2020.csv',
#                              delimiter=',')
# shorty = pd.DataFrame(long_desc_eng)
# nlp = spacy.load("en_core_web_lg")
#
# cleaned = []
# for i in range(len(shorty)):
#     text = shorty['long_desc_eng'][i]
#     lemma = [tok.lemma_ for tok in nlp(text)]
#     no_punct = [tok for tok in lemma if re.match('\w+', tok)]
#     no_zeichen = [tok for tok in no_punct if not re.match('\. \+ \* \( \) \[ \] \- \$ \|', tok)]
#     no_numbers = [tok for tok in no_zeichen if not re.match('\d+', tok)]
#     no_whitespaces = [tok for tok in no_numbers if not re.match('\s+', tok)]
#     filtered_sentence = []
#     for word in no_whitespaces:
#         lexeme = nlp.vocab[word]
#         if not lexeme.is_stop:
#             filtered_sentence.append(word)
#     cleaned.append(filtered_sentence)
#
#
# nlp = English()
# tokenizer = Tokenizer(nlp.vocab)
#
# nlp = spacy.load("en_core_web_lg")
#
#
# def all_values_containing_substring(substring):
#     cleaned_suchwort = substring_cleaning(substring)
#     list = cleaned
#     gotIt = []
#     for i, s in enumerate(list):
#         if cleaned_suchwort in s:
#             gotIt.append(shorty['long_desc_eng'][i])
#             gotIt.append("_____________________________________________________________________________")
#     for index in range(len(gotIt)):
#         print(gotIt[index])
#
#
# all_values_containing_substring("works-")
#
#
# # def substring_cleaning(substring):
# #     lemma = [substring.lemma_ in nlp(substring)]
# #     no_punct = [substring in lemma if re.match('\w+', substring)]
# #     no_zeichen = [ substring in no_punct if not re.match('\. \+ \* \( \) \[ \] \- \$ \|', substring)]
# #     no_numbers = [ substring in no_zeichen if not re.match('\d+', substring)]
# #     no_whitespaces = [ substring in no_numbers if not re.match('\s+', substring)]
# #     return no_whitespaces
#
#
