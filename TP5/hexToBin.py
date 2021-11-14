import csv
def main():
    f = open('data/group1.csv')
    output_f = open('data/group1_format.csv', 'w')
    reader = csv.reader(f)
    for line in reader:
        new_line = ""
        for i, digit in enumerate(line):
            if i != 8-1:
                bi_rep = bin(int(digit, 16))[2:]
                bi_rep = bi_rep.zfill(5)
                for bit in bi_rep:
                    new_line += f'{bit},'
            else:
                new_line += digit
        print(new_line)

        output_f.write(new_line + "\n")

if __name__ == '__main__':
    main()