#!/bin/bash


#Step 1
# Compute an average for each event for each application across 128 ranks.
# Save new time series into two new directories.
# Directory acc is the accumulated hardware events counts.
# Directory del is the delta hardware events counts (per second)

TopDataPrep={path to the raw data}
pathdirs=$(ls $TopDataPrep)
mkdir -p ./acc
mkdir -p ./del
for dirname in $pathdirs
do
	if [[ $dirname == SKX* ]]
	then 
		mkdir -p "./acc/"$dirname
		mkdir -p "./del/"$dirname
		filenames=$(ls $TopDataPrep$dirname)
		for file in $filenames
			do
				python average128accu.py $TopDataPrep$dirname"/"$file "./acc/"$dirname"/"${file:7}
			        python average128deletemax.py $TopDataPrep$dirname"/"$file "./del/"$dirname"/"${file:7}
	
			done
	fi
done

# Step 2
# Since we ran every application 5 times.
# Average the last five seconds for the application execution across 5 runs for each event.
# Save the result in new directory output in directory ./acc and ./del seperately

adirs=$(ls ./acc)
appnames="ExaMiniMD LAMMPS sw4lite sw4 SWFFT HACC MiniQMC QMCPack miniVite vite Nekbone Nek5000 XSBench openmc picsarlite picsar amg2013 Castro Laghos pennant snap hpcc_dgemm hpcc_random hpcc_streams hpcg "

for dirname in $adirs
do
        if [[ $dirname == SKX* ]]
                then
                        for app in $appnames
                                do
                                        python average5new.py "./acc/"$dirname $app "./acc/output"  
                                        python average5std.py "./del/"$dirname $app "./del/output"

                                done
                fi
done


# Step 3
# Build csv for overall features and subgroup features
# Save the result in new directory ./csv_acc and csv_std
# ./csv_acc is the final average, csv_std is the standard deviation 
python buildcsv.py ./acc/output ../Calder/csv_acc
python buildcsv.py ./del/output ../Calder/csv_std
