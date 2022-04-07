#
import numpy as np
import pandas as pd

from lapscore import *
from similar import *


def FeatureSelect(X,algorithm="cos",num=20): 
    ''' 
    X is the data matrix, rows are applications, columns are events
    algorithm is the similarity method to choose, 
        default is cosine simiarity, "cos" for short
    "js" is JS-divergence
    "wd" is Wasserstein distance
    "mh" is Mahalanobis distance
    num is the number of important features we want to keep
    ''' 

    Appname =X.index
    X = X.loc[:, (X != 0).any(axis=0)] #25*212
    column = [name for name in X.columns if not name.startswith("OFFCORE_RESPONSE")]

    #get rid of the 10 features which have some zero values
    somezero = ['FP_ARITH:128B_PACKED_DOUBLE', 'FP_ARITH:512B_PACKED_DOUBLE', 'FP_ARITH:128B_PACKED_SINGLE', 'SW_PREFETCH:NTA', 
    'FP_ARITH:512B_PACKED_SINGLE', 'CORE_POWER.LVL2_TURBO_LICENSE', 'FP_ASSIST:ANY', 'FP_ARITH:256B_PACKED_SINGLE',
     'UOPS_ISSUED:VECTOR_WIDTH_MISMATCH', 'FP_ARITH:256B_PACKED_DOUBLE']
    for c in somezero:
        column.remove(c) 
    print("column left",len(column))

    X = X[column]
    v = X.values
    g = "important features"

    print(X.shape)

    L=LaplacianScore(v,neighbour_size=2,t_param=1)  # 

    top_scores = feature_ranking(L)[:]
    # for score,f_name,ind in zip(L[top_scores],list(X.columns[feature_ranking(L)]),feature_ranking(L)):
    #     print(score,f_name,ind)
    data = {'score':L[top_scores],
            'index':feature_ranking(L),
            'feature_name':list(X.columns[feature_ranking(L)])}
    # df = pd.DataFrame(data)
    # df.to_csv("score.csv",index=False)  

    cor = X.corr()
    cor.columns = list(range(len(column)))
    cor.index = list(range(len(column)))

    cor=cor.abs()

    cor = cor.gt(0.9) & cor.ne(1)
    cor[0][1]

    visit=set()
    feature_set = []
    for i in feature_ranking(L):
        if i not in visit:
            feature_set.append(i)
            visit.add(i)
            for j in range(202):
                if j not in visit and cor[i][j]:
                    visit.add(j)
    print(len(feature_set))

    cc = [column[i] for i in feature_set[:num]] 
    if algorithm=="cos":
        simi_cosine(X[cc],"top "+ str(num)+ " important features")
    elif algorithm=="js":
        simi_JS(X[cc],"top "+ str(num)+ " important features")
    elif algorithm=="wd":
        simi_wd(X[cc],"top "+ str(num)+ " important features")
    elif algorithm=="mh":
        simi_pca_mahalanobis(X[cc],"top "+ str(num)+ " important features")
    


