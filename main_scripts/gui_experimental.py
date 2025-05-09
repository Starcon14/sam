# -*- coding: utf-8 -*-
"""

Created on Fri Feb 28 2025

@author: Jake Beets

Version: 0.1.2

Description: 
The main goal of this program is to provide a UI to automate the data collection for a CARS
system. The program will be able interface with a Thorlabs stage and an Andor spectrometer. 
The program will allow the user to connect, control, manage input, and provide feedback on 
the automated data collection and the status of connected devices. 


Requirements:
    customtkinter
    tkinter

"""


import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext
import sys
import traceback

import kcube_functions
import acquisition as aq

axis1 = kcube_functions.kcube()





# -------------------------------------------
# ------- GUI Functions & Classes
# -----------------------


def position_updater():
    a1_position.set(str(axis1.position))
    a1_connected.set(str(axis1.isconnected))
    a1_homed.set(str(axis1.ishomed))
    window.after(250, position_updater)

def read_input():
    
     axis1.delta = float(stepsize_entry.get())
     axis1.start = float(start_entry.get())
     axis1.end = float(end_entry.get())


def on_close():
    # if tk.messagebox.askokcancel("Quit", "Shut down hardware and exit?"):
    #     thread1 = axis1.disconnect_stage()
    #     thread1.join()
    #     window.destroy()
    #     print("Window Closed")
    window.destroy()
    k=0

def convert():
    
    k=0

class txt_redirect():
    def __init__(self, term_out, tag = "stdout"):
        self.term_out = term_out
        self.tag = tag
        
    def write(self, message):
        self.term_out.config(state = 'normal')
        self.term_out.insert(tk.END, message, self.tag)
        self.term_out.insert(tk.END,'\n')
        self.term_out.see(tk.END)
        self.term_out.config(state = 'disabled')
    
    def flush(self):
        pass

    

# -----------------------
# ------- GUI Functions
# -------------------------------------------






# ----- Initial Window
window = ctk.CTk()
window.title("Stage Acquisition Manager")
window.geometry("1100x630")
# ----- Initial Window

# ------ Font Definitions
base_font = ctk.CTkFont(family="Courier New", 
                          size=14)
base1_font = ctk.CTkFont(family="Courier New", 
                          size=16)
percent_font = ctk.CTkFont(family="Courier New", 
                          size=20)
pos_font1 = ctk.CTkFont(family="Courier New", 
                          size=40)
aquire_font = ctk.CTkFont(family="Courier New", 
                          size=30)
status_font = ctk.CTkFont(family="Courier New",
                          size=24)
# ------ Font Definitions

# ------ Variables

progress_str = ctk.StringVar()
progress_str.set('0.0%')
# ------ Variables


#-----------Grid Frames------------------------------


#------------------------------
frame_col0 = ctk.CTkFrame(master = window,
                      width = 340,
                      height = 630,
                      fg_color = "gray15")
frame_col0.grid(row = 0, column = 0)
#------------------------------

#------------------------------
frame_col1 = ctk.CTkFrame(master = window,
                      width = 600,
                      height = 630,
                      fg_color = "gray15")
frame_col1.grid(row = 0, column = 1)
#------------------------------


#-----------Grid Frames------------------------------





# -------------------------------------------
# ------- Progress, Position, and Start Frame (frame0)
# -----------------------


f0_color1 = "#03C03C"
f0_color2 = "#289A4A"
f0_color3 = "#26362B"
frame0 = ctk.CTkFrame(master = frame_col0,
                      width = 340,
                      height = 200,
                      border_width = 5,
                      border_color = f0_color2)
frame0.pack_propagate(False)
frame0.pack(pady = 5)

# ------- Progress Bar
progress_bar = ctk.CTkProgressBar(master = frame0,
                                 orientation="horizontal",
                                 height = 40,
                                 width = 300,
                                 corner_radius = 10,
                                 progress_color = f0_color2)
