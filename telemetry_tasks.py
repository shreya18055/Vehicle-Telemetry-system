import random
import psutil
import queue

# Task queue for sharing data with the Tkinter UI
task_queue = queue.Queue()

def gps_tracking():
    latitude = round(random.uniform(10.0, 50.0), 5)
    longitude = round(random.uniform(20.0, 80.0), 5)
    value = f"{latitude}, {longitude}"
    print(f"[GPS] Location: {value}")
    task_queue.put(("GPS", value))

def fuel_monitoring():
    fuel_level = random.randint(10, 100)  # Random fuel level
    value = f"{fuel_level}%"
    print(f"[FUEL] Level: {value}")
    task_queue.put(("FUEL", value))

def engine_diagnostics():
    # Call cpu_percent with an interval to get the correct CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)  # Adding interval for accurate measurement
    status = "Good" if cpu_usage < 70 else "Check Engine"
    value = f"{status} (CPU: {cpu_usage}%)"
    print(f"[ENGINE] Health: {value}")
    task_queue.put(("ENGINE", value))
