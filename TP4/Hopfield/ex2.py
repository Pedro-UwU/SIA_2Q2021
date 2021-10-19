import csv
import random

import numpy as np

from Config import Config
from Hopfield import Hopfield


def main():
    Config.init_config('../config.conf')
    file = open('numbers.csv', 'r')
    reader = csv.reader(file)
    patterns = []
    letters = []
    all_patterns = []
    all_letters = []
    for line in reader:
        all_patterns.append([int(x) for x in line[1:26]])
        all_letters.append(line[0])
    for letter in Config.config.ex2_patterns:
        index = all_letters.index(letter)
        patterns.append(all_patterns[index])
        letters.append(letter)

    for i, p in enumerate(patterns):
        for j, p2 in enumerate(patterns):
            p = np.array(p)
            p2 = np.array(p2)
            result = np.dot(p, p2)
            print(f'Letter {letters[i]} and letter {letters[j]} have a dot product value of: {result}')
    if Config.config.ex2_show_saved_patterns:
        for i, p in enumerate(patterns):
            Hopfield.show_pattern(p, f'Saved Pattern {i}')

    hopfield = Hopfield(25, patterns)
    # hopfield.query([1 if random.random() > 0.5 else -1 for _ in range(25)])
    for i in range(Config.config.ex2_total_tests):
        random_pattern = random.choice(patterns).copy()
        for j in range(len(random_pattern)):
            if random.random() > 0.85:
                if random_pattern[j] == -1:
                    random_pattern[j] = 1
                else:
                    random_pattern[j] = -1
        Hopfield.show_pattern(random_pattern, f'Pattern with Noise - Test {i}')
        Hopfield.show_pattern(hopfield.query(random_pattern, show=Config.config.ex2_show_steps, title=f'Intermediate - Test {i}'), f'Minimum found - Test {i}')


    # for i in range(Config.config.ex2_total_tests):
    #     random_pattern = random.choice(patterns).copy()
    #     for j in range(len(random_pattern)):
    #         if random_pattern[j] == -1:
    #             random_pattern[j] = 1
    #         else:
    #             random_pattern[j] = -1
    #     hopfield.query(random_pattern, f'Test {i}')


if __name__ == '__main__':
    main()