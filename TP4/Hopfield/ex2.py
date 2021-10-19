import csv
import random

from Hopfield import Hopfield


def main():
    file = open('numbers.csv', 'r')
    reader = csv.reader(file)
    patterns = []
    for line in reader:
        patterns.append([int(x) for x in line[1:26]])
    hopfield = Hopfield(25, patterns)
    # hopfield.query([1 if random.random() > 0.5 else -1 for _ in range(25)])
    for i in range(6):
        random_pattern = random.choice(patterns).copy()
        for j in range(len(random_pattern)):
            if random.random() > 0.85:
                if random_pattern[j] == -1:
                    random_pattern[j] = 1
                else:
                    random_pattern[j] = -1
        hopfield.query(random_pattern, title=f'Test {i}')


if __name__ == '__main__':
    main()