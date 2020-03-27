import re

BASE_DICT = "liste_francais.txt"

def build_list(string):
    words_list = re.split('\n|\n\n|;|; |,|, |¿| : | |  ', string)
    while '' in words_list: #Clean up
        words_list.remove('')
    return words_list


def read_dictionary(file):
    with open(file) as f:
        dictionary = [word.strip() for word in f.readlines()]
    return dictionary


def list_uncommon_words(list_, dictionary_list):
    """For each word in the list_, checks if it exists in dictionary_list.
    If it doesn't exists, it is added to the output list"""
    output = []
    for word in list_:
        if word.lower() not in dictionary_list:
            output.append(word)
    return output
