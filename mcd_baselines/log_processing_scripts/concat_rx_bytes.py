import pandas as pd
import numpy as np
import sys
import os

cols=["rx_bytes", "timestamp"]
TIME_CONVERSION_khz = 1./(2899999*1000)
JOULES_CONVERSION = 0.000061

def concat_multi_core_timestamps_rx_bytes(logs_dir, skip_cores=[]):
    timestamp_dfs = {}
    rx_bytes_dfs = {}
    iterators = {}
    for file in os.listdir(logs_dir):
        if file.split('_')[0] != "core":
            continue
        core = file.split('_')[1].split('.')[0]
        for skipped in skip_cores:
            if core == str(skipped):
                continue
        df = pd.read_csv(logs_dir + file, sep=" ", names=cols)
        timestamp_dfs[core] = df["timestamp"].values * TIME_CONVERSION_khz
        rx_bytes_dfs[core] = df["rx_bytes"].values
        iterators[core] = 0

    all_timestamps = []
    all_rx_bytes = []
    all_cores = []
    while True:
        done = 0

        min_timestamp = 2**64 - 1
        ref_rx_bytes = 0
        ref_core = ""
        for core in iterators.keys():
            if iterators[core] == len(timestamp_dfs[core]):
                done += 1
                continue
            core_timestamp = timestamp_dfs[core][iterators[core]]
            if core_timestamp < min_timestamp:
                min_timestamp = core_timestamp
                ref_core = core
                ref_rx_bytes = rx_bytes_dfs[core][iterators[core]]

        if done == len(iterators.keys()):
            break

        iterators[ref_core] += 1
        all_timestamps.append(min_timestamp)
        all_cores.append(int(ref_core))
        all_rx_bytes.append(ref_rx_bytes)

    return all_timestamps, all_rx_bytes, all_cores


dir = sys.argv[1]

itrds = []
for subdir in os.listdir(dir):
    if subdir.split("_")[0] != "itrd":
        continue
    itrds.append(subdir.split("_")[1])
itrds = set(itrds)
print(itrds)


all_concat_timestamps = {}
all_concat_interrupted_cores = {}
all_concat_rx_bytes = {}
for itrd in itrds:
    subdir = dir + "/itrd_" + str(itrd) + "/"
    print(subdir)
    concat_timestamps, concat_rx_bytes, concat_interrupted_cores = concat_multi_core_timestamps_rx_bytes(subdir)
    all_concat_timestamps[itrd] = concat_timestamps
    all_concat_interrupted_cores[itrd] = concat_interrupted_cores
    all_concat_rx_bytes[itrd] = concat_rx_bytes
#    break

for itrd in all_concat_timestamps.keys():
    print(itrd)
    timestamps = all_concat_timestamps[itrd]
    interrupted_cores = all_concat_interrupted_cores[itrd]
    rx_bytes = all_concat_rx_bytes[itrd]
    temp = {"timestamp": timestamps, "rx_bytes": rx_bytes, "core": interrupted_cores}
    df = pd.DataFrame(temp)
    print(df)
    print(df["timestamp"].values[-1] - df["timestamp"].values[0])
    print(sum(df["rx_bytes"].values))
    subdir = dir + "/itrd_" + str(itrd) + "/"
    df.to_csv(subdir + "concat_timestamps_rx_bytes_cores.csv", index=False)
#    break

