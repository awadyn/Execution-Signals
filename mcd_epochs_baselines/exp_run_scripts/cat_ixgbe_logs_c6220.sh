#!/bin/bash

dir=$1

for i in {0..15}; do
	cat /proc/ixgbe_stats/core/$i | cut -d ' ' -f 3,6,7,8,9,17 > $dir/core_$i;
done
