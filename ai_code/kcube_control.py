import os
import time
import clr
from System import Decimal

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.KCube.StepperMotorCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI, DeviceConfiguration
from Thorlabs.MotionControl.GenericMotorCLI import MotorDirection
from Thorlabs.MotionControl.KCube.StepperMotorCLI import KCubeStepper

DEFAULT_SERIAL_NO = "26005869"

def check_error(code, function_name):
    if code != 0:
        raise Exception(f"{function_name} failed with error code {code}")

def initialize_kcube(serial_no=DEFAULT_SERIAL_NO, poll_rate=250, verbose=True):
    try:
        DeviceManagerCLI.BuildDeviceList()
        if verbose:
            print(f"Device list built, found {DeviceManagerCLI.GetDeviceListSize()} devices")

        device = KCubeStepper.CreateKCubeStepper(serial_no)
        device.Connect(serial_no)
        time.sleep(0.25)

        device.StartPolling(poll_rate)
        time.sleep(0.25)
        device.EnableDevice()
        time.sleep(0.25)

        device_info = device.GetDeviceInfo()
        if verbose:
            print(f"Connected to {device_info.Description} (Serial: {serial_no})")

        use_file_settings = DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings
        device.LoadMotorConfiguration(device.DeviceID, use_file_settings)

        return device
    except Exception as e:
        raise Exception(f"K-Cube initialization failed: {e}")

def home_stage(device, timeout=60000, ask_user=True, verbose=True):
    if ask_user:
        print("Do you want to home the stage? [y]/[n]")
        response = input().lower().strip()
        if response == "y":
            if verbose:
                print("Homing Motor...")
            device.Home(timeout)
            if verbose:
                print("Motor Homed.")
        elif response == "n":
            if verbose:
                print("Skipping Motor Homing")
                time.sleep(0.5)
                print("You probably should have homed it...")
        else:
            raise ValueError("Invalid input: Please enter 'y' or 'n'")
    else:
        if verbose:
            print("Homing Motor (auto)...")
        device.Home(timeout)
        if verbose:
            print("Motor Homed.")

def get_position(device):
    return device.Position

def move_to_position(device, position_mm, timeout=60000, verbose=True):
    pos = Decimal(position_mm)
    device.SetMoveAbsolutePosition(pos)
    if verbose:
        print(f"Moving to absolute position: {position_mm} mm")
    device.MoveAbsolute(timeout)
    if verbose:
        print(f"Reached position: {get_position(device)} mm")

def shutdown_kcube(device, verbose=True):
    try:
        device.StopPolling()
        time.sleep(0.25)
        device.Disconnect()
        if verbose:
            print("K-Cube disconnected successfully")
    except Exception as e:
        print(f"Error during K-Cube shutdown: {e}")