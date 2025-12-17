import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

exp_dir = sys.argv[1]

TIME_CONVERSION_khz = 1./(2899999*1000)

epochs_dfs = {}
for qps_dir in os.listdir(exp_dir):
    qps = qps_dir.split('_')[1]
    df = pd.read_csv(exp_dir + qps_dir + "/itrd_100_dvfs_0x1900/epochs_per_ref_core.csv", index_col=0)
    epochs_dfs[qps] = df

fig = plt.figure(figsize=(20,12))
frame_size = 100
legend = []
qpses = [int(qps) for qps in epochs_dfs.keys()]
for qps in sorted(qpses):
#    if qps == "100000" or qps == "200000" or qps == "400000" or qps == "600000":
#        continue
    df = epochs_dfs[str(qps)]
    durations = df["duration"] * TIME_CONVERSION_khz
    durations_means = []
    durations_medians = []
    ctr = 0
    while True:
        frame = durations[ctr:ctr+frame_size]
        mean = sum(frame) / len(frame)
        median = sorted(frame)[int(len(frame)/2)]
        durations_means.append(mean * 1000)
        durations_medians.append(median)
        ctr += frame_size
        if ctr >= len(durations):
            # handle final frame 
            frame = durations[ctr-frame_size:]
            mean = sum(frame) / len(frame)
            median = sorted(frame)[int(len(frame)/2)]
            durations_means.append(mean)
            durations_medians.append(median)
            break

    #epochs = [i for i in range(0, len(durations))]
    #plt.plot(epochs[13900:14000], durations[13900:14000])
    epochs = [i for i in range(0, len(durations_means))]
    plt.plot(epochs[50:250], durations_means[50:250])
    #epochs = [i for i in range(0, len(durations_medians))]
    #plt.plot(epochs[100:150], durations_medians[100:150])
    legend.append("QPS:" + str(qps))

plt.title("Mean Durations of Epochs Frames")
plt.xlabel("Epoch Frame (" + str(frame_size) + " epochs/frame)")
plt.ylabel("Mean Epoch Duration (milliseconds)")
plt.legend(legend)
plt.show()



