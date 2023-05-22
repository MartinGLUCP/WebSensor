import numpy as np
import pandas as pd
from sklearn.cluster import MeanShift
from sklearn.datasets import make_blobs
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets

#iris = datasets.load_iris()
#X = iris.data

#X = np.array([[1,1,1,1,1,0],[1, 1, 0,1,1,1], [1, 1, 0,0,1,1], [1, 0, 1,1,1,0],
#             [0, 0, 1,0,0,1], [0,1, 0,0,0,1], [0, 0, 0,0,0,0],[0, 0, 0,0,0,1],
#             [0, 1, 0,1,0,1], [0, 1, 1,1,0,1], [1, 0, 0, 0,0,1], [0, 0, 1,1,1,1]])

X = np.array([[1,0,0,0,0,0,0],[1,0,0,0,0,0,0],[0, 1, 0,0,0,0,0],[0, 1, 0,0,0,0,0],[0, 1, 0,0,0,0,0], [0, 0, 1,0,0,0,0],
              [0, 0, 1,0,0,0,0],[0, 0, 1,0,0,0,0],[0, 0, 1,0,0,0,0],[0, 0, 1,0,0,0,0],[0, 0, 0,1,0,0,0],
             [0, 0, 1,0,0,0,1], [0, 0, 0,0,0,0,0],[1, 1, 0,0,0,1,0],
             [0,1,1,1,1,1,0],[0, 1, 0,1,0,0,1]])

ms = MeanShift()
ms.fit(X)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

print(labels)

#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.scatter(X[:,0], X[:,1], X[:,2], marker='o')
#ax.scatter(cluster_centers[:,0], cluster_centers[:,1], cluster_centers[:,2], marker='x', color='red', s=300, linewidth=5, zorder=10)
#plt.show()