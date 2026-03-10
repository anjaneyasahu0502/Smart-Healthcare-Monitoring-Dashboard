import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
import numpy as np

df = pd.read_csv("patient_simulator/mitbih_hr.csv")



# Create label column based on rules
df["label"] = df.apply(
    lambda row: "critical" if (row["hr"] > 140 or row["acc_mag"] > 20) else "normal",
    axis=1
)

# introduce small label noise (5%)
noise_idx = np.random.choice(len(df), size=int(0.05*len(df)), replace=False)

for i in noise_idx:
    df.loc[i, "label"] = "critical" if df.loc[i, "label"] == "normal" else "normal"
    

X = df[["hr","spo2","temp","acc_mag"]]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

model = RandomForestClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, pos_label="critical"))
print("Recall:", recall_score(y_test, y_pred, pos_label="critical"))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))