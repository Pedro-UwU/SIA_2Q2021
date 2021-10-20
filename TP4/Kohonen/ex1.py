import csv

import numpy as np

import newKohonen
from matplotlib import pyplot as plt

def main():
    file = open('./files/europe.csv')
    reader = csv.reader(file)
    names = []
    data = []
    next(reader)
    for line in reader:
        names.append(line[0])
        data.append([float(x) for x in line[1:8]])
    data = np.array(data)
    kohonen = newKohonen.newKohonen(input_size=6, data=data, data_headers=names, grid_size=4, radius=2)
    kohonen.train()
    results = kohonen.test()
    locations = {}
    for i, row in enumerate(results):
        for j, col in enumerate(row):
            for cname in col:
                if not (i, j) in locations:
                    locations[(i, j)] = []
                locations[(i, j)].append(cname)
    for coor in locations:
        print(f'{coor}: {locations[coor]}')
    heat_map(results)
    weights(kohonen)
    pass

def heat_map(results):
    results_count = np.zeros(results.shape)
    for i in range(results_count.shape[0]):
        for j in range(results_count.shape[1]):
            results_count[i, j] = len(results[i, j])
    plt.imshow(results_count)
    for i in range(results_count.shape[0]):
        for j in range(results_count.shape[1]):
            plt.text(j, i, int(results_count[i, j]), ha='center', va='center', color='white')
    plt.title('Cantidad de registros por nodo')
    plt.show()


def get_neighbors(W, i, j):
    n = []
    for ii in range(max(0, i-1), min(W.shape[0], i+2)):
        for jj in range(max(0, j-1), min(W.shape[1], j+2)):
            if ii == i and jj == j:
                continue
            n.append(W[ii,jj].copy())
    return np.array(n)


def weights(network):
    W = network.W
    distances = np.zeros(W.shape)
    for i in range(W.shape[0]):
        for j in range(W.shape[1]):
            neighbors = get_neighbors(W, i, j)
            total = 0
            count = 0
            for n in neighbors:
                dist = np.linalg.norm(n-W[i,j])
                total += dist
                count += 1
            distances[i, j] = total/count
    plt.imshow(distances, cmap='Reds')
    plt.title('Distancia promedio entre los pesos de cada celda con sus vecinos')
    for i in range(W.shape[0]):
        for j in range(W.shape[1]):
            plt.text(j, i, round(distances[i, j]*100)/100, ha='center', va='center', color='black')
    plt.show()



if __name__ == '__main__':
    main()