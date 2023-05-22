import collections
import os
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics

from sklearn.cluster import KMeans, MeanShift, DBSCAN,estimate_bandwidth

import logging
from optparse import OptionParser
import sys

import numpy as np
from pymongo import MongoClient

from testNLP import *
from connectMongo import *

from time import time

# parse commandline arguments
op = OptionParser()
op.add_option("--use-mongodb",
              action="store_true", dest="use_mongodb", default=False,
              help="Enable mongodb for the dataset.")
op.add_option("--bandwith", type=float, default=None,
              help="If specify, use the value for the bandwith (lenght),"
              "option in MeanShift.")
op.add_option("--dbscan",
              action="store_true", dest="dbscan", default=False,
              help="Use DBSCAN algorithm .")
op.add_option("--no-vocabulary",
              action="store_true", dest="no_vocabulary", default=False,
              help="Use vocabulary for tfidf vectorizer .")
op.add_option("--use-hyperparameters",
              action="store_true", dest="use_hyperparameters", default=False,
              help="Use hyperparameters for algorithm .")
op.add_option("--eps", type=float, default = 0.3,
              help="If specify, use the value for the epsilon ,"
              "option in dbscan.")
op.add_option("--min-samples",dest="min_samples", type=int, default = 5,
              help="If specify, use the value for the min-samples ,"
              "option in dbscan.")
op.add_option("--n-features", type=int, default=300,
              help="Maximum number of features (dimensions)"
                   " to extract from text.")
op.add_option("--verbose",
              action="store_true", dest="verbose", default=False,
              help="Print progress reports inside algorithm.")

op.print_help()


def is_interactive():
    return not hasattr(sys.modules['__main__'], '__file__')

def subject(sentence,features):
        subject =""
        tokens = normalize_corpus(sentence)
        for i in range(len(features)):
                if features[i] in tokens :
                        subject += features[i] + " "
                else:
                    if "stad france" in tokens or "stad" in tokens :
                        subject += "stade france" + " "
        return subject

# work-around for Jupyter notebook and IPython console
argv = [] if is_interactive() else sys.argv[1:]
(opts, args) = op.parse_args(argv)
if len(args) > 0:
    op.error("this script takes no arguments.")
    sys.exit(1)

# #############################################################################
# categories from the training set
categories = [
    'coronavirus',
    'peinture',
    'danse',
    'prince charles',
    'magasin',
    'stad france',
    'spectacle'
]


#True number of expecting clusters

true_k = len(categories)
true_labels_ = []

t0 = time()

if opts.use_mongodb:
    dataset = selectAll()

    print("Extraction mongodb %fs" % (time() - t0))
else :
    dataset = []
    l = 0
    for i in categories :
            for j in range(100) :
                    dataset.append(i)
                    true_labels_.append(l)
            l+=1
    for i in range(10):
            dataset.append('coronavirus danse')
            true_labels_.append(l)
    l+=1
    for i in range(10):
            dataset.append('prince charles coronavirus')
            true_labels_.append(l)
    l+=1
    for i in range(10):
            dataset.append('prince charles coronavirus stade france')
            true_labels_.append(l)

print("Extracting features from the training dataset = ",len(dataset),"using a sparse vectorizer")

# #############################################################################
# Create the true labels array

# #############################################################################

#tfidf_vectorizer = TfidfVectorizer(tokenizer=normalize_corpus,ngram_range=(1,2),binary= True, norm = None, use_idf = False,vocabulary=categories)
#tfidf_vectorizer = TfidfVectorizer(tokenizer=normalize_corpus,ngram_range=(1,2),binary= True, norm = None, use_idf = False,max_features=opts.n_features)

if opts.use_mongodb and not opts.no_vocabulary:
    #voc = ['prince charles', 'prince charles coronavirus stad france', 'coronavirus', 'coronavirus danse', 'coronavirus stad france', 'danse', 'magasin', 'peinture', 'prince charles coronavirus', 'spectacle', 'stad france']
    tfidf_vectorizer = TfidfVectorizer(tokenizer=normalize_corpus,ngram_range=(1,4),vocabulary=categories)
elif opts.use_mongodb and opts.no_vocabulary:
    tfidf_vectorizer = TfidfVectorizer(tokenizer=normalize_corpus,ngram_range=(1,4),max_features=opts.n_features)
else :
    tfidf_vectorizer = TfidfVectorizer(tokenizer=normalize_corpus,ngram_range=(1,4))



