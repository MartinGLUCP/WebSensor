import sys
import numpy as np
from sklearn.utils import check_array
from copy import copy
from MicroCluster import MicroCluster
from math import ceil
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from itertools import cycle, islice


class DenStream:

    def __init__(self, lambd=1, eps=1, beta=2, mu=2):
        """
        DenStream - Density-Based Clustering over an Evolving Data Stream with
        Noise.

        Parameters
        ----------
        lambd: float, optional
            The forgetting factor. The higher the value of lambda, the lower
            importance of the historical data compared to more recent data.
        eps : float, optional
            The maximum distance between two samples for them to be considered
            as in the same neighborhood.

        Attributes
        ----------
        labels_ : array, shape = [n_samples]
            Cluster labels for each point in the dataset given to fit().
            Noisy samples are given the label -1.

        Notes
        -----


        References
        ----------
        Feng Cao, Martin Estert, Weining Qian, and Aoying Zhou. Density-Based
        Clustering over an Evolving Data Stream with Noise.
        """
        self.lambd = lambd
        self.eps = eps
        self.beta = beta
        self.mu = mu
        self.t = 0
        self.p_micro_clusters = []
        self.o_micro_clusters = []
        if lambd > 0:
            self.tp = ceil((1 / lambd) * np.log((beta * mu) / (beta * mu - 1)))
        else:
            self.tp = sys.maxsize

    def partial_fit(self, X, y=None, sample_weight=None):
        """
        Online learning.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            Subset of training data

        y : Ignored

        sample_weight : array-like, shape (n_samples,), optional
            Weights applied to individual samples.
            If not provided, uniform weights are assumed.

        Returns
        -------
        self : returns an instance of self.
        """

        #X = check_array(X, dtype=np.float64, order="C")

        n_samples, _ = np.shape(X)#X.shape

        sample_weight = self._validate_sample_weight(sample_weight, n_samples)

        # if not hasattr(self, "potential_micro_clusters"):

        # if n_features != :
        # raise ValueError("Number of features %d does not match previous "
        # "data %d." % (n_features, self.coef_.shape[-1]))

        for sample, weight in zip(X, sample_weight):
            self._partial_fit(sample, weight)
        return self

    def fit_predict(self, X, y=None, sample_weight=None):
        """
        Lorem ipsum dolor sit amet

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            Subset of training data

        y : Ignored

        sample_weight : array-like, shape (n_samples,), optional
            Weights applied to individual samples.
            If not provided, uniform weights are assumed.

        Returns
        -------
        y : ndarray, shape (n_samples,)
            Cluster labels
        """

        """#X = check_array(X, dtype=np.float64, order="C")

        n_samples, _ = np.shape(X)

        sample_weight = self._validate_sample_weight(sample_weight, n_samples)

        # if not hasattr(self, "potential_micro_clusters"):

        # if n_features != :
        # raise ValueError("Number of features %d does not match previous "
        # "data %d." % (n_features, self.coef_.shape[-1]))
        count = 0
        plot_num = 1
        samples_visited = []
        for sample, weight in zip(X, sample_weight):
            count += 1
            self._partial_fit(sample, weight)
            samples_visited.append(sample)
            print("samples visited: ")
            print(samples_visited)
            print("sample: ")
            print(samples_visited)
            if (count%10)==0:
                p_micro_cluster_centers = np.array([p_micro_cluster.center() for
                                                p_micro_cluster in
                                                self.p_micro_clusters])
                p_micro_cluster_weights = [p_micro_cluster.weight() for p_micro_cluster in
                                       self.p_micro_clusters]
                dbscan = DBSCAN(eps=0.3)
                dbscan.fit(p_micro_cluster_centers,
                       sample_weight=p_micro_cluster_weights)

                y = []
                for sample in samples_visited:
                    index, _ = self._get_nearest_micro_cluster(sample,
                                                           self.p_micro_clusters)
                    y.append(dbscan.labels_[index])

        return y"""
        
        #X = check_array(X, dtype=np.float64, order="C")

        n_samples, _ = np.shape(X)

        sample_weight = self._validate_sample_weight(sample_weight, 15000)

        # if not hasattr(self, "potential_micro_clusters"):

        # if n_features != :
        # raise ValueError("Number of features %d does not match previous "
        # "data %d." % (n_features, self.coef_.shape[-1]))
        count = 0
        tab = np.array([[0,0]])
        dbscan = DBSCAN(eps=0.3)
        for sample, weight in zip(X, sample_weight):
            count += 1
            self._partial_fit(sample, weight)
            tab = np.append(tab,[sample],axis=0)
            #if (count%20) == 0:
            if count>20:
                print(tab)
                p_micro_cluster_centers = np.array([p_micro_cluster.center() for
                                                            p_micro_cluster in
                                                            self.p_micro_clusters])
                p_micro_cluster_weights = [p_micro_cluster.weight() for p_micro_cluster in
                                                   self.p_micro_clusters]
                print(p_micro_cluster_centers)
                print(p_micro_cluster_weights)
                dbscan.fit(p_micro_cluster_centers,sample_weight=p_micro_cluster_weights)

                y = []
                for sample in tab:
                    index, _ = self._get_nearest_micro_cluster(sample,
                                                                       self.p_micro_clusters)
                    y.append(dbscan.labels_[index])

                y[y == -1] = 6

                plt.subplot(5,5,count-20)
            
                plt.title(f"Etape {count-20}", size=10)

                colors = np.array(list(islice(cycle(['#377eb8', '#ff7f00', '#4daf4a',
                                                                     '#f781bf', '#a65628', '#984ea3',
                                                                     '#999999', '#e41a1c', '#dede00']),
                                                              int(max(y) + 1))))
                plt.scatter(tab[:, 0], tab[:, 1], s=10, color=colors[y])

                plt.xlim(-1, 5)
                plt.ylim(-1, 5)
                plt.xticks(())
                plt.yticks(())

                tab = np.delete(tab,0,axis=0)
        plt.show()
            
        return y

    def _get_nearest_micro_cluster(self, sample, micro_clusters):
        smallest_distance = sys.float_info.max
        nearest_micro_cluster = None
        nearest_micro_cluster_index = -1
        for i, micro_cluster in enumerate(micro_clusters):
            current_distance = np.linalg.norm(micro_cluster.center() - sample)
            if current_distance < smallest_distance:
                smallest_distance = current_distance
                nearest_micro_cluster = micro_cluster
                nearest_micro_cluster_index = i
        return nearest_micro_cluster_index, nearest_micro_cluster

    def _try_merge(self, sample, weight, micro_cluster):
        if micro_cluster is not None:
            micro_cluster_copy = copy(micro_cluster)
            micro_cluster_copy.insert_sample(sample, weight)
            if micro_cluster_copy.radius() <= self.eps:
                micro_cluster.insert_sample(sample, weight)
                return True
        return False

    def _merging(self, sample, weight):
        # Try to merge the sample with its nearest p_micro_cluster
        _, nearest_p_micro_cluster = \
            self._get_nearest_micro_cluster(sample, self.p_micro_clusters)
        success = self._try_merge(sample, weight, nearest_p_micro_cluster)
        if not success:
            # Try to merge the sample into its nearest o_micro_cluster
            index, nearest_o_micro_cluster = \
                self._get_nearest_micro_cluster(sample, self.o_micro_clusters)
            success = self._try_merge(sample, weight, nearest_o_micro_cluster)
            if success:
                if nearest_o_micro_cluster.weight() > self.beta * self.mu:
                    del self.o_micro_clusters[index]
                    self.p_micro_clusters.append(nearest_o_micro_cluster)
            else:
                # Create new o_micro_cluster
                micro_cluster = MicroCluster(self.lambd, self.t)
                micro_cluster.insert_sample(sample, weight)
                self.o_micro_clusters.append(micro_cluster)

    def _decay_function(self, t):
        return 2 ** ((-self.lambd) * (t))

    def _partial_fit(self, sample, weight):
        self._merging(sample, weight)
        if self.t % self.tp == 0:
            self.p_micro_clusters = [p_micro_cluster for p_micro_cluster
                                     in self.p_micro_clusters if
                                     p_micro_cluster.weight() >= self.beta *
                                     self.mu]
            Xis = [((self._decay_function(self.t - o_micro_cluster.creation_time
                                          + self.tp) - 1) /
                    (self._decay_function(self.tp) - 1)) for o_micro_cluster in
                   self.o_micro_clusters]
            self.o_micro_clusters = [o_micro_cluster for Xi, o_micro_cluster in
                                     zip(Xis, self.o_micro_clusters) if
                                     o_micro_cluster.weight() >= Xi]
        self.t += 1

    def _validate_sample_weight(self, sample_weight, n_samples):
        """Set the sample weight array."""
        if sample_weight is None:
            # uniform sample weights
            sample_weight = np.ones(n_samples, dtype=np.float64, order='C')
        else:
            # user-provided array
            sample_weight = np.asarray(sample_weight, dtype=np.float64,
                                       order="C")
        if sample_weight.shape[0] != n_samples:
            raise ValueError("Shapes of X and sample_weight do not match.")
        return sample_weight


