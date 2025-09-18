# Calder
Calder is an open-source similarity measurement and feature selection repository in Python. It is build upon several standard math libraries(e.g. math, Numpy) and machine learning libraries (scikit-learn, Scipy).  
Calder could be used to determine the similarity between proxy and parent applications. It also includes algorithms to facilitate feature selection, as minimizing the number of features is very important to reduce the data collected and thus lower the number of application runs.  
With the help of the quantitative similarity measurement we have developed in Calder, users are guided to choose proper proxy applications for particular uses. Besides quantifying fidelity of proxy applications, similarity measurement approaches in Calder can also be applied to various HPC problems, such as compiler optimization, code refactoring, and application input sensitivity.  

# Prerequisites:
Python 3.9.23  
Numpy 1.26.4 
Scipy 1.13.1 
Scikit-learn 1.6.1  
pandas 1.4.4
seabon 0.13.2

# How to run Calder
Clone the repository to your computing platform. $ git clone https://github.com/SimBioSysLab/Calder

Alternatively, you can start with docker container: docker pull meditates/calder

Then, if you want to process the raw data, go to step A. If you want to start from the processed CSV files, go to step B

## A. Start from the raw data
This step will create the accumulated CSV and delta CSV by following the below instructions:     
1- Go to the dataprocess directory in the repo.  
&nbsp;&nbsp; a. $ cd dataprocess  
2- Open dataprep.sh shell file and change the TopDataPrep variable (at the beginning of the file) to point to the raw data directory. Default raw data repository is ../data, which has 2 example files inside. We are working on releasing the rest of the database which is ~300GB.  
3- Perform $ chmod +x dataprep.sh  
4- Run the shell file ./dataprep.sh to get two csv directories csv_acc and csv_std, inside the Calder directory, that contains the all ranks average and standard deviation data. Notice, this step may take a long time (e.g. one or two days) to build two csv directories.  
5- Follow steps in B.       

## B. Use the processed CSV directory to analysis  
1- Go to the Calder directory in the top of the repo.  $ cd Calder/  
2- $ python main.py  
3- You can find the analysis output figures inside the graphs directory.


