import csv
import numpy as np

def get_total_cross(patterns, i1, i2, i3, i4):
    p = []
    p.append(np.array(patterns[i1]))
    p.append(np.array(patterns[i2]))
    p.append(np.array(patterns[i3]))
    p.append(np.array(patterns[i4]))
    total = 0
    for i in range(4):
        for j in range(4):
            if i == j: continue
            total += abs(np.dot(p[i], p[j]))
    return total

def get_minimum():
    file = open('numbers.csv', 'r')
    reader = csv.reader(file)
    all_patterns = []
    all_letters = []
    for line in reader:
        all_patterns.append([int(x) for x in line[1:26]])
        all_letters.append(line[0])

    min_sum = None
    min_letters = None
    for i1, l1 in enumerate(all_letters):
        print(f'First Letter: {l1}')
        for i2, l2 in enumerate(all_letters):
            if i1 == i2: continue
            for i3, l3 in enumerate(all_letters):
                if i1 == i3 or i2 == i3: continue
                for i4, l4 in enumerate(all_letters):
                    if i1 == i4 or i2 == i4 or i3 == i4: continue
                    cum_cross = get_total_cross(all_patterns, i1, i2, i3, i4)
                    if min_sum is None or cum_cross < min_sum:
                        min_sum = cum_cross
                        min_letters = [l1, l2, l3, l4]

    return min_sum, min_letters

if __name__ == '__main__':
    min_s, min_let = get_minimum()
    print(f'letters: {min_let}, min: {min_s}')