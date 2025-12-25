#*******************
#file.csv columns: *
#*******************
#[itrd, dvfs, peak_qps, pkg_joules, avg_read, std_read, 90th_read, 95th_read, 99th_read]
#
#
#------------- ITRD: 400 -- QPS: 100000 -- DVFS: 0x1c00
##type       avg     std     min     5th    10th    90th    95th    99th
#read      284.8   173.1    45.3    97.7   118.5   446.7   475.2   521.8
#update    288.3   192.8    45.3    99.8   121.9   450.0   477.1   523.7
#op_q        1.2     0.4     1.0     1.0     1.0     2.0     2.1     2.9
#
#Total QPS = 99918.1 (2997543 / 30.0s)
#
#Misses = 0 (0.0%)
#Skipped TXs = 0 (0.0%)
#
#RX  515820609 bytes :   16.4 MB/s
#TX  331455800 bytes :   10.5 MB/s
#
#
#rapl readings: 1821377859 1903515244  --  763572545 839606499
#pkg0: 82137385 -- pkg1: 76033954 -- sum: 158171339
#rapl readings: 1869243225 1925876253  --  883174580 934157836
#pkg0: 56633028 -- pkg1: 50983256 -- sum: 107616284
#
#--------------------------------


import sys

if len(sys.argv) < 3:
    print("****** Usage: python3", sys.argv[0], "<input lat_joules.txt file> <output summary_lat_joules.csv file>")
    sys.exit(1)

file_txt = sys.argv[1]
file_csv = sys.argv[2]

with open(file_txt, 'r') as file:
    lines = file.readlines()

out_csvs = "itrd,dvfs,peak_qps,pkg_joules,avg_read,std_read,90th_read,95th_read,99th_read\n"
for i in range(0, len(lines)):
        if "ITRD: " in lines[i]:
            out = lines[i:i+19]
            out_csv = ""
            
            settings = out[0].split()
            out_csv = out_csv + settings[2] + "," + settings[8] + ","

            qps = out[6].split()
            out_csv = out_csv + qps[3] + ","

            joules = out[-3].split()
            joules_val = int(joules[-1]) * 0.000061
            out_csv = out_csv + str(joules_val) + ","

            lats = out[2].split()
            out_csv = out_csv + lats[1] + "," + lats[2] + "," + lats[6] + "," + lats[7] + "," + lats[8]
            out_csvs = out_csvs + out_csv + "\n"

            i = i + 19
print(out_csvs)

with open(file_csv, 'w') as file:
    file.write(out_csvs)
