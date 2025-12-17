import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler
import sys
import numpy as np
import os

file_csv = sys.argv[1]
qps = file_csv.split('_')[-1].split('.')[0]
print(qps)

fig, ax = plt.subplots(figsize=(20,7))

df = pd.read_csv(file_csv)
itrds = [int(itrd) for itrd in list(set(df["itrd"].values))]
dvfss = list(set(df["dvfs"].values))
itrds.sort()
print(itrds, dvfss)

markers = ["s", "o", "^", ".", "x"]
colors = []

for itrd in itrds:
    x_vals = []
    y_vals = []
    itrd_vals = []
    dvfs_vals = []

    df_itrd = df[df["itrd"] == itrd]  
    peak_qpses = df_itrd["peak_qps"].values
    lats = df_itrd["99th_read"].values
    joules = df_itrd["pkg_joules"].values
    dvfses = df_itrd["dvfs"].values  
    print(itrd, peak_qpses, lats, joules, dvfses)

    ctr = 0
    min_joules = 2**32 - 1
    min_lat = 0
    min_dvfs = 0
    for peak_qps in peak_qpses:
        if int(peak_qps) < int(qps) - 5000:
            print("SKIPPING.. qps:", qps, "-- peak qps:", peak_qps, "--", itrd)
            ctr += 1
            continue
        lat = lats[ctr]
        joules_ = joules[ctr]
        dvfs = " " + dvfses[ctr] + " "

#        if lat > 500:
#            print("SKIPPING.. lat:", lat, "-- peak qps:", peak_qps, "--", itrd)
#            ctr += 1
#            continue

        x_vals.append(lat)
        y_vals.append(joules_)
        itrd_vals.append(itrd)
        dvfs_vals.append(dvfs)
        if joules_ < min_joules:
            min_joules = joules_
            min_lat = lat
            min_dvfs = dvfs
        ctr += 1


    print(x_vals)
    print(y_vals)
    print(itrd_vals)
    print(dvfs_vals) 
    print()

    cur_color = ""
    if len(y_vals) > 0:
        ax.plot(x_vals, y_vals, label="ITRD:" + str(itrd))
#        legend.append("ITRD: " + str(itrd))
        cur_color = ax.lines[-1].get_color()
        colors.append(cur_color)
        print(cur_color)

        i = 0
        for x_val in x_vals:
            ax.plot(x_val, y_vals[i], marker=markers[i], color=cur_color)
            i += 1

        i = 0
        if itrd == 2:
            for dvfs in dvfs_vals:
                ax.text(x_vals[i], y_vals[i], dvfs, fontsize=18, verticalalignment="bottom", horizontalalignment="center")
                i += 1


legend = ax.legend(fontsize=16)
i = 0
for text in legend.get_texts():
    text.set_color(colors[i])
    i += 1
plt.title("Latency vs. Energy Pareto Frontier for Variable Interrupt Delay and DVFS with QPS " + str(qps), fontsize=22)
plt.xlabel("99th Tail Read Latency (Milliseconds)", fontsize=22)
plt.ylabel("Energy (Joules)", fontsize=22)
plt.xticks(fontsize=21)
plt.yticks(fontsize=21)
plt.show()

