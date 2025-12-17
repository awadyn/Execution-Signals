import pandas as pd
import sys
import numpy as np

summary_file = sys.argv[1]
merged_intlog_file =  sys.argv[2]

df = pd.read_csv(summary_file)

itrds = list(set(df["itrd"].values))
itrds.sort()

df["rx_bytes_median"] = float(0)

for itrd in itrds:
    df_itrd = df[df["itrd"] == itrd]
    df2 = pd.read_csv(merged_intlog_file)

    rx_bytes = df2["rx_bytes"].values
    rx_bytes.sort()
    rx_median = rx_bytes[len(rx_bytes)/2]
    df.at[df_itrd.index[0], "rx_bytes_median"] = rx_median

df.to_csv(summary_file)

print(df)
