import pandas as pd
import math
from collections import Counter
import spacy
import pickle
import re

infile2 = open('lookup_table', 'rb')
LOOKUP_TABLE = pickle.load(infile2)
infile2.close()

long_desc_eng = pd.read_csv('long_staging_xml_2020.csv', delimiter=',')
long = pd.DataFrame(long_desc_eng)
nlp = spacy.load("en_core_web_lg")


def substring_cleaning(query):
    substringlist=[]
    doc1 = nlp(query)
    for token in doc1:
        lemma = token.lemma_
        no_punct = lemma if re.match('\w+', query) else lemma
        no_zeichen = no_punct if not re.match('[\,\+\*\(\)\|\[\]\?\!\/\=\{\}\#\&\;\:\_]', query) else no_punct
        cleaned_substring = no_zeichen if not re.match('\s+', query) else no_zeichen
        substringlist.append(cleaned_substring)
    return substringlist

substring_cleaning("huhu haaallo")


def add_tfidf_values_for_phrase_search(query):
    cleaned_query = substring_cleaning(query)

    gotIt = []
    # print("RESULT FOR YOUR SEARCH: " + cleaned_query)
    for key, values in LOOKUP_TABLE.items():
        for index, score in values:
            print("das ist der tfidf-score: ", score)

        for word in cleaned_query:
            index_of_buddies = []
            remember_my_index = False

            if word in key and not remember_my_index:
                for j in range(len(values)):
                    gotIt.append(long['long_desc_eng'][values[j][0]])
                    index_of_buddies.append(values[key])
                    remember_my_index = True
                    print("und jetze will ich die indizes für das andere wort")

            elif word in key and remember_my_index:
                for index, score in index_of_buddies:
                    if index == values.index[key]:
                        values.score[key] += index_of_buddies.score
                        gotIt.append(long['long_desc_eng'][values[j][values.score[key]]])

        for i in range(len(gotIt)):
            print(str(i) + " " + gotIt[i])











#addiert tf-werte nur für ein dokument, fängt dann wieder neu an - das war ein erster versuch
corps=[
"He would only survive if he kept the fire going and he could hear thunder in the distance.",
"The delicious aroma from the kitchen was ruined by cigarette smoke.",
"A quiet house stay is nice until you are nice ordered to stay in it for months."]

def add_tfs(my_list):
    counted=[]
    for text in my_list:
        for item in [ele for ind, ele in enumerate(text,1) if ele not in counted[ind:]]:
            count = 0
            for ele in text:
                if item == ele:
                    item=ele
                    count += 1
            tf=(item,count)
            counted.append(tf)
    print(counted)
