import pandas as pd

#read data from csv-file
short_desc_eng = pd.read_csv('cpv_short_desc_eng.csv', delimiter=',')

#create dataframe
shorty = pd.DataFrame(short_desc_eng)

#create indexed list containing all entries of 'short_desc_eng', which can be handed over to spacy pipeline
import spacy
nlp = spacy.load('en_core_web_sm')
from spacy.lang.en import English
parser = English()
short_desc = shorty['short_desc_eng'].tolist()


#testing the index of the new list
#[index for index, value in enumerate(short_desc) if value == 'The establishment of a provisional cable installations at Mosseporten transformation station.']

#comparing the list's index with the one of the dataframe
#shorty['short_desc_eng'][1]

#simple search for substring in the list, returning index of first occurrence
def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
              return i
    return -1

index_containing_substring(short_desc, "streets")


#search for substring, returning all occurences
def all_index_containing_substring(the_list, substring):
    gotIt = []
    for i, s in enumerate(the_list):
        if substring in s:
              gotIt.append(i)
    return gotIt

all_index_containing_substring(short_desc, "estimate")


#search for substring, returning the value at index of occurences
def all_values_containing_substring(the_list,substring):
    gotIt = []
    for i, s in enumerate(the_list):
        if substring in s:
              gotIt.append(the_list[i])
              gotIt.append("_______________________________________________________________________________")
    return gotIt

#all_values_containing_substring(short_desc,"streets")
#all_values_containing_substring(short_desc,"estimate")

