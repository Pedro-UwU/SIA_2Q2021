import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def main():
    total_components = 3
    headers, raw_data = read_data('europe.csv')
    countries = raw_data[:, 0]

    scaled_data = scale_data(raw_data)
    pca = PCA(n_components=total_components)
    transform = pca.fit_transform(scaled_data)
    components = pca.components_.T

    write_components(components, headers, total_components)
    write_new_data(countries, transform, total_components)
    write_variance_ratio(pca.explained_variance_ratio_, total_components)

    biplot(transform, countries, components, headers)


def read_data(file_name: str):
    df = pd.read_csv(file_name, sep=',', header=0)
    return df.columns.values, df.values


def scale_data(raw_data):
    scaled_data = np.zeros((len(raw_data), len(raw_data[0]) - 1))
    for i in range(1, len(raw_data[0])):
        data = StandardScaler().fit_transform(raw_data[:, i].reshape(-1, 1))
        scaled_data[:, i - 1] = data[:, 0]
    return scaled_data


def write_components(components, headers, total_components):
    output_file = open('components.csv', 'w')

    head = 'Features'
    for i in range(total_components):
        head += f',PC{i}'
    head += "\n"
    output_file.write(head)

    for i in range(len(components)):
        line = headers[i + 1]
        for j in components[i]:
            line += f',{j}'
        line += "\n"
        output_file.write(line)
    output_file.close()


def write_new_data(countries, transform, total_components):
    output_file = open('new_data.csv', 'w')

    head = 'Countries'
    for i in range(total_components):
        head += f',PC{i}'
    head += "\n"
    output_file.write(head)

    for i in range(len(countries)):
        line = countries[i]
        for j in transform[i]:
            line += f',{j}'
        line += "\n"
        output_file.write(line)
    output_file.close()


def write_variance_ratio(ratio, total_components):
    output_file = open('variance_ratio.csv', 'w')

    head = 'Ratios'
    for i in range(total_components):
        head += f',PC{i}'
    head += "\n"
    output_file.write(head)

    line1 = 'Individual'
    line2 = 'Cumulative'
    cum_sum = 0
    for i in ratio:
        line1 += f',{i}'
        cum_sum += i
        line2 += f',{cum_sum}'
    line1 += "\n"
    line2 += "\n"
    output_file.write(line1)
    output_file.write(line2)
    output_file.close()

def biplot(data, countries, components, names):
    x = data[:, 0]  # PC0
    y = data[:, 1]  # PC1
    plt.scatter(x, y)
    for i, country in enumerate(countries):
        plt.annotate(country, (x[i], y[i]), size=7, color='b')
    print(components)
    scl = 5
    for i, name in enumerate(names):
        if i == 0:
            continue
        x_coord = components[i-1][0]  # PC0
        y_coord = components[i-1][1]  # PC1
        print(f'{x_coord=}, {y_coord=}')
        plt.arrow(0, 0, x_coord*scl, y_coord*scl, color='r', alpha=0.5)
        plt.text(x_coord*scl*1.1, y_coord*scl*1.1, name, color='r', size=7)

    plt.xlabel("PC0")
    plt.ylabel("PC1")
    plt.title('Principal Components Analysis')
    plt.grid()
    plt.show()

if __name__ == '__main__':
    main()
