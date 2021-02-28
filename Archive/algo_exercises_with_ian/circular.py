def doesContain(circle, target, start, end):
    end = end % len(circle)
    if start == end:
        return False
    if circle[start] < circle[end]:
        return circle[start] <= target < circle[end]
    else:
        return target < circle[end] or circle[start] <= target

def circularBS(circle, target):
    return helper(circle, target, 0, len(circle))

def helper(circle, target, start, end):
    cursor = round(0.618 * start + 0.382 * end)
    if circle[cursor] == target:
        return cursor
    if doesContain(circle, target, start, cursor):
        return helper(circle, target, start, cursor)
    elif doesContain(circle, target, cursor, end):
        return helper(circle, target, cursor, end)
    else:
        raise ValueError('Fail')

def test():
    TOP = 20
    for i in range(TOP):
        nice = [*range(i)]
        for j in range(i):
            mess = nice[j:] + nice[:j]
            print(mess)
            for k in range(i):
                found = circularBS(mess, k)
                truth = (k - j) % i
                if truth != found:
                    print('Mismatch!', truth, found)
                    input('Enter...')
                print(found, '==', truth)

if __name__ == '__main__':
    test()
    input('Enter...')
