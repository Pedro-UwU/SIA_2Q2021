import os
def get_numbers():
    dirname = os.path.dirname(__file__)
    number_file = os.path.join(dirname, './numeros.txt')
    file = open(number_file, 'r')
    lines = file.readlines()
    file.close()
    numbers = []
    for i in range(10):
        digits = []
        number = i
        for j in range((i * 7), (i * 7 + 7)):
            for c in lines[j]:
                if c == '0' or c == '1':
                    digits.append(int(c))
        numbers.append((number, digits.copy()))
    return numbers
