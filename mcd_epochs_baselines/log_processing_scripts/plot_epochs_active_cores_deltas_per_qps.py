import os
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
TIME_CONVERSION_khz = 1./(2899999*1000)

exp_dir = sys.argv[1]
update_str = sys.argv[2]
itrd = sys.argv[3]
dvfs = sys.argv[4]

time_frame = '0.01'

epochs_qps_dfs = {}
for qps_dir in os.listdir(exp_dir):
    if qps_dir.split('_')[0] != "qps": 
        continue
    qps = qps_dir.split('_')[1]
    subdir = exp_dir + "/" + qps_dir + "/itrd_" + itrd + "_dvfs_" + dvfs + "/"
    df = pd.read_csv(subdir + "/active_cores.csv", index_col=0)
    epochs_qps_dfs[qps] = df
qpses = [int(qps) for qps in epochs_qps_dfs.keys()]

title_string = " per Epoch (~" + time_frame + " seconds) with %SETS = " + update_str + ", ITRD = " + itrd + ", DVFS = " + dvfs 
fig = plt.figure(figsize=(13,8))
legend = []
metric = "Active_Cores_Delta"
for qps in sorted(qpses, reverse=True):
    df = epochs_qps_dfs[str(qps)]
    deltas = df["active_cores_delta"]
    epochs = [i for i in range(0, len(deltas))]
    plt.scatter(epochs, deltas, marker='x')
    legend.append("QPS:" + str(qps))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + update_str + "_per_qps_" + itrd + "_" + dvfs + ".png")

