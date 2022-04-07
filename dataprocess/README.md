# How to run SimEngine
If you want to process the raw data, go to step A. If you want to start from the processed CSV files, go to step B

# A.Start from the raw data
If you want to process the raw data,start from here.
# Create the accumulated CSV and delta CSV
1 Open dataprep.sh, change TopDataPrep (at the beginning of the file) to {path to the raw data} 
2 chmod +x dataprep.sh
3 ./dataprep.sh # It may take a long time (e.g. a day)to build two csv directory (csv_acc and csv_del)
 
# B.Use the existing CSV directory to analysis

