def a():
    l = []
    for i in range(4):
        l.append(lambda :i)
    return l

print([x() for x in a()])
input('enter...')

# ??? THAT IS NOT CLOSURE OKAY
