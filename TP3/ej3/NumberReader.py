def get_numbers():
    file = open('./numeros.txt', 'r')
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
