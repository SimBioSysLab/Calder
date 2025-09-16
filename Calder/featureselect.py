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

    # Manually remove some features based on prior knowledge or experts
    column = [name for name in X.columns if not name.startswith("OFFCORE_RESPONSE")]
    #Get rid of the 10 features that some parent applications have zero values(std==0).(get these from std.py zero_column)
    somezero = ['FP_ARITH:128B_PACKED_DOUBLE', 'FP_ARITH:512B_PACKED_DOUBLE', 'FP_ARITH:128B_PACKED_SINGLE', 'SW_PREFETCH:NTA', 
    'FP_ARITH:512B_PACKED_SINGLE', 'CORE_POWER.LVL2_TURBO_LICENSE', 'FP_ASSIST:ANY', 'FP_ARITH:256B_PACKED_SINGLE',
     'UOPS_ISSUED:VECTOR_WIDTH_MISMATCH', 'FP_ARITH:256B_PACKED_DOUBLE']
    for c in somezero:
        column.remove(c) 
    print("column left",len(column))

    X = X[column]
    v = X.values
    print(X.shape)

    # Feature ranking
    L=LaplacianScore(v,neighbour_size=2,t_param=1)  # set neighbour 2 because we assume our cluster size is two (one proxy and one parents)

    top_scores = feature_ranking(L)[:]
    # for score,f_name,ind in zip(L[top_scores],list(X.columns[feature_ranking(L)]),feature_ranking(L)):
    #     print(score,f_name,ind)
    data = {'score':L[top_scores],
            'index':feature_ranking(L),
            'feature_name':list(X.columns[feature_ranking(L)])}
    # df = pd.DataFrame(data)
    # df.to_csv("score.csv",index=False)  

    # Correlation filter
    cor = X.corr()
    cor.columns = list(range(len(column)))
    cor.index = list(range(len(column)))

    #Remove features with correlation bigger than 0.9
    cor=cor.abs()
    cor = cor.gt(0.9) & cor.ne(1)

    visit=set()
    feature_set = []
    for i in feature_ranking(L):
        if i not in visit:
            feature_set.append(i)
            visit.add(i)
            for j in range(X.shape[1]):
                if j not in visit and cor[i][j]:
                    visit.add(j)
    print(len(feature_set))

    #Only keep the "num" of top uncorrelated features
    cc = [column[i] for i in feature_set[:num]] 

    # Test similarity matrix using the top features that we choose
    if algorithm=="cos":
        simi_cosine(X[cc],"top "+ str(num)+ " important features")
    elif algorithm=="js":
        simi_JS(X[cc],"top "+ str(num)+ " important features")
    elif algorithm=="wd":
        simi_wd(X[cc],"top "+ str(num)+ " important features")
    elif algorithm=="mh":
        simi_pca_mahalanobis(X[cc],"top "+ str(num)+ " important features")
    


