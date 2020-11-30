
from fuzzywuzzy import process


def fuzzy_logic(substring, cleaned):
    highest_value = 0
    most_relevant_word = ' '
    for i in range(len(cleaned)):
        Ratios = process.extract(substring, cleaned[i])
        for index in range(len(Ratios)):
            if Ratios[index][1] > 80 and highest_value < (Ratios[index][1]) and len(Ratios[index][0]) > 2:
                temp = process.extractOne(substring, cleaned[i])
                highest_value = temp[1]
                most_relevant_word = temp[0]
    return most_relevant_word
