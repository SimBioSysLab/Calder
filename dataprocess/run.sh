#!/bin/bash

path=/research/file_system_traces/attaway_run_Cosine_08132021/
pathdirs=$(ls $path)
for dirname in $pathdirs
do
        if [[ $dirname == SKX_M* ]]
	then 
		mkdir $dirname
		echo $dirname >> pathdirs.txt
	
		filenames=$(ls $path$dirname)
		for file in $filenames
			do
				python average128accu.py $path$dirname"/"$file $dirname"/"${file:7} >> output112.txt

			done
	fi
done

mkdir output

path=./
pathdirs=$(ls $path)
appnames="ExaMiniMD LAMMPS sw4lite sw4 SWFFT HACC MiniQMC QMCPack miniVite vite Nekbone Nek5000 XSBench openmc picsarlite picsar amg2013 Castro Laghos pennant snap hpcc_dgemm hpcc_random hpcc_streams hpcg "

for dirname in $pathdirs
do
        if [[ $dirname == SKX* ]]
                then
                        for app in $appnames
                                do
                                        python average5new.py $dirname $app

                                done
                fi
done

mkdir csv
python buildcsv.py
