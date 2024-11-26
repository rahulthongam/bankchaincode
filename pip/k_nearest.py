import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn import datasets

#Load data in X

X, y_true=make_blobs(n_samples=300, centers=4,cluster_std=0.50,random_state=0)

db = DBSCAN(eps=0.3,min_samples=10).fit(X)
core_samples_mask =np.zeros_like(db.labels_,dtype=bool)
