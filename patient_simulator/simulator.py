import time
import json
import pandas as pd
import paho.mqtt.client as mqtt
import random

df = pd.read_csv("mitbih_hr.csv")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("127.0.0.1",1883)
client.loop_start()

for _, row in df.iterrows():

    base_hr = int(row["hr"])
    r = random.random()

    # 70% NORMAL
    if r < 0.7:
        hr = base_hr
        acc = round(random.uniform(0.8,1.2),2)

    # 30% CRITICAL
    else:
        hr = random.randint(150, 180)
        acc = round(random.uniform(20,25),2)

    data = {
        "patient_id": "P001",
        "hr": hr,
        "spo2": float(row["spo2"]),
        "temp": float(row["temp"]),
        "acc_mag": acc,
        "timestamp": time.time()
    }

    print("Publishing:", data)
    client.publish("hospital/vitals", json.dumps(data))
    time.sleep(2)