progress_bar.set(0)
progress_bar.pack(pady = 20,
                  padx = 20)
# ------- Progress Bar

# ------- Pecentage Label
percent_label = ctk.CTkLabel(master = frame0,
                             text = "0.0%",
                             font = percent_font,
                             fg_color = "transparent",
                             text_color = "gray74",
                             textvariable = progress_str)
percent_string = ctk.StringVar()
percent_label.place(x = 65,
                    y = 40,
                    anchor = "center")
# ------- Pecentage Label

# ------- Acquisition Timer Label
c_pos = ctk.CTkLabel(master = frame0,
                     text = "Timer",
                     width = 300,
                     font = pos_font1,
                     text_color = f0_color1,
                     #textvariable = s1_pos,
                     anchor = "e")
c_pos.place(x = 20,
            y = 80)
# ------- Acquisition Timer Label

# ------- Start Button
aquire_button = ctk.CTkButton(master = frame0, 
                    text = 'Start', 
                    command = lambda: aq.acquire(axis1, progress_bar, progress_str),
                    font = aquire_font,
                    text_color = f0_color1,
                    fg_color = "gray17",
                    border_color = f0_color2,
                    hover_color = f0_color3,
                    border_width = 2)
aquire_button.place(x = 20,
                    y = 80)
# ------- Start Button

# ------- Stop Button
stop_button = ctk.CTkButton(master = frame0, 
                    text = 'Stop', 
                    command = lambda: aq.stop_aquire_unthreaded(),
                    font = aquire_font,
                    text_color = "FireBrick3",
                    fg_color = "gray17",
                    border_color = "FireBrick3",
                    hover_color = "FireBrick2",
                    border_width = 2)
stop_button.place(x = 20,
                  y = 140)
# ------- Stop Button

# ------- Confirm Stop Button
stop_checkbox = ctk.CTkCheckBox(master = frame0,
                                text = "Confirm Stop",
                                font = base_font,
                                text_color = "FireBrick3",
                                hover_color = "FireBrick2",
                                border_color = "FireBrick4",
                                fg_color = "FireBrick4")
stop_checkbox.place(x = 183,
                   y = 148)
# ------- Confirm Stop Button




# -----------------------
# ------- Progress, Position, and Start Frame (frame0)
# -------------------------------------------




# -------------------------------------------
# ------- Terminal Emulator & User Feedback (frame1)
# -----------------------
f1_color1 = "#03C03C"
f1_color2 = "#289A4A"
f1_color3 = "#26362B"
frame1 = ctk.CTkFrame(master = frame_col0,
                      width = 340,
                      height = 400,
                      border_width = 5,
                      border_color = f1_color2)
frame1.pack_propagate(False)
frame1.pack(pady = 5, padx = 10)


# ------- Terminal Window
term_out = scrolledtext.ScrolledText(master = frame1,
                                     wrap = 'word',
                                     background = 'gray15',
                                     foreground = 'lime',
                                     font = ("Courier New", 12),
                                     height = 400)
term_out.config(insertbackground = 'lime',
                state = 'disabled')
term_out.pack(pady = 5, padx = 10)

# ------- Terminal Window


sys.stdout = txt_redirect(term_out, "stdout")
sys.stderr = txt_redirect(term_out, "stderr")



# -----------------------
# ------- Terminal Emulator & User Feedback (frame1)
# -------------------------------------------




# -------------------------------------------
# ------- Tab View (frame2)
# -----------------------


tabs = ctk.CTkTabview(master = frame_col1,
                      height = 600,
                      width = 650,
                      border_width = 5)
tabs._segmented_button.configure(font = percent_font,
                                 border_width = 8)

tabs.pack_propagate(False)
tabs.pack(pady = 10, padx = 10)

tabs.add('Axes')
tabs.add('Spectrometer')
tabs.add('Settings')
tabs.add('Status')
tabs.add('Live View')



# -----------------------
# ------- Tab View (frame2)
# -------------------------------------------