#data = np.random.random([1000, 5]) * 1000
X = np.array([[0,1.1],[0.1,0.8],[-0.05,1.15],[1.1,1],[1,0.1],[1,1.1],[0,0],[0.1,0.1],[0.15,0.1],
              [0,0.1],[0.1,0],[0.1,0.1],[2,0],[0,4],[0,4],[0,0.9],[0.2,1.3],[-0.2,1.1],
              [1,-0.1],[1.1,0],[1,0.9],[0.1,1],[0.8,0.9],[1,0],[0.9,1],[-0.1,0.95],
              [1.1,1.1],[1,0],[1,1],[1.1,0.1],[0.9,0.1],[0.8,-0.1],[0.9,0.1],[0.8,-0.1],
              [0.9,0.1],[0.75,-0.05],[0.95,0.1],[0.8,-0.15],[0.9,0.15],[0.85,-0.1],[0.9,0.1],
              [0.8,-0.1],[1,3],[0,4]])
clusterer = DenStream(lambd=0.01, eps=0.22, beta=0.25, mu=10) #beta et mu a changer
#for row in X:
    #clusterer.partial_fit([row])
    #print(f"Number of p_micro_clusters is {len(clusterer.p_micro_clusters)}")
    #print(f"Number of o_micro_clusters is {len(clusterer.o_micro_clusters)}")
#for a in clusterer.p_micro_clusters:
#    print(str(a.creation_time) +' '+str(a.mean))
y_pred = clusterer.fit_predict(X)


