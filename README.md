# SimEngine
SimEngine is an open-source similarity measurement and feature selection repository in Python. It is build upon several standard math libraries(e.g. math, Numpy) and machine learning libraries (scikit-learn, Scipy).  
SimEngine could be used to determine the similarity between proxy and parent applications. It also includes algorithms to facilitate feature selection, as minimizing the number of features is very important to reduce the data collected and thus lower the number of application runs.  
With the help of the quantitative similarity measurement we have developed in SimEngine, users are guided to choose proper proxy applications for particular uses. Besides quantifying fidelity of proxy applications, similarity measurement approaches in SimEngine can also be applied to various HPC problems, such as compiler optimization, code refactoring, and application input sensitivity.  

# Prerequisites:
Python 3  
Numpy  
Scipy  
Scikit-learn  

# How to run SimEngine
If you want to process the raw data, go to step A. If you want to start from the processed CSV files, go to step B

## A.Start from the raw data
Create the accumulated CSV and delta CSV
1 Go to directory dataprocess. Open dataprep.sh, change TopDataPrep (at the beginning of the file) to {path to the raw data}  
2 chmod +x dataprep.sh  
3 ./dataprep.sh  Notice, it may take a long time (e.g. one or two days)to build two csv directory (csv_acc and csv_del)    

## B.Use the existing CSV directory to analysis
1 Go to directory engine  
2 python main.py  