# -------------------------------------------
# ------- Control and Modify Axes (tab1)
# -----------------------

f2_color1 = "#00C7E6"
f2_color2 = "#068599"
f2_color3 = "#133D44"


# ------- Jog Label
jog_label = ctk.CTkLabel(master = tabs.tab('Axes'),
                         text = "Jog(mm)",
                         font = percent_font,
                         text_color = f2_color1)
jog_label.place(x = 10,
                y = 5)
# ------- Jog Label

# ------- Jog Entry
jog_entry = ctk.CTkEntry(master = tabs.tab('Axes'),
                         text_color = f2_color1,
                         font = percent_font,
                         width = 172)
jog_entry.place(x = 10,
                y = 45) 

# ------- Jog Entry

# ------- Jog Button Positive
jog_pos = ctk.CTkButton(master = tabs.tab('Axes'), 
                    text = '+', 
                    command = lambda: axis1.jog_stage_pos(jog_entry),
                    font = percent_font,
                    text_color = f2_color1,
                    fg_color = "gray17",
                    border_color = f2_color2,
                    hover_color = f2_color3,
                    border_width = 2,
                    width = 40)
jog_pos.place(x = 100,
              y = 5)
# ------- Jog Button Positive

# ------- Jog Button Negative
jog_neg = ctk.CTkButton(master = tabs.tab('Axes'), 
                    text = '-', 
                    command = lambda: axis1.jog_stage_neg(jog_entry),
                    font = percent_font,
                    text_color = f2_color1,
                    fg_color = "gray17",
                    border_color = f2_color2,
                    hover_color = f2_color3,
                    border_width = 2,
                    width = 40)
jog_neg.place(x = 140,
              y = 5)
# ------- Jog Button Negative


# ------- Move To Button 
move_pos = ctk.CTkButton(master = tabs.tab('Axes'), 
                    text = 'Move(mm)', 
                    command = lambda: axis1.move_stage(move_entry),
                    font = percent_font,
                    text_color = f2_color1,
                    fg_color = "gray17",
                    border_color = f2_color2,
                    hover_color = f2_color3,
                    border_width = 2,
                    width = 140)
move_pos.place(x = 200,
               y = 5)
# ------- Move To Button 

# ------- Move To Entry
move_entry = ctk.CTkEntry(master = tabs.tab('Axes'),
                         text_color = f2_color1,
                         font = percent_font,
                         width = 140)
move_entry.place(x = 200,
                 y = 45) 
# ------- Move To Entry

# ------- Stage Connect & Disconnect Buttons
stage_connect = ctk.CTkButton(master = tabs.tab('Axes'), 
                    text = 'Connect', 
                    command = lambda: axis1.connect_stage(),
                    font = percent_font,
                    text_color = f2_color1,
                    fg_color = "gray17",
                    border_color = f2_color2,
                    hover_color = f2_color3,
                    border_width = 2,
                    width = 140,
                    height = 50)
stage_connect.place(x = 350,
                    y = 60)

stage_disconnect = ctk.CTkButton(master = tabs.tab('Axes'), 
                    text = 'Disconnect', 
                    command = lambda: axis1.disconnect_stage(),
                    font = percent_font,
                    text_color = f2_color1,
                    fg_color = "gray17",
                    border_color = f2_color2,
                    hover_color = f2_color3,
                    border_width = 2,
                    width = 140,
                    height = 50)
stage_disconnect.place(x = 490,
                       y = 60)
 
stage_home = ctk.CTkButton(master = tabs.tab('Axes'), 
                    text = 'Home Axis', 
                    command = lambda: axis1.home_stage(),
                    font = percent_font,
                    text_color = f2_color1,
                    fg_color = "gray17",
                    border_color = f2_color2,
                    hover_color = f2_color3,
                    border_width = 2,
                    width = 140,
                    height = 50)
stage_home.place(x = 490,
                 y = 5)   

