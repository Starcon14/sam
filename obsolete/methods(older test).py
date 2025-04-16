#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 12:11:43 2025

@author: Jake Beets

Version: 0.1.0

Changes: https://docs.google.com/document/d/1uxsw22l4aI11v3yd_o_6eYBWLN_Vuacpy6a7-J05IsA/edit?usp=sharing

Description: 
This module is designed to provide the methods and functionality for the automation GUI. 

Requirements:
    customtkinter
    tkinter
    Thorlabs Kinesis
"""

import customtkinter as ctk
import tkinter as tk


# imports for use with Thorlabs API
import os
import time
import sys





class stage_methods:
    def __init__(self):
        return
    
    
    
    
        
    def pb_updater(self, jog_entry, progress_bar):
        
        
        num = jog_entry.get()
        print(num)
        
        num = float(num)
        
        progress_bar.set(num)


    