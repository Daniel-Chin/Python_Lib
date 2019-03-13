import keyboard
import pickle
from itertools import combinations_with_replacement

with open('words.pickle', 'rb') as f:
    words = pickle.load(f)
with open('my_personal_dict_that_is_public_on_github.txt', 'r') as f:
    for line in f:
        words.append(line.strip())

def fix(word):
    if word in words:
        return '_correct'
    