all_axes_checkbox = ctk.CTkCheckBox(master = tabs.tab('Axes'),
                                text = "All",
                                font = percent_font,
                                text_color = f2_color1,
                                hover_color = f2_color3,
                                border_color = f2_color2,
                                fg_color = f2_color3,
                                width = 40)
all_axes_checkbox.place(x = 390,
                   y = 15)
# ------- Stage Connect, Home, & Disconnect Buttons

# ------- Axis 1 Controls
a1_position = ctk.StringVar()
a1_homed = ctk.StringVar()
a1_connected = ctk.StringVar()

a1_select = ctk.CTkButton(master = tabs.tab('Axes'), 
                              text = 'Axis 1', 
                              font = percent_font,
                              text_color = f2_color1,
                              fg_color = "gray17",
                              border_color = f2_color2,
                              hover_color = f2_color3,
                              border_width = 2,
                              width = 170,
                              height = 50)
a1_select.place(x = 10,
                    y = 120)

a1_name_entry = ctk.CTkEntry(master = tabs.tab('Axes'),
                         text_color = f2_color1,
                         font = base_font,
                         width = 170,
                         placeholder_text = "Axis 1 Name")
a1_name_entry.place(x = 10,
                    y = 180) 

a1_position_label = ctk.CTkLabel(master = tabs.tab('Axes'),
                                 textvariable = a1_position,
                                 font = percent_font,
                                 text_color = f2_color1,
                                 anchor = 'e',
                                 width = 110)
a1_position_label.place(x = 10,
                        y = 210)

a1_mm_label = ctk.CTkLabel(master = tabs.tab('Axes'),
                           text = "mm",
                           font = percent_font,
                           text_color = f2_color1)
a1_mm_label.place(x = 130,
                  y = 210)

a1_connected_label = ctk.CTkLabel(master = tabs.tab('Axes'),
                                   text = "Connected: ",
                                   font = base_font,
                                   text_color = f2_color1)
a1_connected_label.place(x = 10,
                         y = 230)

a1_cstatus_label = ctk.CTkLabel(master = tabs.tab('Axes'),
                                   font = base_font,
                                   text_color = f2_color1,
                                   textvariable = a1_connected)
a1_cstatus_label.place(x = 110,
                         y = 230)

a1_homed_label = ctk.CTkLabel(master = tabs.tab('Axes'),
                              text = "Homed: ",
                              font = base_font,
                              text_color = f2_color1)
a1_homed_label.place(x = 45,
                     y = 250)

a1_hstatus_label = ctk.CTkLabel(master = tabs.tab('Axes'),
                                font = base_font,
                                text_color = f2_color1,
                                textvariable = a1_homed)
a1_hstatus_label.place(x = 110,
                       y = 250)

# ------- Axis 1 Controls



# -----------------------
# ------- Control and Modify Axes (tab1)
# -------------------------------------------




# -------------------------------------------
# ------- Spectrometer Settings & Control (tab2)
# -----------------------

t2_color1 = "#00C7E6"
t2_color2 = "#068599"
t2_color3 = "#133D44"

s1_temp = ctk.StringVar()
s1_wavelength = ctk.StringVar()
s1_slit = ctk.StringVar()
s1_exposure = ctk.StringVar()
s1_temp.set('-70.456')
s1_wavelength.set('450')
s1_slit.set('10')
s1_exposure.set("1000000")


all_spec_checkbox = ctk.CTkCheckBox(master = tabs.tab('Spectrometer'),
                                    text = "All",
                                    font = percent_font,
                                    text_color = f2_color1,
                                    hover_color = f2_color3,
                                    border_color = f2_color2,
                                    fg_color = f2_color3,
                                    width = 40)
all_spec_checkbox.place(x = 520,
                        y = 15)


spec_connect = ctk.CTkButton(master = tabs.tab('Spectrometer'), 
                    text = 'Connect', 
                    command = lambda: axis1.connect_stage(),
                    font = percent_font,
                    text_color = f2_color1,
                    fg_color = "gray17",
                    border_color = f2_color2,
                    hover_color = f2_color3,
                    border_width = 2,
                    width = 140,
                    height = 50)
