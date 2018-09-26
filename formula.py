'''
Evaluate beautiful formulas like    √(2×3÷4)
'''
from console import console
from math import sqrt

def fixer(raw):
    s1 = raw.replace('×', '*') \
        .replace('^', '**') \
        .replace('〖', '(') \
        .replace('〗', ')') \
        .replace('÷', '/') \
        .replace('√(', 'sqrt(')
    l1 = s1.split('√')
    for i_seg in range(1, len(l1)):
        for i, chara in enumerate(l1[i_seg]):
            if chara=='.' or chara.isnumeric():
                continue
            i -= 1
            break
        i += 1
        l1[i_seg] = 'sqrt(' + l1[i_seg][:i] + ')' + l1[i_seg][i:]
    return ''.join(l1)

def main():
    console({'sqrt':sqrt}, use_input = True, fixer = fixer)

if __name__ == '__main__':
    main()
