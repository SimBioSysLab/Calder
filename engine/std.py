#
import pandas as pd
import numpy as np

def StandardDeviation(X,X_std,std_n=2):
    """
    X is the matrix of accumulated data set(mean value)
    X_std is the matrix of std data (standard divation for each events for each application)
    std_n is the number of standard deviation proxy applicaiton different from the parents application, default is 2.
    """
    column = [name for name in X.columns if not name.startswith("OFFCORE_RESPONSE")]
    X = X[column]
    X_std = X_std[column]
    Appname =X.index
    X_std = X_std.loc[:, (X_std != 0).any(axis=0)] #drop the zero columns does not change much
    X = X.loc[:, (X != 0).any(axis=0)]
    print(X.shape)
    print(X_std.shape)

    zero_column=set()
    std_features=set()
    for i in range(0,15,2):
        print("----application pairs: ",Appname[i],Appname[i+1])
        zero_std = X_std.iloc[i+1:i+2,:].values==0
        zero_std_features = list(X.columns[zero_std[0]])
        # print("zero std features:",zero_std_features)
        for c in zero_std_features:
            zero_column.add(c)

        div_std = np.absolute(X.iloc[i:i+1,:].values- X.iloc[i+1:i+2,:].values)/ X_std.iloc[i+1:i+2,:].values > std_n
        div_std_features = list(X.columns[div_std[0]])
        exclude_zero_std = [item for item in div_std_features if item not in zero_std_features]
        print("div bigger than "+str(std_n)+" std features ",len(exclude_zero_std),exclude_zero_std)
        for d in exclude_zero_std:
            std_features.add(d)

    # The features that some parent applications have zero values(std==0)
    print(len(zero_column),zero_column) 
     # All the unique features that contribute to the dissimilarity of the proxy and parent pairs
    print(len(std_features),std_features)
                


