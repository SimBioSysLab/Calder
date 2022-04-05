#!/bin/bash


#Step 1
# Compute an average for each event for each application across 128 ranks.
# Save new time series into new directories.

TopDataPrep={path to the raw data}
pathdirs=$(ls $TopDataPrep)
for dirname in $pathdirs
do
        if [[ $dirname == SKX* ]]
	then 
		mkdir $dirname
		filenames=$(ls $TopDataPrep$dirname)
		for file in $filenames
			do
				python average128accu.py $path$dirname"/"$file $dirname"/"${file:7} 
			done
	fi
done

# Step 2
# Since we ran every application 5 times.
# Average the last five seconds for the application execution across 5 runs for each event.
# Save the result in new directory: output
mkdir output
pdirs=$(ls)
appnames="ExaMiniMD LAMMPS sw4lite sw4 SWFFT HACC MiniQMC QMCPack miniVite vite Nekbone Nek5000 XSBench openmc picsarlite picsar amg2013 Castro Laghos pennant snap hpcc_dgemm hpcc_random hpcc_streams hpcg "

for dirname in $pdirs
do
        if [[ $dirname == SKX* ]]
                then
                        for app in $appnames
                                do
                                        python average5new.py $dirname $app

                                done
                fi
done

# Step 3
# Build csv for overall features and subgroup features
# Save the result in new directory: csv

mkdir csv
python buildcsv.py
