import json,joblib,requests
import paho.mqtt.client as mqtt

model = joblib.load("model.pkl")

MQTT_TOPIC="hospital/vitals"
CLOUD_ALERT_API="http://127.0.0.1:5000/api/alerts"
CLOUD_HEALTH_API="http://127.0.0.1:5000/api/health"

def on_connect(client,userdata,flags,reason,props=None):
    print("Fog connected")
    client.subscribe(MQTT_TOPIC)

def on_message(client,userdata,msg):

    data=json.loads(msg.payload.decode())

    hr=data["hr"]
    spo2=data["spo2"]
    temp=data["temp"]
    acc=data["acc_mag"]

    pred=model.predict([[hr,spo2,temp,acc]])[0]

    if acc>20 or hr>140:
        status="CRITICAL"
    elif pred==-1:
        status="WARNING"
    else:
        status="NORMAL"

    health={
        "patient_id":data["patient_id"],
        "status":status,
        "hr":hr,
        "spo2":spo2,
        "temp":temp,
        "acc_mag":acc,
        "timestamp":data["timestamp"]
    }

    requests.post(CLOUD_HEALTH_API, json=health, proxies={"http": None, "https": None})

    if status=="CRITICAL":
        alert=health.copy()
        alert["type"]="CRITICAL"
        requests.post(CLOUD_ALERT_API, json=alert, proxies={"http": None, "https": None})
        print("CRITICAL:",alert)
    else:
        print(status)

client=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect=on_connect
client.on_message=on_message
client.connect("127.0.0.1",1883)
client.loop_forever()
