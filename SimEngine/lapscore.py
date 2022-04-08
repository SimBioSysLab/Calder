##
import numpy as np
from scipy.sparse import *
from sklearn.metrics.pairwise import pairwise_distances
def construct_W(X, **kwargs):
    k=kwargs['neighbour_size']
    t = kwargs['t_param']
    n_samples, n_features = np.shape(X)

    D = pairwise_distances(X)
    D **= 2
    # sort the distance matrix D in ascending order
    dump = np.sort(D, axis=1)
    idx = np.argsort(D, axis=1)
    idx_new = idx[:, 0:k+1]
    dump_new = dump[:, 0:k+1]
    # compute the pairwise heat kernel distances
    dump_heat_kernel = np.exp(-dump_new/(2*t*t))
    G = np.zeros((n_samples*(k+1), 3))
    G[:, 0] = np.tile(np.arange(n_samples), (k+1, 1)).reshape(-1)
    G[:, 1] = np.ravel(idx_new, order='F')
    G[:, 2] = np.ravel(dump_heat_kernel, order='F')
    # build the sparse affinity matrix W
    W = csc_matrix((G[:, 2], (G[:, 0], G[:, 1])), shape=(n_samples, n_samples))
    bigger = np.transpose(W) > W
    W = W - W.multiply(bigger) + np.transpose(W).multiply(bigger)
    return W

  
def LaplacianScore(X, **kwargs):
    """
    This function implements the laplacian score feature selection, steps are as follows:
    1. Construct the affinity matrix W if it is not specified
    2. For the r-th feature, we define fr = X(:,r), D = diag(W*ones), ones = [1,...,1]', L = D - W
    3. Let fr_hat = fr - (fr'*D*ones)*ones/(ones'*D*ones)
    4. Laplacian score for the r-th feature is score = (fr_hat'*L*fr_hat)/(fr_hat'*D*fr_hat)
    Input
    -----
    X: {numpy array}, shape (n_samples, n_features)
        input data
    kwargs: {dictionary}
        W: {sparse matrix}, shape (n_samples, n_samples)
            input affinity matrix
    Output
    ------
    score: {numpy array}, shape (n_features,)
        laplacian score for each feature
    Reference
    ---------
    He, Xiaofei et al. "Laplacian Score for Feature Selection." NIPS 2005.
    https://github.com/jundongl/scikit-feature
    """

    # if 'W' is not specified, use the default W
    if 'W' not in kwargs.keys():
        if 't_param' not in kwargs.keys():
            t=1
        else:
            t = kwargs['t_param']
        
        if 'neighbour_size' not in kwargs.keys():
            n=2
        else:
            n=kwargs['neighbour_size']
            
        W = construct_W(X,t_param=t,neighbour_size=n)
    else:
    # construct the affinity matrix W
        W = kwargs['W']
    # build the diagonal D matrix from affinity matrix W
    D = np.array(W.sum(axis=1))
    L = W
    tmp = np.dot(np.transpose(D), X)
    D = diags(np.transpose(D), [0])
    Xt = np.transpose(X)
    t1 = np.transpose(np.dot(Xt, D.todense()))
    t2 = np.transpose(np.dot(Xt, L.todense()))
    tmp=np.multiply(tmp, tmp)/D.sum()
    # compute the numerator of Lr
    D_prime = np.sum(np.multiply(t1, X), 0) - tmp
    # compute the denominator of Lr
    L_prime = np.sum(np.multiply(t2, X), 0) - tmp
    # avoid the denominator of Lr to be 0
    D_prime[D_prime < 1e-12] = 10000

    # compute laplacian score for all features
    score = 1 - np.array(np.multiply(L_prime, 1/D_prime))[0, :]
    return np.transpose(score)


def feature_ranking(score):
    """
    Rank features in ascending order according to their laplacian scores, the smaller the laplacian score is, the more
    important the feature is
    """
    idx = np.argsort(score, 0)
    return idx
