'''
For counting votes and ranking the counts. 
'''
import collections
import operator

data = {}

while True:
    op = input('new: ').lower().strip()
    if op == 'end':
        break
    if op in data:
        data[op] += 1
    else:
        data[op] = 1
    data = collections.OrderedDict(sorted(data.items()))
    print()
    [print(x) for x in data.items()]
    print('added:', op)
print()
print('ranked:')
sorted = sorted(data.items(), key=operator.itemgetter(1))
[print(x) for x in reversed(sorted)]
input('Enter.. ')
