import time
import requests
from telemetry_tasks import task_queue

# Function to log data
def log_data():
    while True:
        if not task_queue.empty():
            sensor, value = task_queue.get()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            with open("telemetry_log.txt", "a") as f:
                f.write(f"{timestamp} [{sensor}] {value}\n")
            print(f"[LOGGED] {sensor}: {value}")
            
            # Simulate cloud upload
            send_to_cloud(sensor, value)
        time.sleep(0.5)

# Function to simulate sending data to cloud
def send_to_cloud(sensor, value):
    url = "https://example.com/api/telemetry"  # Replace with actual API
    data = {"sensor": sensor, "value": value, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
    response = requests.post(url, json=data)
    print(f"[CLOUD] Sent {sensor} data: {response.status_code}")
