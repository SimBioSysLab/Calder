#
import os
import numpy as np
import pandas as pd

from similar import *
from featureselect import *
from std import *

if __name__ == "__main__":
    
    # In groupss, allapps means all the features, the others are the subgroup names.
    groupss = ["allapps","Branch","DecodeIssue_Pipeline","Dispatch_Pipeline","Execution_Pipeline",
          "Frontend","Instruction_Cache","Instruction_Mix","L1_D_Cache",
          "L2_D_Cache","L3_D_Cache","Memory_Pipeline","Misc","Power","Retirement_Pipeline",
          "Memory"]

    # Using different similarity algorithms to show similarity matrices using all features
    for g in groupss[:1]:
        f = "csv/SKX_"+g+".csv"
        X = pd.read_csv(f,header = 0,index_col=0)   
        simi_cosine(X,g)
        simi_JS(X,g)
        simi_wd(X,g)
        simi_pca_mahalanobis(X,g)

    #Using cosine similarity to show similarity matrices in subgroup features
    for g in groupss[1:]:
        f = "csv/SKX_"+g+".csv"
        X = pd.read_csv(f,header = 0,index_col=0)   
        simi_cosine(X,g)


    allapps = "csv/SKX_allapps.csv"
    stdfile = "csv/SKX_allapps_std.csv"   

    X_std = pd.read_csv(stdfile,header = 0,index_col=0)
    X = pd.read_csv(allapps,header = 0,index_col=0)

    # Rank and select the top uncorrelated features
    FeatureSelect(X,"cos")

    # Find the unique features that contribute to the dissimilarity of the proxy and parent pairs
    StandardDeviation(X,X_std)
    



