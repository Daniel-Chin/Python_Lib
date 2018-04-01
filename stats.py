def mean(sample):
    return sum(sample)/len(sample)

def var(sample, fix = True):
    sample_mean = mean(sample)
    sum = 0
    for i in sample:
        sum += (i - sample_mean) ** 2
    if fix:
        return sum / (len(sample) - 1)
    else:
        return sum / len(sample)

def std(sample, fix = True):
    return var(sample, fix) ** .5

def inputList():
    new_list = []
    count = 0
    op = ''
    def takeInput():
        nonlocal op, count
        op = input(str(count) + ': ')
        count += 1
        return op != ''
    while takeInput():
        new_list.append(float(op))
    return new_list

if __name__ == '__main__':
    from console import console
    global a
    a = inputList()
    console(globals())
