import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox
from rtos_scheduler import rtos_scheduler  # RTOS Scheduler Function
from logging_system import log_data  # Logging Function
from telemetry_tasks import task_queue  # Shared task queue for data
from PIL import Image, ImageTk

def show_info():
    info_window = tk.Toplevel()
    info_window.title("System Info")
    info_window.geometry("400x250")
    info_window.configure(bg="#222")
    
    label = tk.Label(info_window, text="This dashboard displays real-time\nvehicle telemetry data including:\n- GPS location\n- Fuel levels\n- Engine diagnostics", 
                      font=('Helvetica', 12), fg="white", bg="#222")
    label.pack(pady=20)
    
    btn_close = tk.Button(info_window, text="Close", command=info_window.destroy, bg="#444", fg="white", font=('Helvetica', 12, 'bold'))
    btn_close.pack(pady=10)

def update_dashboard(window, label_gps, label_fuel, fuel_bar, label_engine, f1_label):
    if not task_queue.empty():
        sensor, value = task_queue.get()
        if sensor == "GPS":
            label_gps.config(text=f"GPS: {value}")
        elif sensor == "FUEL":
            label_fuel.config(text=f"Fuel Level: {value}")
            fuel_percentage = int(value.replace('%', ''))
            fuel_bar['value'] = fuel_percentage
        elif sensor == "ENGINE":
            label_engine.config(text=f"Engine Status: {value}")
    
    # Simulated F1 tracking stats update
    f1_label.config(text=f"F1 Speed: {round(time.time() % 300, 2)} km/h")
    
    window.after(100, update_dashboard, window, label_gps, label_fuel, fuel_bar, label_engine, f1_label)

def create_dashboard():
    window = tk.Tk()
    window.title("Vehicle Telemetry Dashboard")
    window.geometry("1024x768")
    
    # Load and set background image to fit full screen
    bg_image = Image.open("porsche.jpg")  # Ensure the image is in the same directory
    bg_image = bg_image.resize((1024, 768), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
    
    frame = tk.Frame(window, bg="#1e1e1e", bd=5)
    frame.place(relx=0.95, rely=0.05, anchor=tk.NE, width=400, height=320)  # Increased dashboard size
    frame.configure(bg='#1e1e1e', highlightbackground='#ffffff', highlightthickness=2)
    
    title = tk.Label(frame, text="🚗 Vehicle Telemetry System", font=('Calligraphy', 20, 'bold'), fg="white", bg="#1e1e1e")
    title.pack(pady=10)
    title.config(relief=tk.RIDGE)  # Adds shadow effect
    
    btn_info = tk.Button(frame, text="ℹ️ Click for Info", command=show_info, bg="#444", fg="white", font=('Helvetica', 12, 'bold'))
    btn_info.pack(pady=5)
    
    gps_frame = tk.Frame(frame, bg="#1e1e1e", padx=10, pady=10)
    gps_frame.pack(fill=tk.X, pady=5)
    label_gps = tk.Label(gps_frame, text="GPS: Waiting for data...", font=('Helvetica', 14), fg="white", bg="#1e1e1e")
    label_gps.pack()
    
    fuel_frame = tk.Frame(frame, bg="#1e1e1e", padx=10, pady=10)
    fuel_frame.pack(fill=tk.X, pady=5)
    label_fuel = tk.Label(fuel_frame, text="Fuel Level: Waiting...", font=('Helvetica', 14), fg="white", bg="#1e1e1e")
    label_fuel.pack()
    fuel_bar = ttk.Progressbar(fuel_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
    fuel_bar.pack(pady=5)
    
    engine_frame = tk.Frame(frame, bg="#1e1e1e", padx=10, pady=10)
    engine_frame.pack(fill=tk.X, pady=5)
    label_engine = tk.Label(engine_frame, text="Engine Status: Waiting...", font=('Helvetica', 14), fg="white", bg="#1e1e1e")
    label_engine.pack()
    
    # F1 Stats Dashboard
    f1_frame = tk.Frame(window, bg="#1e1e1e", bd=5)
    f1_frame.place(relx=0.05, rely=0.8, anchor=tk.W, width=350, height=80)
    f1_frame.configure(bg='#1e1e1e', highlightbackground='#ffffff', highlightthickness=2)
    
    f1_title = tk.Label(f1_frame, text="🏎️ F1 Live Stats", font=('Helvetica', 14, 'bold'), fg="white", bg="#1e1e1e")
    f1_title.pack(pady=5)
    f1_label = tk.Label(f1_frame, text="F1 Speed: -- km/h", font=('Helvetica', 12), fg="white", bg="#1e1e1e")
    f1_label.pack()
    
    update_dashboard(window, label_gps, label_fuel, fuel_bar, label_engine, f1_label)
    window.mainloop()

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=rtos_scheduler, daemon=True)
    log_thread = threading.Thread(target=log_data, daemon=True)
    scheduler_thread.start()
    log_thread.start()
    create_dashboard()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nTelemetry system shutting down...")