# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 15:58:44 2025

@author: kcube2
"""



import customtkinter as ctk
import tkinter as tk
import threading


# imports for use with Thorlabs API
import os
import time
import sys
import clr


# Thorlabs API reference and imports
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.KCube.StepperMotorCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.KCube.StepperMotorCLI import *
from System import Decimal  # necessary for real world units
import System



class kcube:
    def __init__(self):

        
        self.device = None
        self.ishomed = False
        self.isconnected = False
        self.serial_no = "26005869"
        self.position = 0.000000
        self.delta = 0
        self.start = 0
        self.end = 0
        
        
        
    # -------- Connect Stage -------- #
    
    
    def connect_stage_unthreaded(self):
        try:
            
            DeviceManagerCLI.BuildDeviceList()
            device = KCubeStepper.CreateKCubeStepper(self.serial_no)
        
            # Connect
            device.Connect(self.serial_no)
            time.sleep(0.25)  # wait statements are important to allow settings to be sent to the device

            # Get Device Information and display description
            device_info = device.GetDeviceInfo()
            print(device_info.Description)
            

            # Start polling and enable
            device.StartPolling(250)  #250ms polling rate
            time.sleep(0.25)
            device.EnableDevice()
            time.sleep(0.25)  # Wait for device to enable

            # Configure device#
            use_file_settings = DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings
            device.LoadMotorConfiguration(device.DeviceID, use_file_settings)
            # Get homing settings
            home_params = device.GetHomingParams()
            # Get/Set Velocity Params
            device_vel_params = device.GetVelocityParams()
            
            
            self.device = device
            self.isconnected = True
            self.pos_update_unthreaded()
            
            print('KCube Initialized')
            
        except Exception as e: 
            print(e)
        
    def connect_stage(self):
        
        threading.Thread(target=self.connect_stage_unthreaded, daemon=True).start()
    
    
    # -------- Connect Stage -------- #
    
    
    # -------- Disconnect Stage -------- #
    
    
    def disconnect_stage_unthreaded(self):
        
        while self.isconnected == False:
            time.sleep(0.2)
            tick = 1
            if tick > 100:
                raise Exception("disconnect_stage_unthreaded failed due to timeout. Make sure KCube has bee connected properly.")
        
        
        device = self.device  
        try:        
            device.StopPolling()
            time.sleep(0.25)
            device.Disconnect()
            
            self.isconnected = False
            
            self.device = device
            print("KCube Disconnected")
        
        except Exception as e:
            print(e)
    
    def disconnect_stage(self):
        
        threading.Thread(target=self.disconnect_stage_unthreaded, daemon=True).start()
        
        
    # -------- Disconnect Stage -------- #
    
    
    # -------- Home Stage -------- #
        
    
    def home_stage_unthreaded(self):
        
        while self.isconnected == False:
            time.sleep(0.25)
        
        device = self.device
        try:
            
            self.pos_update_unthreaded()
            
            print("Homing KCube...")
            device.Home(60000)  # 60 seconds
            print("KCube Homed")
        
            self.ishomed = True
            self.device = device
            self.pos_update_unthreaded()
            
        except Exception as e:
            print(e)
            
    def home_stage(self):
        
        threading.Thread(target=self.home_stage_unthreaded, daemon=True).start()
            
            
    # -------- Home Stage -------- #
    
    
    # -------- Jog Stage Positive -------- #
    
    
    def jog_stage_pos_unthreaded(self, jog_entry):
        
        device = self.device
        try:
            num = jog_entry.get()
            #num = jog_entry
            num = float(num)
            
            relative_step = Decimal(num)              # converts step size to Decimal
            device.SetMoveRelativeDistance(relative_step)   # sets relative step length
            device.MoveRelative(60000)
            
            self.pos_update_unthreaded()
            
        except Exception as e:
            print(e)
        
        self.device = device
        
    
    def jog_stage_pos(self, jog_entry):    
        
        threading.Thread(target=self.jog_stage_pos_unthreaded, args=(jog_entry,), daemon=True).start()
    
    
    
    # -------- Jog Stage Positive -------- #
    
    
    # -------- Jog Stage Negative -------- #
    
    
    def jog_stage_neg_unthreaded(self, jog_entry):
        
        device = self.device
        try:
            num = "-" + jog_entry.get()
            num = float(num)
        
            relative_step = Decimal(num)              # converts step size to Decimal
            device.SetMoveRelativeDistance(relative_step)   # sets relative step length
            device.MoveRelative(60000)
            
            self.pos_update_unthreaded()
        
        except Exception as e:
            print(e)
        
        self.device = device
    
    
    def jog_stage_neg(self, jog_entry):    
        
        threading.Thread(target=self.jog_stage_neg_unthreaded, args=(jog_entry,), daemon=True).start()
    
    # -------- Jog Stage Negative -------- #
    
    
    # -------- Move Stage Positive -------- #
    
    def move_stage_unthreaded(self, move_entry):
        
        device = self.device
        
        try:
            num = move_entry.get()
            num = float(num)
            
            absolute_step = Decimal(num)              # converts step size to Decimal
            device.SetMoveAbsolutePosition(absolute_step)   # sets relative step length
            device.MoveAbsolute(60000)
            
            self.pos_update_unthreaded()
            
        except Exception as e:
            print(e)
            
        self.device = device
        
        
    def move_stage(self, move_entry):
            
        threading.Thread(target=self.move_stage_unthreaded, args=(move_entry,), daemon=True).start()
    
    # -------- Move Stage Positive -------- #
    
    
    # -------- Position Updater -------- #
    
    
    def pos_update_unthreaded(self):
        
        device = self.device

        try:
            
            pos = device.Position
            pos = str(pos)
            pos = float(pos)
            pos = f"{pos:.6f}"
            
            self.position = pos

        except Exception as e:
            print(e)
        
    def pos_update(self):
        
        threading.Thread(target=self.pos_update_unthreaded, daemon=True).start()
        
    # -------- Position Updater -------- #

        