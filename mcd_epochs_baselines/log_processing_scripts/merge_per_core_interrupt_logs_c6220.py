import sys
import pandas as pd

logs_dir = sys.argv[1]
out_file = sys.argv[2]

dfs = {}
for core in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
    dfs[core] = pd.read_csv(logs_dir + "core_" + str(core), sep=' ', names=["rx_bytes", "instructions", "cycles", "ref_cycles", "llc_miss", "timestamp"])
    dfs[core]["core"] = [core] * dfs[core].shape[0]

df_concat = pd.concat([df for df in dfs.values()])
df_merged = df_concat.sort_values(by="timestamp", ascending=True)
df_merged = df_merged.reset_index(drop=True)
df_merged.to_csv(out_file)