spec_connect.place(x = 490,
                    y = 50)

spec_disconnect = ctk.CTkButton(master = tabs.tab('Spectrometer'), 
                    text = 'Disconnect', 
                    command = lambda: axis1.connect_stage(),
                    font = percent_font,
                    text_color = f2_color1,
                    fg_color = "gray17",
                    border_color = f2_color2,
                    hover_color = f2_color3,
                    border_width = 2,
                    width = 140,
                    height = 50)
spec_disconnect.place(x = 490,
                    y = 105)

spec_input = ctk.CTkButton(master = tabs.tab('Spectrometer'), 
                    text = 'Input',
                    font = percent_font,
                    text_color = f2_color1,
                    fg_color = "gray17",
                    border_color = f2_color2,
                    hover_color = f2_color3,
                    border_width = 2,
                    width = 140,
                    height = 80)
spec_input.place(x = 490,
                 y = 160)




s1_select = ctk.CTkButton(master = tabs.tab('Spectrometer'), 
                              text = 'Spectrometer 1', 
                              font = percent_font,
                              text_color = t2_color1,
                              fg_color = "gray17",
                              border_color = t2_color2,
                              hover_color = t2_color3,
                              border_width = 2,
                              width = 170,
                              height = 50)
s1_select.place(x = 10,
                y = 5)

s1_name_entry = ctk.CTkEntry(master = tabs.tab('Spectrometer'),
                         text_color = t2_color1,
                         font = base_font,
                         width = 170,
                         placeholder_text = "Spec. 1 Name")
s1_name_entry.place(x = 10,
                    y = 60)

s1_temp_label = ctk.CTkLabel(master = tabs.tab('Spectrometer'),
                             text = 'Temp(°C):',
                             font = base1_font,
                             text_color = f2_color1,)
s1_temp_label.place(x = 220,
                    y = 0)

s1_tstatus_label = ctk.CTkLabel(master = tabs.tab('Spectrometer'),
                                font = base1_font,
                                text_color = f2_color1,
                                textvariable = s1_temp)
s1_tstatus_label.place(x = 310,
                       y = 0)

s1_temp_entry = ctk.CTkEntry(master = tabs.tab('Spectrometer'),
                             text_color = t2_color1,
                             font = base_font,
                             width = 110,
                             placeholder_text = "Set Temp",)
s1_temp_entry.place(x = 360,
                    y = 0)

s1_wavelength_label = ctk.CTkLabel(master = tabs.tab('Spectrometer'),
                                   font = base1_font,
                                   text_color = f2_color1,
                                   text = "λ(nm):")
s1_wavelength_label.place(x = 220,
                          y = 40)

s1_wstatus_label = ctk.CTkLabel(master = tabs.tab('Spectrometer'),
                                   font = base1_font,
                                   text_color = f2_color1,
                                   textvariable = s1_wavelength)
s1_wstatus_label.place(x = 280,
                       y = 40)

s1_wavelength_entry = ctk.CTkEntry(master = tabs.tab('Spectrometer'),
                                   text_color = t2_color1,
                                   font = base_font,
                                   width = 110,
                                   placeholder_text = "Set λ",)
s1_wavelength_entry.place(x = 360,
                          y = 40)



s1_slit_label = ctk.CTkLabel(master = tabs.tab('Spectrometer'),
                                   font = base1_font,
                                   text_color = f2_color1,
                                   text = "Slit(µm):")
s1_slit_label.place(x = 190,
                    y = 80)

s1_sstatus_label = ctk.CTkLabel(master = tabs.tab('Spectrometer'),
                                   font = base1_font,
                                   text_color = f2_color1,
                                   textvariable = s1_slit)
s1_sstatus_label.place(x = 280,
                       y = 80)

