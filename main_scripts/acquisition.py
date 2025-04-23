# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 12:34:19 2025

@author: kcube2
"""

import customtkinter as ctk
import tkinter as tk
import threading
import time


def acquire_unthreaded(stage1, progress_bar, progress_str):
    
    
    try:
        # store user input variables
        delta = stage1.delta
        p0 = stage1.start
        pf = stage1.end
    
        # initialize loop control variables
        stepcount = 0
        steps = int( abs(pf - p0) / delta )
    
        # set up stage 1
        stage1.move_stage_unthreaded(p0)
        stage1.pos_update_unthreaded
        
        # progress bar updater
        progress = 0

        while steps > stepcount:
            
            # spectrometer acquire spectra
            
            stepcount += 1
            
            stage1.jog_stage_pos_unthreaded(delta)
            stage1.pos_update_unthreaded
            
            progress = stepcount / steps
            progress_bar.set(progress)
            progress = progress * 100
            p_str = f"{progress:06.2f}" + "%"
            print(progress)
            print(p_str)
            progress_str.set(p_str)
            
            time.sleep(2)
    
    except Exception as e:
        print(e)
 

def acquire(stage1, progress_bar, progress_str):
    threading.Thread(target=acquire_unthreaded, args=(stage1, progress_bar, progress_str), daemon=True).start()
      