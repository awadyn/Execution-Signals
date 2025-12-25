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

title_string = " per Epoch (~0.1 seconds) with %SETS = " + update_str + ", ITRD = " + itrd + ", DVFS = " + dvfs 

epochs_dfs = {}
for qps_dir in os.listdir(exp_dir):
    if qps_dir.split('_')[0] != "qps": 
        continue
    qps = qps_dir.split('_')[1]
    subdir = exp_dir + "/" + qps_dir + "/itrd_" + itrd + "_dvfs_" + dvfs + "/"
    df = pd.read_csv(subdir + "/epochs_per_delta_time.csv", index_col=0)
    epochs_dfs[qps] = df

qpses = [int(qps) for qps in epochs_dfs.keys()]

fig = plt.figure(figsize=(13,8))
legend = []
metric = "Number_of_Interruptions"
for qps in sorted(qpses):
    df = epochs_dfs[str(qps)]
    lengths = df["num_interruptions"]
    epochs = [i for i in range(0, len(lengths))]
    plt.plot(epochs[50:-50], lengths[50:-50])
    legend.append("QPS:" + str(qps))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + update_str + "_per_qps_" + itrd + "_" + dvfs + ".png")

fig = plt.figure(figsize=(13,8))
legend = []
metric = "Rx_Bytes"
for qps in sorted(qpses):
    df = epochs_dfs[str(qps)]
    rx_bytes = df["rx_bytes_sum"]
    epochs = [i for i in range(0, len(rx_bytes))]
    plt.plot(epochs[50:-50], rx_bytes[50:-50])
    legend.append("QPS:" + str(qps))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + update_str + "_per_qps_" + itrd + "_" + dvfs + ".png")


fig = plt.figure(figsize=(13,8))
legend = []
metric = "Instructions"
for qps in sorted(qpses):
    df = epochs_dfs[str(qps)]
    instructions = df["instructions_sum"]
    epochs = [i for i in range(0, len(instructions))]
    plt.plot(epochs[50:-50], instructions[50:-50])
    legend.append("QPS:" + str(qps))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + update_str + "_per_qps_" + itrd + "_" + dvfs + ".png")


fig = plt.figure(figsize=(13,8))
legend = []
metric = "Cycles"
for qps in sorted(qpses):
    df = epochs_dfs[str(qps)]
    cycles = df["cycles_sum"]
    epochs = [i for i in range(0, len(cycles))]
    plt.plot(epochs[50:-50], cycles[50:-50])
    legend.append("QPS:" + str(qps))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + update_str + "_per_qps_" + itrd + "_" + dvfs + ".png")


fig = plt.figure(figsize=(13,8))
legend = []
metric = "Ref_Cycles"
for qps in sorted(qpses):
    df = epochs_dfs[str(qps)]
    ref_cycles = df["ref_cycles_sum"]
    epochs = [i for i in range(0, len(ref_cycles))]
    plt.plot(epochs[50:-50], ref_cycles[50:-50])
    legend.append("QPS:" + str(qps))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + update_str + "_per_qps_" + itrd + "_" + dvfs + ".png")

fig = plt.figure(figsize=(13,8))
legend = []
metric = "LLC_Miss"
for qps in sorted(qpses):
    df = epochs_dfs[str(qps)]
    llc_miss = df["llc_miss_sum"]
    epochs = [i for i in range(0, len(llc_miss))]
    plt.plot(epochs[50:-50], llc_miss[50:-50])
    legend.append("QPS:" + str(qps))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + update_str + "_per_qps_" + itrd + "_" + dvfs + ".png")

fig = plt.figure(figsize=(13,8))
legend = []
metric = "Active_Cores"
for qps in sorted(qpses):
    df = epochs_dfs[str(qps)]
    cores = df["active_cores"]
    epochs = [i for i in range(0, len(cores))]
    plt.plot(epochs[50:-50], cores[50:-50])
    legend.append("QPS:" + str(qps))
plt.title(metric + title_string)
plt.xlabel("Epoch")
plt.ylabel(metric)
plt.legend(legend)
plt.savefig(exp_dir + "/" + metric.lower() + "_" + update_str + "_per_qps_" + itrd + "_" + dvfs + ".png")