s1_slit_entry = ctk.CTkEntry(master = tabs.tab('Spectrometer'),
                                   text_color = t2_color1,
                                   font = base_font,
                                   width = 110,
                                   placeholder_text = "Set Slit",)
s1_slit_entry.place(x = 360,
                        y = 80)



s1_exposure_label = ctk.CTkLabel(master = tabs.tab('Spectrometer'),
                                   font = base1_font,
                                   text_color = f2_color1,
                                   text = "Exposure(ms):")
s1_exposure_label.place(x = 10,
                          y = 120)

s1_estatus_label = ctk.CTkLabel(master = tabs.tab('Spectrometer'),
                                   font = base1_font,
                                   text_color = f2_color1,
                                   textvariable = s1_exposure)
s1_estatus_label.place(x = 145,
                       y = 120)

s1_exposure_entry = ctk.CTkEntry(master = tabs.tab('Spectrometer'),
                                   text_color = t2_color1,
                                   font = base_font,
                                   width = 180,
                                   placeholder_text = "Set Exposure",)
s1_exposure_entry.place(x = 230,
                        y = 120)


# -----------------------
# ------- Spectrometer Settings & Control (tab2)
# -------------------------------------------





# -------------------------------------------
# ------- Acquisition & Other Settings (tab4)
# -----------------------


f3_color1 = "#B587D4"
f3_color2 = "#70438E"
f3_color3 = "#331249"



# ------- Directory Button
directory_button = ctk.CTkButton(master = tabs.tab("Settings"), 
                    text = 'Browse Directory',
                    font = percent_font,
                    text_color = f3_color1,
                    fg_color = "gray17",
                    border_color = f3_color2,
                    hover_color = f3_color3,
                    border_width = 2,
                    height = 40)
directory_button.place(x = 10,
                      y = 10)
# ------- Directory Button

# ------- Directory Entry
directory_entry = ctk.CTkEntry(master = tabs.tab("Settings"),
                               text_color = f3_color1,
                               font = percent_font,
                               width = 400,
                               placeholder_text = "Select or Type Directory")
directory_entry.place(x = 230,
                      y = 15) 
# ------- Directory Entry


# ------- Start Label
start_label = ctk.CTkLabel(master = tabs.tab("Settings"),
                         text = "Start(mm):",
                         font = percent_font,
                         text_color = f3_color1)
start_label.place(x = 490,
                  y = 50)
# ------- Start Label

# ------- Start Entry
start_entry = ctk.CTkEntry(master = tabs.tab("Settings"),
                         text_color = f3_color1,
                         font = percent_font)
start_entry.place(x = 490,
                  y = 80) 
# ------- Start Entry

# ------- End Label
end_label = ctk.CTkLabel(master = tabs.tab("Settings"),
                         text = "End(mm):",
                         font = percent_font,
                         text_color = f3_color1)
end_label.place(x = 490,
                y = 110)
# ------- End Label

# ------- End Entry
end_entry = ctk.CTkEntry(master = tabs.tab("Settings"),
                         text_color = f3_color1,
                         font = percent_font)
end_entry.place(x = 490,
                y = 140) 
# ------- End Entry

# ------- Stepsize Label
stepsize_label = ctk.CTkLabel(master = tabs.tab("Settings"),
                              text = "Stepsize(mm):",
                              font = base1_font,
                              text_color = f3_color1)
stepsize_label.place(x = 490,
                     y = 175)
# ------- Stepsize Label

# ------- Stepsize Entry
stepsize_entry = ctk.CTkEntry(master = tabs.tab("Settings"),
                              text_color = f3_color1,
                              font = percent_font)
stepsize_entry.place(x = 490,
                     y = 200) 
# ------- Stepsize Entry


# ------- Input Parameters Button 
input_paramters = ctk.CTkButton(master = tabs.tab("Settings"), 
                    text = 'Input', 
                    command = lambda: read_input(),
                    font = percent_font,
                    text_color = f3_color1,
                    fg_color = "gray17",
                    border_color = f3_color2,
                    hover_color = f3_color3,
                    border_width = 2,
                    width = 140,
                    height = 90)