X = tfidf_vectorizer.fit_transform(dataset).toarray()
vocabulary = tfidf_vectorizer.get_feature_names()
print("")
print("done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X.shape)
print(vocabulary)
print("")

# #############################################################################
# Do the actual clustering
_S=[]
_S_eps=[]
_S_min_samples=[]
_S_leaf_size = []

_H=[]
_AR=[]

_HP=[]
_HP_eps=[]
_HP_min_samples=[]
_HP_leaf_size = []

_NB_CLUSTER = []
_NB_CLUSTER_eps = []
_NB_CLUSTER_min_samples = []
_NB_CLUSTER_leaf_size = []

_BV=[]

bandwidth = 0.1
eps = 0.1
min_samples = 5
leaf_size = 1
max_s=0

print("")

if opts.dbscan:
    if opts.use_hyperparameters:
        ml = DBSCAN(eps=opts.eps, min_samples=opts.min_samples)
        print("")
        print("Clustering sparse data with %s" % ml)
        print("")
        t0 = time()
        ml.fit(X)
    else:
        t0 = time()
        while eps < 2.0:
            _HP_eps.append(eps)
            ml = DBSCAN(eps=eps)
            
            ml.fit(X)
            n_clusters_ = len(set(ml.labels_)) - (1 if -1 in ml.labels_ else 0)
            _NB_CLUSTER_eps.append(n_clusters_)
            if n_clusters_ > 1:
                s=metrics.silhouette_score(X, ml.labels_)
                _S_eps.append(s)
            else :
                _S_eps.append(0)
                
            """
            if not opts.use_mongodb:
                h=metrics.v_measure_score(true_labels_, ml.labels_)
                ar=metrics.adjusted_rand_score(true_labels_, ml.labels_)
                _H.append(h)
                _AR.append(ar)
            """
            
            eps+=0.1
        
        ind = _S_eps.index(max(_S_eps))
        _BV.append(_HP_eps[ind])
        
        while min_samples < 50:
            _HP_min_samples.append(min_samples)
            
            ml = DBSCAN(eps=_BV[0], min_samples=min_samples)
            
            ml.fit(X)
            n_clusters_ = len(set(ml.labels_)) - (1 if -1 in ml.labels_ else 0)
            _NB_CLUSTER_min_samples.append(n_clusters_)
            if n_clusters_ > 1:
                s=metrics.silhouette_score(X, ml.labels_)
                _S_min_samples.append(s)
            else :
                _S_min_samples.append(0)
            
            min_samples+=5
            
        ind = _S_min_samples.index(max(_S_min_samples))
        _BV.append(_HP_min_samples[ind])

        while leaf_size < 5:
            _HP_leaf_size.append(leaf_size)
            ml = DBSCAN(eps=_BV[0], min_samples=_BV[1],leaf_size=leaf_size)
            
            ml.fit(X)
            n_clusters_ = len(set(ml.labels_)) - (1 if -1 in ml.labels_ else 0)
            _NB_CLUSTER_leaf_size.append(n_clusters_)
            if n_clusters_ > 1:
                s=metrics.silhouette_score(X, ml.labels_)
                _S_leaf_size.append(s)
            else :
                _S_leaf_size.append(0)
            
            leaf_size+=1
            
        ind = _S_leaf_size.index(max(_S_leaf_size))
        _BV.append(_HP_leaf_size[ind])

        ml = DBSCAN( eps=_BV[0],min_samples=_BV[1],leaf_size=_BV[2])
        print("")
        print("Clustering sparse data ",_BV," with %s" % ml)
        print("")
        ml.fit(X)
else:
    if opts.use_hyperparameters and not opts.dbscan:
        ml = MeanShift(bandwidth=opts.bandwith)
        print("")
        print("Clustering sparse data with %s" % ml)
        print("")
        t0 = time()
        ml.fit(X)
    else :
        t0 = time()
        while bandwidth < 2.0:
            _HP.append(bandwidth)
            ml = MeanShift(bandwidth=bandwidth)
            
            ml.fit(X)
            n_clusters_ = len(set(ml.labels_)) - (1 if -1 in ml.labels_ else 0)
            _NB_CLUSTER.append(n_clusters_)
            if n_clusters_ > 1:
                s=metrics.silhouette_score(X, ml.labels_)
                _S.append(s)
            else :
                s=0
                _S.append(0)
            if not opts.use_mongodb:
                h=metrics.v_measure_score(true_labels_, ml.labels_)
                ar=metrics.adjusted_rand_score(true_labels_, ml.labels_)
                _H.append(h)
                _AR.append(ar)
            
                if s > 0.9 and h > 0.9 and ar > 0.9:
                    Best_Value = bandwidth
            
            bandwidth+=0.1
        ind = _S.index(max(_S))
        Best_Value = _HP[ind]
        #Best_Value
        ml = MeanShift(bandwidth=Best_Value)
        print("")
        print("Clustering sparse data with %s" % ml)
        print("")
        ml.fit(X)

# Number of clusters in labels, ignoring noise if present (work for dbscan).
n_clusters_ = len(set(ml.labels_)) - (1 if -1 in np.unique(ml.labels_) else 0)
n_noise_ = list(ml.labels_).count(-1)
print("")
print("done in %0.3fs" % (time() - t0))
print(np.unique(ml.labels_))
print("")
print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)
#print('Best Value For Hyperparameter: %d' %Best_Value)
if n_clusters_ > 1:
    print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, ml.labels_))
