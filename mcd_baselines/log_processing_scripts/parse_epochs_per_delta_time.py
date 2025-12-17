import sys
import pandas as pd

csv_file = sys.argv[1]
outfile = sys.argv[2]

df_merged = pd.read_csv(csv_file, index_col = 0)

rx_sum = df_merged["rx_bytes"].values[0]
length = 1
time_start = df_merged["timestamp"].values[0]

epochs_df = pd.DataFrame(columns=["rx_bytes_sum", "num_interruptions", "duration"])

time_frame = 0.01    # seconds
TIME_CONVERSION_khz = 1./(2899999*1000)

duration = 0
for index, row in df_merged.iterrows():
    if index == 0:      # skip first row
        continue
    if (row["timestamp"] - time_start) * TIME_CONVERSION_khz >= time_frame: 
        new_row_data = {"rx_bytes_sum": rx_sum, "num_interruptions": length, "duration": duration}
        new_row = pd.DataFrame([new_row_data])
        epochs_df = pd.concat([epochs_df, new_row], ignore_index=True)
        time_start = row["timestamp"]
        duration = 0
        rx_sum = row["rx_bytes"]
        length = 1
    else:
        length += 1
        rx_sum += row["rx_bytes"]
        duration = (row["timestamp"] - time_start ) * TIME_CONVERSION_khz

print(epochs_df)
epochs_df.to_csv(outfile)

