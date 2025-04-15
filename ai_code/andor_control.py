import ctypes
import time
import numpy as np
import threading
import os

DLL_FOLDER = r"C:\Program Files\Andor SDK\Shamrock64"
CAMERA_DLL_PATH = f"{DLL_FOLDER}\\atmcd64d.dll"
SUPPORT_DLLS = [
    f"{DLL_FOLDER}\\atshamrock.dll",
    f"{DLL_FOLDER}\\UsbI2cIo64.dll",
]
SHAMROCK_DLL_PATH = f"{DLL_FOLDER}\\atspectrograph.dll"

for dll_path in SUPPORT_DLLS:
    if os.path.exists(dll_path):
        try:
            ctypes.CDLL(dll_path)
            print(f"Support DLL loaded: {dll_path}")
        except OSError as e:
            print(f"Warning: Failed to load support DLL {dll_path}: {e}")
    else:
        print(f"Warning: Support DLL not found: {dll_path}")

try:
    camera_dll = ctypes.CDLL(CAMERA_DLL_PATH)
    print(f"Camera DLL loaded from {CAMERA_DLL_PATH}")
except OSError as e:
    raise Exception(f"Failed to load camera DLL: {e}. Ensure it's in {DLL_FOLDER}")
try:
    shamrock_dll = ctypes.CDLL(SHAMROCK_DLL_PATH)
    print(f"Shamrock DLL loaded from {SHAMROCK_DLL_PATH}")
except OSError as e:
    raise Exception(f"Failed to load Shamrock DLL: {e}. Ensure atspectrograph.dll is in {DLL_FOLDER}")

temperature_stabilized = False
current_temperature = ctypes.c_float(0.0)
temperature_lock = threading.Lock()


def check_error(code, function_name):
    error_codes = {
        20002: "DRV_SUCCESS",
        20010: "DRV_NOT_INITIALIZED",
        20024: "DRV_TEMPERATURE_OFF",
        20033: "DRV_TEMPERATURE_STABILIZED",
        20034: "DRV_TEMP_NOT_STABILIZED",
        20035: "DRV_TEMP_NOT_REACHED",
        20075: "DRV_ERROR_ACK",
        20201: "SHAMROCK_COMMUNICATION_ERROR",
        20202: "SHAMROCK_SUCCESS",
        20275: "SHAMROCK_NOT_INITIALIZED"
    }
    if code not in (20002, 20202):
        raise Exception(f"{function_name} failed with error: {error_codes.get(code, f'Unknown code {code}')} "
                        f"Check Shamrock power, connection, or ensure all DLLs are in {DLL_FOLDER}.")
    print(f"{function_name} succeeded")


def initialize_camera():
    error = camera_dll.Initialize(ctypes.c_char_p(b"C:\\Program Files\\Andor SOLIS\\"))
    check_error(error, "Initialize")
    print("Camera initialized successfully")

    error = camera_dll.CoolerON()
    check_error(error, "CoolerON")
    print("Cooler turned on")
    error = camera_dll.SetReadMode(ctypes.c_int(0))
    check_error(error, "SetReadMode")
    print("Read mode set to Full Vertical Binning")
    time.sleep(3)


def initialize_shamrock():
    print("Initializing Shamrock...")
    tekst = ctypes.create_string_buffer(256)
    error = shamrock_dll.ShamrockInitialize(ctypes.byref(tekst))
    print(f"ShamrockInitialize output: {tekst.value.decode('utf-8', errors='ignore')}")
    check_error(error, "ShamrockInitialize")

    print("Attempting to detect Shamrock devices...")
    num_devices = ctypes.c_int()
    error = shamrock_dll.ShamrockGetNumberDevices(ctypes.byref(num_devices))
    check_error(error, "ShamrockGetNumberDevices")
    if num_devices.value == 0:
        raise Exception("No Shamrock devices detected. Check power, connection, and DLL folder.")
    print(f"Detected {num_devices.value} Shamrock device(s)")

    device = ctypes.c_int(0)
    print(f"Shamrock initialized successfully, device index: {device.value}")
    return device


def monitor_temperature(target_temp, timeout=600):
    global temperature_stabilized, current_temperature
    error = camera_dll.SetTemperature(ctypes.c_int(target_temp))
    check_error(error, "SetTemperature")
    print(f"Target temperature set to {target_temp}°C")

    start_time = time.time()
    while time.time() - start_time < timeout:
        temp = ctypes.c_float()
        error = camera_dll.GetTemperatureF(ctypes.byref(temp))
        with temperature_lock:
            current_temperature.value = temp.value
        print(f"Status code: {error}, Current temperature: {temp.value}°C")
        if error == 20033 or abs(temp.value - target_temp) < 0.5:
            with temperature_lock:
                temperature_stabilized = True
            print(f"Temperature stabilized at {temp.value}°C")
            break
        elif error == 20024:
            print("Cooler is off")
            break
        time.sleep(2)
    else:
        print("Temperature stabilization timed out")
        with temperature_lock:
            temperature_stabilized = True


def set_temperature(target_temp=-70):
    global temperature_stabilized
    temperature_stabilized = False
    temp_thread = threading.Thread(target=monitor_temperature, args=(target_temp,))
    temp_thread.start()
    return temp_thread


def is_temperature_stabilized():
    with temperature_lock:
        return temperature_stabilized, current_temperature.value


def set_exposure_time(exposure_time=0.05):
    exposure = ctypes.c_float(exposure_time)
    error = camera_dll.SetExposureTime(exposure)
    check_error(error, "SetExposureTime")
    print(f"Exposure time set to {exposure_time} seconds")


def set_wavelength(device, wavelength=450.0):
    wl = ctypes.c_float(wavelength)
    error = shamrock_dll.ShamrockSetWavelength(device, wl)
    check_error(error, "ShamrockSetWavelength")
    current_wl = ctypes.c_float()
    error = shamrock_dll.ShamrockGetWavelength(device, ctypes.byref(current_wl))
    check_error(error, "ShamrockGetWavelength")
    print(f"Center wavelength set to {wavelength} nm, verified at {current_wl.value} nm")


def acquire_spectra():
    error = camera_dll.SetReadMode(ctypes.c_int(0))
    check_error(error, "SetReadMode")
    error = camera_dll.SetHSSpeed(ctypes.c_int(0), ctypes.c_int(1))
    check_error(error, "SetHSSpeed")
    width = ctypes.c_int()
    height = ctypes.c_int()
    error = camera_dll.GetDetector(ctypes.byref(width), ctypes.byref(height))
    check_error(error, "GetDetector")
    data_size = width.value
    data = (ctypes.c_int * data_size)()
    error = camera_dll.StartAcquisition()
    check_error(error, "StartAcquisition")
    while True:
        status = ctypes.c_int()
        error = camera_dll.GetStatus(ctypes.byref(status))
        if status.value == 20073:
            break
        time.sleep(0.01)
    error = camera_dll.GetAcquiredData(data, ctypes.c_uint(data_size))
    check_error(error, "GetAcquiredData")
    print("Spectra acquired successfully")
    return np.array(data)


def shutdown():
    try:
        camera_dll.CoolerOFF()
        print("Cooler turned off")
    except Exception as e:
        print(f"Error turning off cooler: {e}")
    try:
        camera_dll.ShutDown()
        print("Camera shut down")
    except Exception as e:
        print(f"Error shutting down camera: {e}")
    try:
        shamrock_dll.ShamrockClose()
        print("Shamrock closed")
    except Exception as e:
        print(f"Error closing Shamrock: {e}")
    print("System shut down safely")