import sys
import pandas as pd
import numpy as np
import math

csv_file = sys.argv[1]
outfile = sys.argv[2]

df_merged = pd.read_csv(csv_file, index_col = 0)

duration = 0

time_start = df_merged["timestamp"].values[0]
time_now = time_start
start_loc = 0
end_loc = 0

epochs_df = pd.DataFrame(columns=["rx_bytes_sum", "instructions_sum", "cycles_sum", "ref_cycles_sum", "llc_miss_sum", "num_interruptions", "duration", "active_cores"])

time_frame = 0.01    # seconds
TIME_CONVERSION_khz = 1./(2899999*1000)


for index, row in df_merged.iterrows():
    if index == 0:      # skip first row
        continue
    if (row["timestamp"] - time_start) * TIME_CONVERSION_khz >= time_frame: 
        # create new epoch
        epoch = df_merged.iloc[start_loc:end_loc+1]
        duration = (time_now - time_start) * TIME_CONVERSION_khz
        length = epoch.shape[0]
        rx_sum = np.sum(epoch["rx_bytes"].values)

        cores = list(set(epoch["core"].values))
        instructions_sum = 0
        cycles_sum = 0
        ref_cycles_sum = 0
        llc_miss_sum = 0
        for core in cores:
            diffs = np.diff(epoch[epoch["core"] == core]["instructions"].values)
            instructions_sum += np.sum(diffs[diffs > 0])     # drop overflow diffs for now
            diffs = np.diff(epoch[epoch["core"] == core]["cycles"].values)
            cycles_sum += np.sum(diffs[diffs > 0])     # drop overflow diffs for now
            diffs = np.diff(epoch[epoch["core"] == core]["ref_cycles"].values)
            ref_cycles_sum += np.sum(diffs[diffs > 0])     # drop overflow diffs for now
            diffs = np.diff(epoch[epoch["core"] == core]["llc_miss"].values)
            llc_miss_sum += np.sum(diffs[diffs > 0])     # drop overflow diffs for now

        new_row_data = {"rx_bytes_sum": rx_sum, "instructions_sum": instructions_sum, "cycles_sum": cycles_sum, "ref_cycles_sum": ref_cycles_sum, "llc_miss_sum": llc_miss_sum, "num_interruptions": length, "duration": duration, "active_cores": len(cores)}
        new_row = pd.DataFrame([new_row_data])
        epochs_df = pd.concat([epochs_df, new_row], ignore_index=True, sort=False)

        start_loc = index
        end_loc = index
        time_now = row["timestamp"]
        time_start = time_now

    else:
        end_loc += 1
        time_now = row["timestamp"]


print(epochs_df)
epochs_df.to_csv(outfile)

