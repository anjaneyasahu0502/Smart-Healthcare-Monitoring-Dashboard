import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# load dataset
df = pd.read_csv("../patient_simulator/mitbih_hr.csv")

# select features
features = df[["hr","spo2","temp","acc_mag"]]

# train model
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(features)

# save model
joblib.dump(model, "model.pkl")

print("model.pkl trained successfully")