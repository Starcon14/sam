# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 12:34:19 2025

@author: kcube2
"""

import customtkinter as ctk
import tkinter as tk
import threading

import kcube_functions
from System import Decimal  # necessary for real world units

def acquire_unthreaded(stage1):
    
    # store user input variables
    delta = stage1.delta
    p0 = stage1.start
    pf = stage1.end
    
    # initialize loop control variables
    stepcount = 0
    steps = int( abs(pf - p0) / delta )
    
    # set up stage 1
    s_pos = Decimal(p0)
    stage1.move_stage
    
    
    while steps > stepcount:
        
        # spectrometer acquire spectra
        
        stepcount += 1
    




def acquire(stage1):
    f=0
      