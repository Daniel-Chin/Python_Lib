import re
import pickle
from collections import Counter
import operator

with open('big.txt', 'r') as f:
    big = f.read().lower()
counter = Counter(re.findall(r'\w+', big))
words = tuple(x[0] for x in reversed(sorted(counter.items(), key=operator.itemgetter(1))))
with open('words.pickle', 'wb+') as f:
    pickle.dump(words, f)