if opts.use_mongodb == False:
    print("Homogeneity: %0.3f" % metrics.homogeneity_score(true_labels_, ml.labels_))
    print("Completeness: %0.3f" % metrics.completeness_score(true_labels_, ml.labels_))
    print("V-measure: %0.3f" % metrics.v_measure_score(true_labels_, ml.labels_))
    print("Adjusted Rand-Index: %.3f" % metrics.adjusted_rand_score(true_labels_, ml.labels_))

print()


clusters = collections.defaultdict(list)
for i, label in enumerate(ml.labels_):
    clusters[label].append(i)

total_data = {key :0 for key in range(n_clusters_)}
total_feature = {}
pourcentage = {key :[] for key in range(n_clusters_) }

clusters = dict(clusters)
for cluster in range(n_clusters_):
    for i,sentence in enumerate(clusters[cluster]):
        w=subject(dataset[sentence],vocabulary)
        if total_feature.get(w) == None :
                total_feature[w] = 1
                total_data[cluster]+=1
        else :
                total_feature[w] += 1
                total_data[cluster]+=1
                
    pourcentage[cluster].append(total_feature.copy())
    
    total_feature.clear()

   
for cluster in pourcentage :
    for key in pourcentage[cluster] :
        for char in key :
                key[char] = "{:.1f}".format((key[char]/total_data[cluster])*100)
                

print("")
zz = 0
while os.path.exists("quantity_%s.txt" % zz):
    zz += 1

z=""

for cluster in pourcentage :
    z += "cluster"+str(cluster)+" : "+str(pourcentage[cluster])+" % for "+str(total_data[cluster])+" tweets in the cluster"+"\n"
    print("cluster",cluster," : ",pourcentage[cluster]," % for ",total_data[cluster]," tweets in the cluster")


file = open("quantity_%s.txt" % zz, "a")
file.write(str(ml))
file.write(z)
file.write("Silhouette score for each sample : ")
file.write(str(metrics.silhouette_samples(X, ml.labels_)))
file.close()

print("")


# #############################################################################
# Plot result
if not opts.use_hyperparameters and not opts.use_mongodb and opts.dbscan:
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2)
    axs[0].plot(_HP_eps,_S_eps,label="Epsilon",linewidth=2)
    print(_HP_eps,_S_eps)
    axs[0].set(xlabel="Epsilon")
    axs[0].set(ylabel="Silhouette score")
    axs[0].legend()
    axs[1].bar(_HP_eps,_NB_CLUSTER_eps,label="Number of Cluster",width=0.02)
    axs[1].set(xlabel="Epsilon")
    axs[1].set(ylabel="Number of Clusters")
    plt.legend()
    fig.suptitle('Estimated number of clusters for best epsilon value: %d' % n_clusters_)
    
    fig1, axs1 = plt.subplots(2)
    axs1[0].plot(_HP_min_samples,_S_min_samples,label="min_samples",linewidth=2)
    print(_HP_min_samples,_S_min_samples)
    axs1[0].set(xlabel="min_samples")
    axs1[0].set(ylabel="Silhouette score")
    axs1[0].legend()
    axs1[1].bar(_HP_min_samples,_NB_CLUSTER_min_samples,label="Number of Cluster")
    axs1[1].set(xlabel="min_samples")
    axs1[1].set(ylabel="Number of Clusters")
    plt.legend()
    fig1.suptitle('Estimated number of clusters for best min_samples value: %d' % n_clusters_)

    fig2, axs2 = plt.subplots(2)
    axs2[0].plot(_HP_leaf_size,_S_leaf_size,label="leaf_size",linewidth=2)
    
    axs2[0].set(xlabel="leaf_size")
    axs2[0].set(ylabel="Silhouette score")
    axs2[0].legend()
    axs2[1].bar(_HP_leaf_size,_NB_CLUSTER_leaf_size,label="Number of Cluster",width=0.1)
    axs2[1].set(xlabel="leaf_size")
    axs2[1].set(ylabel="Number of Clusters")
    plt.legend()
    fig2.suptitle('Estimated number of clusters for best leaf_size value: %d' % n_clusters_)
    
    plt.show()

