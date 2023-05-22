import numpy as np
import pandas as pd
from sklearn.cluster import MeanShift
from sklearn.datasets import make_blobs
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets
from dbconn import *
import json

features = "sport foot stade football athletisme basketball natation cyclisme golf handball equitation judo karate marathon rugby ski taekwondo volleyball superbowl match coupe championnat attentat tremblement concert exposition explosion festival terroriste election fete cirque gala oscar cesar congre forum ceremoni convention spectacle theatr politique trianon vote election accident mort sortie album cinema film coronaviru viru maladie epidemie pandemie nouveau solde carnaval france europe monde national regionnal zenith olympia bataclan hippodrome cinema"
F = features.split(" ")

dico={}
   
    
selectVectors = selectVectors()
V = []
for row in selectVectors:
    r=row[1].split("ARRAY")
    res = json.loads(r[1])
    V.append(res)

v = 0
i = 0

for vector in V :
    for feature in vector :
        if feature == 1 :
            
            if v in dico :
                dico[v] += F[i] + " "
            else :
                dico[v] = F[i] + " "
            i+=1
    v+=1
    i=0
print(v)

X = np.array(V)

ms = MeanShift()
ms.fit(X)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

l = list(labels)

for i in range(len(l)) :
    print(l[i],dico[l[i]])

"""
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X[:,0], X[:,1], X[:,2], marker='o')
ax.scatter(cluster_centers[:,0], cluster_centers[:,1], cluster_centers[:,2], marker='x', color='red', s=300, linewidth=5, zorder=10)
plt.show()


##plt.scatter(X[:,0], X[:,1], s=150)
##plt.show()

colors = 10*["g","r","c","b","k"]

class Mean_Shift:
    def __init__(self, radius=4):
        self.radius = radius

    def fit(self, data):
        centroids = {}

        for i in range(len(data)):
            centroids[i] = data[i]
        
        while True:
            new_centroids = []
            for i in centroids:
                in_bandwidth = []
                centroid = centroids[i]
                for featureset in data:
                    if np.linalg.norm(featureset-centroid) < self.radius:
                        in_bandwidth.append(featureset)

                new_centroid = np.average(in_bandwidth,axis=0)
                new_centroids.append(tuple(new_centroid))

            uniques = sorted(list(set(new_centroids)))

            prev_centroids = dict(centroids)

            centroids = {}
            for i in range(len(uniques)):
                centroids[i] = np.array(uniques[i])

            optimized = True

            for i in centroids:
                if not np.array_equal(centroids[i], prev_centroids[i]):
                    optimized = False
                if not optimized:
                    break
                
            if optimized:
                break

        self.centroids = centroids



clf = Mean_Shift()
clf.fit(X)

centroids = clf.centroids

plt.scatter(X[:,0], X[:,1], s=150)

for c in centroids:
    plt.scatter(centroids[c][0], centroids[c][1], color='k', marker='*', s=150)

plt.show()
"""