input_paramters.place(x = 490,
                      y = 250)
# ------- Input Parameters Button 

# ------- Axis 1 Button
input_paramters = ctk.CTkButton(master = tabs.tab("Settings"), 
                    text = "Axis 1", 
                    font = percent_font,
                    text_color = f3_color1,
                    fg_color = "gray17",
                    border_color = f3_color2,
                    hover_color = f3_color3,
                    border_width = 2)
input_paramters.place(x = 10,
                      y = 80)


# -----------------------
# ------- Acquisition & Other Settings (tab4)
# -------------------------------------------








# -------------------------------------------
# ------- Homing & Connection Status Frame (tab3)
# -----------------------



f5_color1 = "#D6AC38"
f5_color2 = "#9D7B20"
f5_color3 = "#594612"
frame5 = ctk.CTkFrame(master = tabs.tab('Status'),
                      width = 340,
                      height = 380,
                      border_width = 5,
                      border_color = f5_color2)
frame5.pack_propagate(False)
frame5.pack(pady = 10, padx = 10)


# ------- Status Title
status_title = ctk.CTkLabel(master = frame5,
                         text = "Status",
                         font = pos_font1,
                         text_color = f5_color1)
status_title.place(x = 90,
                   y = 10)
# ------- Status Title

# ------- Stage Connection Status
stage_connection_label = ctk.CTkLabel(master = frame5,
                         text = "Stage Connection: ",
                         font = percent_font,
                         text_color = f5_color2)
stage_connection_label.place(x = 20,
                             y = 60)
stage_connect_string = ctk.StringVar()
stage_connection_status = ctk.CTkLabel(master = frame5,
                         text = "Standby",
                         #textvariable = stage_connect_string,
                         font = status_font,
                         text_color = f5_color1,
                         textvariable = a1_connected)
stage_connection_status.place(x = 20,
                              y = 90)
# ------- Stage Connection Status

# ------- Stage Homed Status
stage_homed_label = ctk.CTkLabel(master = frame5,
                         text = "Stage Homed: ",
                         font = percent_font,
                         text_color = f5_color2)
stage_homed_label.place(x = 20,
                        y = 120)
stage_homed_string = ctk.StringVar()
stage_homed_status = ctk.CTkLabel(master = frame5,
                         text = "Standby",
                         #textvariable = stage_position_string,
                         font = status_font,
                         text_color = f5_color1,
                         textvariable = a1_homed)
stage_homed_status.place(x = 20,
                         y = 150)
# ------- Stage Homed Status

# ------- Stage Position Status
stage_connection_label = ctk.CTkLabel(master = frame5,
                         text = "Stage Position: ",
                         font = percent_font,
                         text_color = f5_color2)
stage_connection_label.place(x = 20,
                             y = 180)
stage_position_string = ctk.StringVar()
stage_connection_status = ctk.CTkLabel(master = frame5,
                         text = "Standby",
                         #textvariable = stage_position_string,
                         font = status_font,
                         text_color = f5_color1)
stage_connection_status.place(x = 20,
                              y = 210)
# ------- Stage Position Status

# ------- Number of Steps Taken
step_count_label = ctk.CTkLabel(master = frame5,
                         text = "Steps Taken: ",
                         font = percent_font,
                         text_color = f5_color2)
step_count_label.place(x = 20,
                             y = 240)
step_count_string = ctk.StringVar()
step_count_status = ctk.CTkLabel(master = frame5,
                         text = "Standby",
                         #textvariable = stage_position_string,
                         font = status_font,
                         text_color = f5_color1)
step_count_status.place(x = 20,
                              y = 270)
# ------- Stage Position Status




# -----------------------
# ------- Homing & Connection Status Frame (tab3)
# -------------------------------------------






# ------ Run Main Loop
window.protocol("WM_DELETE_WINDOW", on_close)
position_updater()
window.mainloop()
# ------ Run Main Loop