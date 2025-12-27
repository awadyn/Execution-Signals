import os
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
TIME_CONVERSION_khz = 1./(2899999*1000)

exp_dir = sys.argv[1]
qps_dir = sys.argv[2]
itrd = sys.argv[3]
dvfs = sys.argv[4]

time_frame = '0.01'
qps_str = qps_dir.split('_')[1].split('/')[0]

epochs_update_dfs = {}
for update_dir in os.listdir(exp_dir):
    if update_dir.split('_')[0] != "sets": 
        continue
    update = update_dir.split('_')[1]
    subdir = exp_dir + "/" + update_dir + "/" + qps_dir + "/itrd_" + itrd + "_dvfs_" + dvfs + "/"
    df = pd.read_csv(subdir + "/active_cores.csv", index_col=0)
    epochs_update_dfs[update] = df

updates = [update for update in epochs_update_dfs.keys()]


title_string = " per Epoch (~" + time_frame + " seconds) with QPS = " + qps_str + ", ITRD = " + itrd + ", DVFS = " + dvfs 
fig = plt.figure(figsize=(13,8))
legend = []
metric = "Active_Cores_Delta"
for update in sorted(updates, reverse=True):
    df = epochs_update_dfs[str(update)]
    deltas = df["active_cores_delta"]
    epochs = [i for i in range(0, len(deltas))]
    plt.scatter(epochs, deltas, marker='x')
    legend.append("%SETS:" + str(update))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + qps_str + "_per_update_" + itrd + "_" + dvfs + ".png")




