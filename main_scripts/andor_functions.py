# -*- coding: utf-8 -*-
"""
Created on Fri May  9 17:54:39 2025

@author: kcube2
"""

import ctypes
import time
import numpy as np
import threading
import os


    
    
    
class andor():
    def __init__(self):
        
        
        self.is_connected = False
        self.t_stable = False
        self.current_temp = ctypes.c_float(0.0)
        self.t_lock = threading.Lock()
        
        
        # Importing DLLs and supporting SDK firmware
        self.SOLIS_FOLDER = b"C:\\Program Files\\Andor SOLIS\\"
        self.DLL_FOLDER = r"C:\\Program Files\\compiled_sdk"
        self.CAMERA_DLL_PATH = f"{self.DLL_FOLDER}\\atmcd64d.dll"
        self.SUPPORT_DLLS = [
            f"{self.DLL_FOLDER}\\atshamrock.dll",
            f"{self.DLL_FOLDER}\\UsbI2cIo64.dll",
        ]
        self.SHAMROCK_DLL_PATH = f"{self.DLL_FOLDER}\\atspectrograph.dll"

        for self.dll_path in self.SUPPORT_DLLS:
            if os.path.exists(self.dll_path):
                try:
                    ctypes.CDLL(self.dll_path)
                    print(f"Support DLL loaded: {self.dll_path}")
                except OSError as e:
                    print(f"Warning: Failed to load support DLL {self.dll_path}: {e}")
            else:
                print(f"Warning: Support DLL not found: {self.dll_path}")

        try:
            self.camera_dll = ctypes.CDLL(self.CAMERA_DLL_PATH)
            print(f"Camera DLL loaded from {self.CAMERA_DLL_PATH}")
        except OSError as e:
            print(f"Failed to load camera DLL: {e}. Ensure it's in {self.DLL_FOLDER}")
        try:
            self.shamrock_dll = ctypes.CDLL(self.SHAMROCK_DLL_PATH)
            print(f"Shamrock DLL loaded from {self.SHAMROCK_DLL_PATH}")
        except OSError as e:
            print(f"Failed to load Shamrock DLL: {e}. Ensure atspectrograph.dll is in {self.DLL_FOLDER}")
        
        
        
    def check_error(self, code, function_name):
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
            print(f"{function_name} failed with error: {error_codes.get(code, f'Unknown code {code}')} "
                            f"Check Shamrock power, connection, or ensure all DLLs are in {self.DLL_FOLDER}.")
        print(f"{function_name} succeeded")
        
        
        
    def initialize_camera(self):
        error = self.camera_dll.Initialize(ctypes.c_char_p(self.SOLIS_FOLDER))
        self.check_error(error, "Initialize")
        print("Camera initialized successfully")

        error = self.camera_dll.CoolerON()
        self.check_error(error, "CoolerON")
        print("Cooler turned on")
        error = self.camera_dll.SetReadMode(ctypes.c_int(0))
        self.check_error(error, "SetReadMode")
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