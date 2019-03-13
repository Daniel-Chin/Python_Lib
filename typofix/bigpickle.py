import re
import pickle
from collections import Counter
import operator
from string import ascii_lowercase

with open('big.txt', 'r') as f:
    big = f.read().lower()
counter = Counter(re.findall(r'\w+', big))
words = {x for x in counter if all([y in ascii_lowercase for y in x])}
with open('words.pickle', 'wb+') as f:
    pickle.dump(words, f)
