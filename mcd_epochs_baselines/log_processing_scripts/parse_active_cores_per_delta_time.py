import sys
import pandas as pd
import numpy as np
import math

csv_file = sys.argv[1]
outfile = sys.argv[2]

df_merged = pd.read_csv(csv_file, index_col = 0)

#df_merged = df_merged.iloc[0:20000]
#df_merged = df_merged.reset_index(drop=True)

duration = 0
time_start = df_merged["timestamp"].values[0]
time_now = time_start
start_loc = 0
end_loc = 0

epochs_df = pd.DataFrame(columns=["duration", "active_cores"])

time_frame = 0.01    # seconds
TIME_CONVERSION_khz = 1./(2899999*1000)

all_cores = [i for i in range(0,16)]
print(all_cores)

for index, row in df_merged.iterrows():
    if index == 0:      # skip first row
        continue
    if (row["timestamp"] - time_start) * TIME_CONVERSION_khz >= time_frame: 
        # create new epoch
        epoch = df_merged.iloc[start_loc:end_loc+1]
        duration = (time_now - time_start) * TIME_CONVERSION_khz
        cores = list(set(epoch["core"].values))
        active_cores = [1 if c in cores else 0 for c in all_cores]
        new_row_data = {"duration": duration, "active_cores": active_cores}
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

