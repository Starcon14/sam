#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 12:15:41 2025

@author: main_user
"""





import customtkinter as ctk
import tkinter as tk


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


serial_no = "26005869"





class stage_methods:
    def __init__(self):

        
        self.device = None
        
        return
    
    def connect_stage(self):
        try:
            
            
            DeviceManagerCLI.BuildDeviceList()
            self.device = KCubeStepper.CreateKCubeStepper(serial_no)
        
            # Connect
            self.device.Connect(serial_no)
            time.sleep(0.25)  # wait statements are important to allow settings to be sent to the device

            # Get Device Information and display description
            self.device_info = device.GetDeviceInfo()
            print(device_info.Description)

            # Start polling and enable
            self.device.StartPolling(250)  #250ms polling rate
            time.sleep(0.25)
            self.device.EnableDevice()
            time.sleep(0.25)  # Wait for device to enable

            # Configure device#
            use_file_settings = DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings
            self.device.LoadMotorConfiguration(self.device.DeviceID, use_file_settings)
            # Get homing settings
            home_params = self.device.GetHomingParams()
            # Get/Set Velocity Params
            device_vel_params = self.device.GetVelocityParams()
            
        except: 
            test = 1
        return self.device
        
    def disconnect_stage(self):
        
        self.device.StopPolling()
        time.sleep(0.25)
        self.device.Disconnect()
        #SimulationManager.Instance.UninitializeSimulations()
        print("hello")
        
        return self.device
        
    def home_stage():
        
        print("Homing Motor...")
        device.Home(60000)  # 60 seconds
        print("Motor Homed.")
        
        ishomed = True
        return ishomed
        
       
    
    def jog_stage_pos(self, jog_entry):
        
        num = jog_entry.get()
        
        num = float(num)
        
        relative_step = Decimal(1.0)              # converts step size to Decimal
        device.SetMoveRelativeDistance(relative_step)   # sets relative step length
        device.MoveRelative(60000)
        
    
    
    def jog_stage_neg(self, jog_entry):
        
        num = "-" + jog_entry.get()
        
        
        
        relative_step = Decimal(num)              # converts step size to Decimal
        device.SetMoveRelativeDistance(relative_step)   # sets relative step length
        device.MoveRelative(60000)
    
    
        
    def pb_updater(self, jog_entry, progress_bar):
        
        
        num = jog_entry.get()
        print(num)
        
        num = float(num)
        
        progress_bar.set(num)
        
    
    
        