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
    df = pd.read_csv(exp_dir + qps_dir + "/itrd_100_dvfs_0x1900/epochs_per_delta_time.csv", index_col=0)
    epochs_dfs[qps] = df

fig = plt.figure(figsize=(20,12))
frame_size = 1
legend = []
qpses = [int(qps) for qps in epochs_dfs.keys()]
for qps in sorted(qpses):
    df = epochs_dfs[str(qps)]
    lengths = df["num_interruptions"]
    rx_bytes = df["rx_bytes_sum"]
    epochs = [i for i in range(0, len(lengths))]
    #plt.plot(epochs[750:1000], lengths[750:1000])
    plt.plot(epochs[0:], rx_bytes[0:])
    legend.append("QPS:" + str(qps))

plt.title("Rx_Bytes Sum per Epoch of ~0.01 seconds")
plt.xlabel("Epoch")
plt.ylabel("Rx_Bytes Sum Across all Interrupts")
plt.legend(legend)
plt.show()



