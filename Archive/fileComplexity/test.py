from time import perf_counter
from math import log
from matplotlib import pyplot as plt

def main():
    x = []
    y = []
    for j in range(6):
        for i in range(30):
            size = 2 ** i
            start = perf_counter()
            with open(f'{i}.data', 'rb+') as f:
                f.seek(size - 1)
                f.write(b'o')
                f.seek(size - 1)
                f.write(b'k')
            end = perf_counter()
            x.append(i)
            y.append(log(end - start))
            print(x[-1], y[-1])
    plt.plot(x, y, 'o')
    plt.show()

main()
