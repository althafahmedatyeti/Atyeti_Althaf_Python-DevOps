from google.cloud import pubsub_v1
import json,random ,time
from datetime import datetime
Data_Limit=100
count=0
PROJECT_ID = "iot-stream-project"       
TOPIC_ID = "iot-stream"
""
publisher = pubsub_v1.PublisherClient()# Create a Publisher client
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

while count < Data_Limit :# Generate 100 data points
    data={
        "device_id": random.choice(["iot_Hitech _city", "iot_KPHB", "iot_Madhapur","iot_secunderabad"]),
        "temperature":round(random.uniform(25.0, 40.0),1),
        "pressure": round(random.uniform(950.0, 1050.0), 1),
        "humidity": round(random.uniform(30.0, 70.0),1),
          "co2_level": round(random.uniform(300, 1000), 1),
        "gas_leak": random.choice([True, False]),
        "timestamp": datetime.utcnow().isoformat()
    }
    publisher.publish(topic_path, data=json.dumps(data).encode("utf-8"))
    with open("op_file.json", "a") as f: #optional file to store data in local for testingt
        f.write(json.dumps(data) + "\n")
        f.flush()
    print("Published:", data)
    count+=1
    time.sleep(1)