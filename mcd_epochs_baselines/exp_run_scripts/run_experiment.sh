#!/bin/bash

dir=$1

for qps in "400000" "800000" "1400000"; do
	for update in "0.25" "0.50" "0.75" ; do
		echo "Running memcached experiment... QPS: $qps -- update: $update"
		./run_multi_itrd_dvfs_ixgbe_c6220.sh "10.10.1.2" "enp5s0f0" "$dir" "$qps" "$update" > $dir/lat_joules_16_cores_c6220_qps_"$qps"_update_"$update".txt
	
		for itrd in 10 100; do 
			for dvfs in 0xc00 0x1c00; do 
				subdir=$dir/sets_$update/qps_$qps/itrd_$itrd\_dvfs_$dvfs/
				echo "Merging logs... ITRD: $itrd -- DVFS: $dvfs"
				python2.7 merge_per_core_interrupt_logs_c6220.py $subdir $subdir/merged_by_timestamp.csv
				echo "Parsing Epochs... ITRD: $itrd -- DVFS: $dvfs"
				python2.7 parse_epochs_per_delta_time.py $subdir/merged_by_timestamp.csv $subdir/epochs_per_0.01s.csv
				echo "Parsing Active Cores... ITRD: $itrd -- DVFS: $dvfs"
				python2.7 parse_active_cores_per_delta_time.py $subdir/merged_by_timestamp.csv $subdir/active_cores.csv
				echo "Parsing Active Cores Deltas... ITRD: $itrd -- DVFS: $dvfs"
				python2.7 parse_active_cores_deltas.py $subdir/active_cores.csv
			done
		done
	done
done


for update in "0.25" "0.50" "0.75"; do
	subdir=$dir/sets_$update/
	echo "Plotting epochs per qps.. update: $update"
	python2.7 plot_epochs_per_qps.py $subdir $update 10 0xc00  
	python2.7 plot_epochs_per_qps.py $subdir $update 10 0x1c00  
	python2.7 plot_epochs_per_qps.py $subdir $update 100 0xc00  
	python2.7 plot_epochs_per_qps.py $subdir $update 100 0x1c00  
#	# TODO fix
#	python2.7 plot_epochs_active_cores_deltas.py $subdir $update 100 0x1c00
done
	
for qps in "400000" "800000" "1400000"; do
	echo "Plotting epochs per workload.. qps: $qps"
	subdir=qps_"$qps"/
	python2.7 plot_epochs_per_update.py $dir $subdir 10 0xc00
	python2.7 plot_epochs_per_update.py $dir $subdir 10 0x1c00
	python2.7 plot_epochs_per_update.py $dir $subdir 100 0xc00
	python2.7 plot_epochs_per_update.py $dir $subdir 100 0x1c00
done


