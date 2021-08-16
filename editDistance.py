'''
Uses dynamic programming (DP) to calculate the minimum editing distance.  
DP is implemented via a breadth-first search with function caching.  
'''

from functools import lru_cache

def editDistance(
    a, b, 
    insert_cost = 1, del_cost = 1, replace_cost = 1, 
):
    @lru_cache(maxsize=len(a) * len(b))
    def matrix(x, y):
        if x == 0:
            return y * insert_cost
        if y == 0:
            return x * del_cost
        if a[x] == b[y]:
            return matrix(x - 1, y - 1)
        else:
            return min(
                matrix(x, y - 1) + insert_cost, 
                matrix(x - 1, y) + del_cost, 
                matrix(x - 1, y - 1) + replace_cost, 
            )
    return matrix(len(a) - 1, len(b) - 1)

def test(a, b, do_swap = True):
    print(f'"{a}", "{b}" ->', editDistance(a, b))
    if do_swap:
        test(b, a, False)

if __name__ == '__main__':
    test('asdf', 'asdf')
    test('asdf', 'assf')
    test('asdf', 'asf')
    test('banana', 'palace')
    test('banana palace', 'palace')
    test('cat', 'cut')
    test('saturday', 'sunday')
    test('1234567890', '123e45ty780')
