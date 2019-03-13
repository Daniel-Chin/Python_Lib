import keyboard
import pickle
from itertools import combinations_with_replacement, product

MAX_N_ERROR = 8
LONGEST_TO_FIX = 16
CORRECT = 1
NOT_A_WORD = 2
TOO_LONG = 3

with open('words.pickle', 'rb') as f:
    all_words = pickle.load(f)
with open('my_personal_dict_that_is_public_on_github.txt', 'r') as f:
    for line in f:
        all_words.add(line.strip())

def fixNoSwap(word, to_add = None, score_offset = 0):
    len_word = len(word)
    guessed = [keyboard.guess(x) for x in word]
    for score in range(1, min(len_word // 2 + 2, MAX_N_ERROR) + score_offset):
        for combination in combinations_with_replacement(range(len_word), score):
            char_scores = [0] * len_word
            for i_char in combination:
                char_scores[i_char] += 1
            if any([x >= 2 for x in char_scores]):
                continue
            for candidate in product(*[x[y] for x, y in zip(guessed, char_scores)]):
                candidate = ''.join(candidate)
                if candidate.lower() in all_words:
                    if to_add is None:
                        return candidate
                    else:
                        to_add.add(candidate)
    if to_add is None:
        return NOT_A_WORD

def fix(word, only_first = True):
    if word.lower() in all_words:
        return CORRECT
    if len(word) > LONGEST_TO_FIX:
        return TOO_LONG
    if only_first:
        results = None
    else:
        results = set()
    try:
        guess_no_swap = fixNoSwap(word, results)
        if only_first and guess_no_swap != NOT_A_WORD:
            return guess_no_swap
        for i in range(len(word) - 1):
            chars = [*word]
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
            swapped = ''.join(chars)
            if swapped.lower() in all_words:
                if only_first:
                    return swapped
                else:
                    results.add(swapped)
            guess_no_swap = fixNoSwap(swapped, results, -1)
            if only_first and guess_no_swap != NOT_A_WORD:
                return guess_no_swap
        if only_first:
            return NOT_A_WORD
        else:
            return results or NOT_A_WORD
    except keyboard.ImprobableChar:
        return NOT_A_WORD

def fixIO(inIO, outIO):
    

if __name__ == '__main__':
    from console import *
    console(globals())
