# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 12:34:19 2025

@author: kcube2
"""

import customtkinter as ctk
import tkinter as tk
import threading
import time


def acquire_unthreaded(stage1, progress_bar, progress_str, stop):
    
    
    try:
        # store user input variables
        delta = stage1.delta
        p0 = stage1.start
        pf = stage1.end
    
        # initialize loop control variables
        stepcount = 0
        steps = int( (pf - p0) / delta )
        
        
        # set up stage 1
        stage1.move_stage_unthreaded(p0)
        stage1.pos_update_unthreaded
        
        # progress bar updater
        progress = 0

        while abs(steps) > stepcount:
            
            if stop.is_set == True:
                
                e_str = "Acquisition canceled"
                
                raise Exception(e_str)
            
            # spectrometer acquire spectra
            
            stepcount += 1
            
            if steps > 0:
                stage1.jog_stage_pos_unthreaded(delta)
                
            elif steps < 0:
                stage1.jog_stage_neg_unthreaded(delta)
            
            stage1.pos_update_unthreaded
            
            progress = stepcount / abs(steps)
            progress_bar.set(progress)
            progress = progress * 100
            p_str = f"{progress:06.2f}" + "%"
            progress_str.set(p_str)
            
            time.sleep(2)
    
    except Exception as e:
        print(e)
 

def acquire(stage1, progress_bar, progress_str):
    thread1 = threading.Thread(target=acquire_unthreaded, 
                     args=(stage1, progress_bar, progress_str), daemon=True)
    thread1.start()
    return thread1


def stop_aquire_unthreaded():
    stop = threading.Event()
    

def stop_acquire():
    thread1 = threading.Thread(target=stop_aquire_unthreaded(), deamon=True)
    thread1.start()
    return thread1()
    