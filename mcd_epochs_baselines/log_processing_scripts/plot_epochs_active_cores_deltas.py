import os
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
TIME_CONVERSION_khz = 1./(2899999*1000)

exp_dir = sys.argv[1]
qps_str = sys.argv[2]
update_str = sys.argv[3]
itrd = sys.argv[4]
dvfs = sys.argv[5]

qps_str = qps_dir.split('_')[1].split('/')[0]

epochs_qps_dfs = {}
for qps_dir in os.listdir(exp_dir):
    if qps_dir.split('_')[0] != "qps": 
        continue
    qps = qps_dir.split('_')[1]
    subdir = exp_dir + "/" + qps_dir + "/itrd_" + itrd + "_dvfs_" + dvfs + "/"
    df = pd.read_csv(subdir + "/active_cores.csv", index_col=0)
    epochs_qps_dfs[qps] = df
qpses = [int(qps) for qps in epochs_qps_dfs.keys()]

epochs_update_dfs = {}
for update_dir in os.listdir(exp_dir):
    if update_dir.split('_')[0] != "sets": 
        continue
    update = update_dir.split('_')[1]
    subdir = exp_dir + "/" + update_dir + "/" + qps_dir + "/itrd_" + itrd + "_dvfs_" + dvfs + "/"
    df = pd.read_csv(subdir + "/epochs_per_delta_time.csv", index_col=0)
    epochs_update_dfs[update] = df
updates = [update for update in epochs_update_dfs.keys()]

title_string = " per Epoch (~0.1 seconds) with %SETS = " + update_str + ", ITRD = " + itrd + ", DVFS = " + dvfs 
fig = plt.figure(figsize=(13,8))
legend = []
metric = "Active_Cores_Delta"
for qps in sorted(qpses):
    df = epochs_qps_dfs[str(qps)]
    deltas = df["active_cores_delta"]
    epochs = [i for i in range(0, len(deltas))]
    plt.scatter(epochs, deltas, marker='.')
    legend.append("QPS:" + str(qps))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + update_str + "_per_qps_" + itrd + "_" + dvfs + ".png")

title_string = " per Epoch (~0.1 seconds) with QPS = " + qps_str + ", ITRD = " + itrd + ", DVFS = " + dvfs 
fig = plt.figure(figsize=(13,8))
legend = []
for update in sorted(updates):
    df = epochs_update_dfs[str(update)]
    deltas = df["active_cores_delta"]
    epochs = [i for i in range(0, len(deltas))]
    plt.plot(epochs, deltas)
    legend.append("%SETS:" + str(update))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + qps_str + "_per_update_" + itrd + "_" + dvfs + ".png")




