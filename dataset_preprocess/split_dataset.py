import pandas as pd
import numpy as np

df = pd.read_csv("mitbih_edge.csv")

# Shuffle rows
df = df.sample(frac=1).reset_index(drop=True)

# 70% normal, 30% critical
split = int(len(df) * 0.7)

normal = df[:split]
critical = df[split:]

# Inject abnormal values in CRITICAL
critical["hr"] = np.random.randint(140, 180, size=len(critical))
critical["spo2"] = np.random.randint(85, 92, size=len(critical))
critical["temp"] = np.random.uniform(38.5, 40.0, size=len(critical))
critical["acc_mag"] = np.random.uniform(15, 25, size=len(critical))

normal.to_csv("normal.csv", index=False)
critical.to_csv("critical.csv", index=False)

print("normal rows:", len(normal))
print("critical rows:", len(critical))
print("Saved normal.csv and critical.csv")