elif not opts.use_hyperparameters and opts.use_mongodb and opts.dbscan:
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2)
    axs[0].plot(_HP_eps,_S_eps,label="Epsilon",linewidth=2)
    print(_HP_eps,_S_eps)
    axs[0].set(xlabel="Epsilon")
    axs[0].set(ylabel="Silhouette score")
    axs[0].legend()
    axs[1].bar(_HP_eps,_NB_CLUSTER_eps,label="Number of Cluster",width=0.02)
    axs[1].set(xlabel="Epsilon")
    axs[1].set(ylabel="Number of Clusters")
    plt.legend()
    fig.suptitle('Estimated number of clusters for best epsilon value: %d' % n_clusters_)
    
    fig1, axs1 = plt.subplots(2)
    axs1[0].plot(_HP_min_samples,_S_min_samples,label="min_samples",linewidth=2)
    print(_HP_min_samples,_S_min_samples)
    axs1[0].set(xlabel="min_samples")
    axs1[0].set(ylabel="Silhouette score")
    axs1[0].legend()
    axs1[1].bar(_HP_min_samples,_NB_CLUSTER_min_samples,label="Number of Cluster")
    axs1[1].set(xlabel="min_samples")
    axs1[1].set(ylabel="Number of Clusters")
    plt.legend()
    fig1.suptitle('Estimated number of clusters for best min_samples value: %d' % n_clusters_)

    fig2, axs2 = plt.subplots(2)
    axs2[0].plot(_HP_leaf_size,_S_leaf_size,label="leaf_size",linewidth=2)
    
    axs2[0].set(xlabel="leaf_size")
    axs2[0].set(ylabel="Silhouette score")
    axs2[0].legend()
    axs2[1].bar(_HP_leaf_size,_NB_CLUSTER_leaf_size,label="Number of Cluster",width=0.1)
    axs2[1].set(xlabel="leaf_size")
    axs2[1].set(ylabel="Number of Clusters")
    plt.legend()
    fig2.suptitle('Estimated number of clusters for best leaf_size value: %d' % n_clusters_)
    
    plt.show()
    
elif not opts.use_hyperparameters and not opts.use_mongodb:
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2)
    axs[0].plot(_HP,_S,label="Silhouette score",linewidth=2)
    print(_HP,_S)
    #axs[0].plot(_HP,_H,label="V measure score",linewidth=2)
    #axs[0].plot(_HP,_AR,label="Arranged Rand Index score",linewidth=2)
    axs[0].set(xlabel="bandwidth")
    axs[0].set(ylabel="Silhouette score")
    axs[0].legend()
    axs[1].bar(_HP,_NB_CLUSTER,label="Number of Cluster",width=0.02)
    axs[1].set(xlabel="bandwidth")
    axs[1].set(ylabel="Number of Clusters")
    plt.legend()
    fig.suptitle('Estimated number of clusters for best value: %d' % n_clusters_)
    plt.show()

elif not opts.use_hyperparameters and opts.use_mongodb:
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2)
    axs[0].plot(_HP,_S,label="Silhouette score",linewidth=2)
    print(_HP,_S)
    axs[0].set(xlabel="bandwidth")
    axs[0].set(ylabel="Silhouette score")
    axs[0].legend()
    axs[1].bar(_HP,_NB_CLUSTER,label="Number of Cluster",width=0.02)
    axs[1].set(xlabel="bandwidth")
    axs[1].set(ylabel="Number of Clusters")
    plt.legend()
    fig.suptitle('Estimated number of clusters: %d' % n_clusters_)
    plt.show()
