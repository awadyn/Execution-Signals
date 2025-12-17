import sys
import pandas as pd

csv_file = sys.argv[1]
outfile = sys.argv[2]

df_merged = pd.read_csv(csv_file, index_col = 0)

ref_core = df_merged["core"].values[0]
start = df_merged["timestamp"].values[0]
rx_sum = df_merged["rx_bytes"].values[0]
length = 1

epochs_df = pd.DataFrame(columns=["rx_bytes_sum", "duration", "num_interruptions"])
end = 0

print(ref_core)

for epoch, row in df_merged.iterrows():
    if epoch == 0:      # skip first row
        continue

    if row["core"] == ref_core:
        end = row["timestamp"]
        new_row_data = {"rx_bytes_sum": rx_sum, "duration": end - start, "num_interruptions": length}
        new_row = pd.DataFrame([new_row_data])
        epochs_df = pd.concat([epochs_df, new_row], ignore_index=True)
        start = end
        rx_sum = row["rx_bytes"]
        length = 1
    else:
        length += 1
        rx_sum += row["rx_bytes"]

print(epochs_df)
epochs_df.to_csv(outfile)

