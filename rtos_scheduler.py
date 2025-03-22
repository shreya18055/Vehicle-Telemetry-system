import time
from telemetry_tasks import gps_tracking, fuel_monitoring, engine_diagnostics, task_queue

# Define tasks with priorities
tasks = [
    (gps_tracking, 1),  # Higher priority
    (fuel_monitoring, 2),
    (engine_diagnostics, 3)
]

# RTOS Round-Robin Scheduler
def rtos_scheduler():
    while True:
        for task, priority in sorted(tasks, key=lambda x: x[1]):  # Sort by priority
            task()  # Execute the function
            time.sleep(1)  # Simulate RTOS time slice
        time.sleep(1)  # Add delay for synchronization with UI
