'''
Uses dynamic programming (DP) to calculate the minimum editing distance.  
DP is implemented via a breadth-first search with function caching.  
'''

from functools import lru_cache
import numpy as np

def editDistance(
    a, b, 
    insert_cost = 1, del_cost = 1, replace_cost = 1, 
):
    @lru_cache()
    def matrix(x, y):
        if x == 0 and y == 0:
            return 0
        if x == -1 or y == -1:
            return np.inf
        return min(
            matrix(x - 1, y) + insert_cost, 
            matrix(x, y - 1) + del_cost, 
            matrix(x - 1, y - 1) + (
                0 if a[x - 1] == b[y - 1] else replace_cost
            ), 
        )
    return matrix(len(a), len(b))

def test(a, b, do_swap = True):
    print(f'"{a}", "{b}" ->', editDistance(a, b))
    if do_swap:
        test(b, a, False)

if __name__ == '__main__':
    test('asd', 'rsd')
    test('asdf', 'asdf')
    test('asdf', 'assf')
    test('asdf', 'asf')
    test('banana', 'palace')
    test('banana palace', 'palace')
    test('cat', 'cut')
    test('saturday', 'sunday')
    test('1234567890', '23e45ty780')
