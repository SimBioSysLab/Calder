#
import os
import numpy as np
import pandas as pd

from similar import *
from featureselect import *
from std import *

if __name__ == "__main__":
    
    groupss = ["allapps","Branch","DecodeIssue_Pipeline","Dispatch_Pipeline","Execution_Pipeline",
          "Frontend","Instruction_Cache","Instruction_Mix","L1_D_Cache",
          "L2_D_Cache","L3_D_Cache","Memory_Pipeline","Misc","Power","Retirement_Pipeline",
          "Memory"]
    for g in groupss[:]:
        f = "csv/SKX_"+g+".csv" 
        X = pd.read_csv(f,header = 0,index_col=0)   
        simi_cosine(X,f)
        # simi_JS(X,f)
        # simi_wd(X,f)
        # simi_pca_mahalanobis(X,f)

    allapps = "csv/SKX_allapps.csv"
    stdfile = "csv/SKX_allapps_std.csv"   

    X_std = pd.read_csv(stdfile,header = 0,index_col=0)
    X = pd.read_csv(allapps,header = 0,index_col=0)

    FeatureSelect(X,"cos")

    StandardDeviation(X,X_std)
    



