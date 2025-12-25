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

qps_str = qps_dir.split('_')[1].split('/')[0]

title_string = " per Epoch (~0.1 seconds) with QPS = " + qps_str + ", ITRD = " + itrd + ", DVFS = " + dvfs 

epochs_dfs = {}
for update_dir in os.listdir(exp_dir):
    if update_dir.split('_')[0] != "sets": 
        continue
    update = update_dir.split('_')[1]
    subdir = exp_dir + "/" + update_dir + "/" + qps_dir + "/itrd_" + itrd + "_dvfs_" + dvfs + "/"
    df = pd.read_csv(subdir + "/epochs_per_delta_time.csv", index_col=0)
    epochs_dfs[update] = df

updates = [update for update in epochs_dfs.keys()]

fig = plt.figure(figsize=(13,8))
legend = []
metric = "Number_of_Interruptions"
for update in sorted(updates):
    df = epochs_dfs[str(update)]
    lengths = df["num_interruptions"]
    epochs = [i for i in range(0, len(lengths))]
    plt.plot(epochs[50:-50], lengths[50:-50])
    legend.append("%SETS:" + str(update))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + qps_str + "_per_update_" + itrd + "_" + dvfs + ".png")

fig = plt.figure(figsize=(13,8))
legend = []
metric = "Rx_Bytes"
for update in sorted(updates):
    df = epochs_dfs[str(update)]
    rx_bytes = df["rx_bytes_sum"]
    epochs = [i for i in range(0, len(rx_bytes))]
    plt.plot(epochs[50:-50], rx_bytes[50:-50])
    legend.append("%SETS:" + str(update))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + qps_str + "_per_update_" + itrd + "_" + dvfs + ".png")


fig = plt.figure(figsize=(13,8))
legend = []
metric = "Instructions"
for update in sorted(updates):
    df = epochs_dfs[str(update)]
    instructions = df["instructions_sum"]
    epochs = [i for i in range(0, len(instructions))]
    plt.plot(epochs[50:-50], instructions[50:-50])
    legend.append("%SETS:" + str(update))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + qps_str + "_per_update_" + itrd + "_" + dvfs + ".png")


fig = plt.figure(figsize=(13,8))
legend = []
metric = "Cycles"
for update in sorted(updates):
    df = epochs_dfs[str(update)]
    cycles = df["cycles_sum"]
    epochs = [i for i in range(0, len(cycles))]
    plt.plot(epochs[50:-50], cycles[50:-50])
    legend.append("%SETS:" + str(update))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + qps_str + "_per_update_" + itrd + "_" + dvfs + ".png")


fig = plt.figure(figsize=(13,8))
legend = []
metric = "Ref_Cycles"
for update in sorted(updates):
    df = epochs_dfs[str(update)]
    ref_cycles = df["ref_cycles_sum"]
    epochs = [i for i in range(0, len(ref_cycles))]
    plt.plot(epochs[50:-50], ref_cycles[50:-50])
    legend.append("%SETS:" + str(update))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + qps_str + "_per_update_" + itrd + "_" + dvfs + ".png")

fig = plt.figure(figsize=(13,8))
legend = []
metric = "LLC_Miss"
for update in sorted(updates):
    df = epochs_dfs[str(update)]
    llc_miss = df["llc_miss_sum"]
    epochs = [i for i in range(0, len(llc_miss))]
    plt.plot(epochs[50:-50], llc_miss[50:-50])
    legend.append("%SETS:" + str(update))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + qps_str + "_per_update_" + itrd + "_" + dvfs + ".png")

fig = plt.figure(figsize=(13,8))
legend = []
metric = "Active_Cores"
for update in sorted(updates):
    df = epochs_dfs[str(update)]
    cores = df["active_cores"]
    epochs = [i for i in range(0, len(cores))]
    plt.plot(epochs[50:-50], cores[50:-50])
    legend.append("%SETS:" + str(update))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + qps_str + "_per_update_" + itrd + "_" + dvfs + ".png")




