import pandas as pd
import time

df = pd.read_csv("../patient_simulator/mitbih_hr.csv")

start = time.time()

df["timestamp"] = [(start + i*2)*1000 for i in range(len(df))]

df = df[["timestamp","hr","spo2","temp","acc_mag"]]

df.to_csv("mitbih_edge.csv", index=False)

print("Created mitbih_edge.csv")
