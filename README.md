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
Clone the repository to your computing platform. $ git clone https://github.com/SimBioSysLab/SimEngine

Then, if you want to process the raw data, go to step A. If you want to start from the processed CSV files, go to step B

## A. Start from the raw data
This step will create the accumulated CSV and delta CSV by following the below instructions:     
1- Copy the raw data inside your machine.  
2- Go to the dataprocess directory in the repo.  
&nbsp;&nbsp; a. $ cd dataprocess  
3- Open dataprep.sh shell file and change the TopDataPrep variable (at the beginning of the file) to point to the raw data directory.   
4- Perform $ chmod +x dataprep.sh  
5- Run the shell file ./dataprep.sh to get two csv directories csv_acc and csv_std, inside the dataprocess directory, that contains the all ranks average and standard deviation data. Notice, this step may take a long time (e.g. one or two days) to build two csv directories.  
6- Follow steps in B.       

## B. Use the existing CSV directory to analysis  
1- Go to the SimEngine directory in the top of the repo.  $ cd SimEngine/  
2- $ python main.py  
3- You can find the analysis output figures inside the graphs directory.


