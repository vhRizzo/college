import operator

import matplotlib.pyplot as plt
import numpy  as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

def plot(points, path: list):
    xyz = [[0 for _ in range(3)] for _ in range(100)]

    X = []
    Y = []
    Z = []
    for i in range(0, len(path)):
        if (i < len(path)):
            # print(path[i])
            # print(points[path[i]][0])
            xyz[i][0] = points[path[i]][0]
            xyz[i][1] = points[path[i]][1]
            xyz[i][2] = points[path[i]][2]
        # else:
        #     xyz[i][0] = points[path[0]-1][0]
        #     xyz[i][1] = points[path[0]-1][1]
        #     xyz[i][2] = points[path[0]-1][2]
    ax = plt.axes(projection='3d')
    X= [sub[0] for sub in xyz]
    Y= [sub[1] for sub in xyz]
    Z= [sub[2] for sub in xyz]
    ax.plot(X, Y, Z, color='g', alpha=0.3)
    X.pop(X.index(0.0))
    Y.pop(Y.index(0.0))
    Z.pop(Z.index(0.0))
    ax.scatter(0, 0, 0, color='red')
    ax.scatter(X, Y, Z, color='Green')
    plt.show()
    #         xyz[i, 0] = points[path[0]-1, 0]
    #         xyz[i, 1] = points[path[0]-1, 1]
    #         xyz[i, 2] = points[path[0]-1, 2]

    # ax = plt.axes(projection='3d')
    # X= xyz[:,0]
    # Y= xyz[:,1]
    # Z= xyz[:,2]
    # ax = plt.axes(projection='3d')
    
    # ax.plot(X, Y, Z, color='g', alpha=0.3)
    # X= np.delete(X,np.where(X == 0.0))
    # Y= np.delete(Y,np.where(Y == 0.0))
    # Z= np.delete(Z,np.where(Z == 0.0))
    # ax.scatter(0, 0, 0, color='red')
    # ax.scatter(X, Y, Z, color='Green')
    # plt.show()
