from aco_func import ACO, Graph
from plot import plot
import math

def distance(city1: dict, city2: dict):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2 + (city1['z'] - city2['z']) ** 2)

def aco():
    cities = []
    points = []
    index = 1
    with open('./dataset/star100.xyz') as f:
        for line in f.readlines():
            city = line.split(' ')
            cities.append(dict(index=int(index), x=float(city[0]), y=float(city[1]), z=float(city[2])))
            points.append((float(city[0]), float(city[1]), float(city[2])))
            index += 1
    cost_matrix = []
    rank = len(cities)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distance(cities[i], cities[j]))
        cost_matrix.append(row)
    aco = ACO(100, 100, 1.0, 10.0, 0.5, 10, 2)
    graph = Graph(cost_matrix, rank)
    path, cost = aco.solve(graph)
    print('cost: {}, path: {}'.format(cost, path))
    plot(points, path)
