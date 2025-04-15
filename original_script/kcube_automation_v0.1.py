# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 14:06:46 2025

@author: Jake Beets

Version: 0.1

Changes: none

Description: 
The main goal is to command and control a Thorlabs KST201 Stepper Motor Controller in 
conjunction with an Andor Spectrometer. This is a preliminary script to test the 
automation loop and integration with the spectrometer.

Requirements:
    pythonnet
    Full Thorlabs Kinesis installation


"""

import os
import time
import sys
import clr

# Add References to .NET libraries
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.KCube.StepperMotorCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.KCube.StepperMotorCLI import *
from System import Decimal  # necessary for real world units

def main():
    """The main entry point for the application"""

    # Uncomment this line if you are using the Kinesis Simulator
    #SimulationManager.Instance.InitializeSimulations()

    try:
        
        # ------ Initialization -----------------------------------------
        DeviceManagerCLI.BuildDeviceList()

        # create new device
        serial_no = "26005869"  # Replace this line with your device's serial number
        device = KCubeStepper.CreateKCubeStepper(serial_no)
        

        # Connect
        device.Connect(serial_no)
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
        device_config = device.LoadMotorConfiguration(device.DeviceID, use_file_settings)
        # Get homing settings
        home_params = device.GetHomingParams()
        # Get/Set Velocity Params
        device_vel_params = device.GetVelocityParams()
        
        # Ask user if they want to home the device
        print("Do you want to home the stage? [y]/[n]")
        init_home = input()
        
        if init_home == "y":
            # Home device
            print("Homing Motor...")
            device.Home(60000)  # 60 seconds
            print("Motor Homed.")
        elif init_home == "n":
            print("Skipping Motor Homing")
            time.sleep(0.5)
            print("You probably should have homed it Dominik...")
        else:
            device.StopPolling()
            device.Disconnect()
            time.sleep(.25)
            sys.exit("Error: Please enter [y] or [n] for homing on initialization.")
        
        # ------ Initialization -----------------------------------------
        
        # ------ Automation Loop -----------------------------------------
        
        exterior_connect = False
        
        # connect to spectrometer, devices, or other software
        while exterior_connect == False:
            exterior_connect = True
            
        
        # --------- Enter Automation Parameters --------
        start_pos = 12    # start position in mm
        end_pos = 13.5      # end position in mm
        step_size = .1   # step size in mm
        
        stepcount = 0        # track the number of steps taken by loop
        spec_flag = False    # tells loop to wait for spectrometer to signal ready
        stage_flag = False   # tells spectrometer that stage has finished moving
        # --------- Enter Automation Parameters --------
        
        
        s_pos = Decimal(start_pos)                      # converts start_pos to Decimal
        steps = abs(start_pos - end_pos) / step_size    # calculates number of steps to take
        relative_step = Decimal(step_size)              # converts step size to Decimal
        device.SetMoveRelativeDistance(relative_step)   # sets relative step length
        
        device.SetMoveAbsolutePosition(s_pos)      # sets stage to move to star_pos
        device.MoveAbsolute(60000)                 # commands stage to move to star_pos
        
        # stepping loop
        while steps > stepcount:
            stage_flag = False
            
            # wait for spectrometer to inidcate ready to step
            while spec_flag != True:
                time.sleep(2)
                
                spec_flag = True   # spectrometer feedback to stage
                
            stepcount += 1

            spec_flag = False      # reset flag
            device.MoveRelative(60000)
            stage_flag = True      # stage feedback to spectrometer
            
            print(f'Stage Position: {device.Position}')
            print(f'Step Count: {stepcount}')
                
        # ------ Automation Loop -----------------------------------------
        
        
        
        # Stop Polling and Disconnect
        device.StopPolling()
        device.Disconnect()
    except Exception as e:
        print(e)

    # Uncomment this line if you are using the Kinesis Simulator
    #SimulationManager.Instance.UninitializeSimulations()
    ...


if __name__ == "__main__":
    main()
        