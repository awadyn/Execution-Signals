import pandas as pd
import sys

file = sys.argv[1]

ref = [1] * 16

df = pd.read_csv(file, index_col=0);
deltas = []
for i,row in df.iterrows():
    cores = row["active_cores"].split('[')[1].split(']')[0].split(',')
    cores = [int(c) for c in cores]
    delta_list = [x ^ y for x,y in zip(cores, ref)]
    delta = sum(delta_list)
    deltas.append(delta)

df["active_cores_delta"] = deltas

print(df)

df.to_csv(file);

