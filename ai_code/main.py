import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import os
import numpy as np
import threading
from andor_control import (initialize_camera, initialize_shamrock, set_temperature,
                           set_exposure_time, set_wavelength, acquire_spectra,
                           shutdown, is_temperature_stabilized)
from kcube_control import (initialize_kcube, home_stage, move_to_position, shutdown_kcube)
import time

class SpectrometerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spectrometer Control")
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Hardware variables
        self.device_andor = None
        self.device_kcube = None
        self.temp_thread = None
        self.spectra_data = []

        # GUI variables
        self.experiment_dir = "C:\\Users\\termi\\Desktop\\test_directory"
        self.experiment_name = "test_run"
        self.current_pos = tk.DoubleVar(value=12.0)

        # Initialize hardware in a separate thread to keep GUI responsive
        self.status_label = tk.Label(self, text="Initializing hardware...", font=("Arial", 12))
        self.status_label.pack(pady=10)
        threading.Thread(target=self.initialize_hardware, daemon=True).start()

        # Create GUI elements after initialization
        self.create_widgets()

    def initialize_hardware(self):
        try:
            initialize_camera()
            self.device_andor = initialize_shamrock()
            self.device_kcube = initialize_kcube(serial_no="26005869")
            self.temp_thread = set_temperature(-70)
            home_stage(self.device_kcube, ask_user=False)  # Auto-home for simplicity

            # Wait for temperature stabilization
            while True:
                stabilized, temp = is_temperature_stabilized()
                if stabilized:
                    self.status_label.config(text=f"Temperature stabilized at {temp:.2f}°C")
                    break
                self.status_label.config(text=f"Current temp: {temp:.2f}°C")
                time.sleep(2)

            # Set defaults
            set_exposure_time(0.05)
            set_wavelength(self.device_andor, 450.0)
            move_to_position(self.device_kcube, self.current_pos.get())
        except Exception as e:
            self.status_label.config(text=f"Initialization failed: {e}")
            messagebox.showerror("Error", f"Hardware initialization failed: {e}")

    def create_widgets(self):
        # Parameters frame
        param_frame = ttk.LabelFrame(self, text="Acquisition Parameters")
        param_frame.pack(padx=10, pady=10, fill="x")

        # Exposure time
        ttk.Label(param_frame, text="Exposure Time (s):").grid(row=0, column=0, padx=5, pady=5)
        self.exposure_entry = ttk.Entry(param_frame)
        self.exposure_entry.insert(0, "0.05")
        self.exposure_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(param_frame, text="Set", command=self.set_exposure).grid(row=0, column=2, padx=5, pady=5)

        # Wavelength
        ttk.Label(param_frame, text="Wavelength (nm):").grid(row=1, column=0, padx=5, pady=5)
        self.wavelength_entry = ttk.Entry(param_frame)
        self.wavelength_entry.insert(0, "450.0")
        self.wavelength_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(param_frame, text="Set", command=self.set_wavelength).grid(row=1, column=2, padx=5, pady=5)

        # Stage controls
        stage_frame = ttk.LabelFrame(self, text="Stage Control")
        stage_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(stage_frame, text="Start Position (mm):").grid(row=0, column=0, padx=5, pady=5)
        self.start_pos_entry = ttk.Entry(stage_frame)
        self.start_pos_entry.insert(0, "12.0")
        self.start_pos_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(stage_frame, text="End Position (mm):").grid(row=1, column=0, padx=5, pady=5)
        self.end_pos_entry = ttk.Entry(stage_frame)
        self.end_pos_entry.insert(0, "13.5")
        self.end_pos_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(stage_frame, text="Step Size (mm):").grid(row=2, column=0, padx=5, pady=5)
        self.step_size_entry = ttk.Entry(stage_frame)
        self.step_size_entry.insert(0, "0.1")
        self.step_size_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(stage_frame, text="Home Stage", command=self.home_stage).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(stage_frame, text="Acquire Spectra", command=self.acquire_spectra).grid(row=1, column=2, padx=5, pady=5)

        # Current position display
        ttk.Label(stage_frame, text="Current Position (mm):").grid(row=2, column=2, padx=5, pady=5)
        ttk.Label(stage_frame, textvariable=self.current_pos).grid(row=2, column=3, padx=5, pady=5)

        # Plotting controls
        plot_frame = ttk.LabelFrame(self, text="Plotting")
        plot_frame.pack(padx=10, pady=10, fill="x")

        ttk.Button(plot_frame, text="Plot Spectra", command=self.plot_spectra).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(plot_frame, text="Clear Data", command=self.clear_data).grid(row=0, column=1, padx=5, pady=5)

    def set_exposure(self):
        try:
            exp = float(self.exposure_entry.get())
            set_exposure_time(exp)
            self.status_label.config(text=f"Exposure set to {exp} s")
        except ValueError:
            messagebox.showerror("Error", "Invalid exposure time")

    def set_wavelength(self):
        try:
            wl = float(self.wavelength_entry.get())
            set_wavelength(self.device_andor, wl)
            self.status_label.config(text=f"Wavelength set to {wl} nm")
        except ValueError:
            messagebox.showerror("Error", "Invalid wavelength")

    def home_stage(self):
        threading.Thread(target=lambda: home_stage(self.device_kcube, ask_user=False), daemon=True).start()
        self.status_label.config(text="Stage homed")

    def acquire_spectra(self):
        def run_acquisition():
            try:
                start = float(self.start_pos_entry.get())
                end = float(self.end_pos_entry.get())
                step = float(self.step_size_entry.get())
                steps = int(abs(end - start) / step) + 1

                move_to_position(self.device_kcube, start)
                self.current_pos.set(start)
                time.sleep(0.1)  # Delay before first acquisition

                for i in range(steps):
                    pos = start + i * step * (1 if end > start else -1)
                    if (end > start and pos > end) or (end < start and pos < end):
                        pos = end
                    self.status_label.config(text=f"Acquiring at {pos:.2f} mm")
                    time.sleep(0.3)  # Delay after stepping, before acquisition
                    spectrum = acquire_spectra()
                    self.spectra_data.append((pos, spectrum))
                    self.save_spectrum(spectrum, pos)
                    self.current_pos.set(pos)
                    if pos != end:
                        move_to_position(self.device_kcube, pos + step * (1 if end > start else -1))
                        time.sleep(0.3)  # Delay before next step
                self.status_label.config(text="Acquisition complete")
            except Exception as e:
                messagebox.showerror("Error", f"Acquisition failed: {e}")

        threading.Thread(target=run_acquisition, daemon=True).start()

    def plot_spectra(self):
        if not self.spectra_data:
            messagebox.showinfo("Info", "No spectra to plot")
            return
        fig = plt.figure(figsize=(10, 6))
        for pos, spectrum in self.spectra_data:
            plt.plot(spectrum, label=f"Pos {pos:.2f} mm")
        plt.xlabel("Pixel")
        plt.ylabel("Intensity")
        plt.title("Spectra at Different Stage Positions")
        plt.legend()
        plt.show()

    def clear_data(self):
        self.spectra_data.clear()
        self.status_label.config(text="Spectra data cleared")

    def save_spectrum(self, spectrum, position):
        if not os.path.exists(self.experiment_dir):
            os.makedirs(self.experiment_dir)
        filename = f"{self.experiment_name}_pos_{position:.2f}mm_{int(time.time())}.txt"
        filepath = os.path.join(self.experiment_dir, filename)
        np.savetxt(filepath, spectrum, fmt="%d", header=f"Position: {position} mm, Intensity (counts)")
        print(f"Saved spectrum to {filepath}")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Shut down hardware and exit?"):
            if self.temp_thread and self.temp_thread.is_alive():
                self.temp_thread.join()
            shutdown()
            if self.device_kcube:
                shutdown_kcube(self.device_kcube)
            self.destroy()

if __name__ == "__main__":
    app = SpectrometerGUI()
    app.mainloop()