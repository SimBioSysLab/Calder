#
import os
import numpy as np
from collections import Counter,defaultdict
import pandas as pd
import random
from statistics import mean
import math
import json
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors 
import matplotlib.patheffects as PathEffects
from itertools import cycle,islice
from time import time
from sklearn.manifold import MDS,TSNE
from sklearn.decomposition import PCA,KernelPCA
from sklearn.cluster import DBSCAN,KMeans,AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity,euclidean_distances,pairwise_distances
from sklearn.preprocessing import MinMaxScaler,StandardScaler,Normalizer
from sklearn import metrics
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial import distance
from scipy.stats import wasserstein_distance,zscore
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import svds, eigs
from scipy.sparse import *

def simi_cosine(X,f):
    ''' 
    X is the data matrix, rows are applications, columns are events
    f is the path for X, used for graph title 
    '''  
    Appname =X.index
    X = X.loc[:, (X != 0).any(axis=0)] #drop the zero columns does not change much
    t1 = time()
    cosX = cosine_similarity(X)
    t2 = time()
    print("cost time:",t2-t1)
    cosX=np.round(cosX,decimals=6)  #(np.min(cosX),np.max(cosX))=0.4749522451634041 1.000000000000001

    degree = [list(map(lambda x: math.degrees (math.acos (x)),line)) for line in cosX] #show the degree of cosine

    plt.figure(figsize=(24,18))
    sns.set(font_scale=2.5)

    sns.set_style("ticks")

    # lower triangular heatmap with diagnal
    mask = np.ones_like(degree)
    mask[np.tril_indices_from(mask)] = False

    ax = sns.heatmap(degree,mask=mask,annot=True,annot_kws={'size':20},fmt=".0f",cbar=True,linewidths=.5,cmap="RdYlGn_r",vmax=90, vmin=0) #only show the integer instead of float
    ax.set_yticklabels(Appname,rotation=0) 
    ax.set_xticklabels(Appname, ha="right",rotation=40) 
    ax.set_title("sky cosine similarity "+f)
    plt.savefig("sky cosine similarity "+f)


def simi_JS(X,f):
    ''' 
    X is the data matrix, rows are applications, columns are events
    f is the path for X, used for graph title 
    ''' 
    Appname =X.index
    X_value = X.values
    jsd=[[0]*len(X) for _ in range(len(X_value))]
    t1 = time()
    for i in range(len(X_value)):
        for j in range(len(X_value)):
            jsd[i][j]=distance.jensenshannon(X_value[i],X_value[j])*100
    t2 = time()
    print("cost time:",t2-t1)

    plt.figure(figsize=(24,18))
    sns.set(font_scale=2.5)
    sns.set_style("ticks")

    mask = np.ones_like(jsd)
    mask[np.tril_indices_from(mask)] = False
    ax = sns.heatmap(jsd,mask=mask,annot=True,fmt='.0f',annot_kws={'size':20},cbar=True,linewidths=.5,cmap="RdYlGn_r",vmax=90,vmin=0)
    ax.set_yticklabels(Appname,rotation=0) 
    ax.set_xticklabels(Appname, ha="right",rotation=40) 
    ax.set_title("sky JS-divergence "+f)
    plt.savefig("sky JS-divergence "+f)  
    

def simi_wd(X,f):
    ''' 
    X is the data matrix, rows are applications, columns are events
    f is the path for X, used for graph title 
    ''' 
    Appname =X.index
    X_value = X.values
    wd=[[0]*len(X) for _ in range(len(X_value))]
    t1 = time()
    for i in range(len(X_value)):
        for j in range(len(X_value)):
            wd[i][j]=wasserstein_distance(X_value[i],X_value[j])*1000
    t2 = time()
    print("cost time:",t2-t1)

    plt.figure(figsize=(24,18))
    sns.set(font_scale=2.5)
    sns.set_style("ticks")
    mask = np.ones_like(wd)
    mask[np.tril_indices_from(mask)] = False
    ax = sns.heatmap(wd,mask=mask,annot=True,fmt='.0f',annot_kws={'size':20},cbar=True,linewidths=.5,cmap="RdYlGn_r",vmax=90,vmin=0)
    
    
    ax.set_yticklabels(Appname,rotation=0) 
    ax.set_xticklabels(Appname, ha="right",rotation=40) 
    ax.set_title("sky Wasserstein distance "+f)
    plt.savefig("sky Wasserstein distance "+f)  

def simi_pca_mahalanobis(X,f):
    ''' 
    X is the data matrix, rows are applications, columns are events
    f is the path for X, used for graph title 
    ''' 
    Appname =X.index
    X_value = X.values

    md=[[0]*len(X) for _ in range(len(X_value))]
    X_reduced = PCA(n_components=0.95).fit_transform(X_value) #n_components should be between 0 and min(n_samples, n_features)=7 with svd_solver='full'
    t1=time()
    mmd = distance.pdist(X_reduced,'mahalanobis')
    
    k=0
    for i in range(len(X_value)):
        for j in range(i+1,len(X_value)):
            md[i][j]=md[j][i]= mmd[k]*10
            k+=1
    t2=time()
    print("cost time:",t2-t1)
    plt.figure(figsize=(24,18))
    sns.set(font_scale=2.5)
    sns.set_style("ticks")
    mask = np.ones_like(md)
    mask[np.tril_indices_from(mask)] = False
    ax = sns.heatmap(md,mask=mask,annot=True,fmt='.0f',annot_kws={'size':20},cbar=True,linewidths=.5,cmap="RdYlGn_r",vmax=90,vmin=0)
    
    ax.set_yticklabels(Appname,rotation=0) 
    ax.set_xticklabels(Appname, ha="right",rotation=40) 
    ax.set_title("sky pca + Mahalanobis "+f)
    plt.savefig("sky pca + Mahalanobis "+f) 

def simi_kpca_cosine(X,f):
    ''' 
    X is the data matrix, rows are applications, columns are events
    f is the path for X, used for graph title 
    ''' 
    Appname =X.index
    X_value = X.values
    kpca=KernelPCA(n_components=6,kernel="rbf", fit_inverse_transform=True, gamma=10)
    X_reduced = kpca.fit_transform(X_value)

    cosX = cosine_similarity(X_reduced)

    cosX[cosX > 1] = 1  #(np.min(cosX),np.max(cosX))=0.4749522451634041 1.000000000000001
    # print(cosX)
    degree = [list(map(lambda x: math.degrees (math.acos (x)),line)) for line in cosX] #show the degree of cosine
    plt.figure(figsize=(12,9))
    sns.set(font_scale=1.2)
    sns.set_style("ticks")
    ax = sns.heatmap(degree,annot=True,fmt=".0f",cbar=False,linewidths=.5,cmap="RdYlGn_r",vmax=120, vmin=0) #only show the integer instead of float
    ax.set_yticklabels(Appname,rotation=0) 
    ax.set_xticklabels(Appname, ha="right",rotation=40) 
    ax.set_title("sky kpac + cosine "+f) 
    plt.savefig("sky kpac + cosine "+f)   

def simi_hierachical(X,f):
    ''' 
    X is the data matrix, rows are applications, columns are events
    f is the path for X, used for graph title 
    ''' 
    Appname =X.index
    t1 = time()
    linked = linkage(X, 'single')
    t2 = time()
    print("cost time:",t2-t1)
    labelList = list(Appname)

    plt.figure(figsize=(10, 7))
    dendrogram(linked,
                orientation='top',
                labels=labelList,
                distance_sort='descending',
                show_leaf_counts=True)
    plt.xticks(fontsize=20,ha='right')
    plt.title("sky hierachical "+f)
    plt.savefig("sky hierachical "+f)