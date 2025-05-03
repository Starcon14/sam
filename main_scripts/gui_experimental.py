# -*- coding: utf-8 -*-
"""

Created on Fri Feb 28 2025

@author: Jake Beets

Version: 0.1.2

Changes: https://docs.google.com/document/d/1uxsw22l4aI11v3yd_o_6eYBWLN_Vuacpy6a7-J05IsA/edit?usp=sharing

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

import kcube_functions
import acquisition as aq

stage1 = kcube_functions.kcube()





# -------------------------------------------
# ------- GUI Functions & Classes
# -----------------------


def position_updater():
    s1_pos.set(str(stage1.position))
    s1_connected.set(str(stage1.isconnected))
    s1_homed.set(str(stage1.ishomed))
    window.after(250, position_updater)

def read_input():
    
     stage1.delta = float(stepsize_entry.get())
     stage1.start = float(start_entry.get())
     stage1.end = float(end_entry.get())


def on_close():
    # if tk.messagebox.askokcancel("Quit", "Shut down hardware and exit?"):
    #     thread1 = stage1.disconnect_stage()
    #     thread1.join()
    #     window.destroy()
    #     print("Window Closed")
    window.destroy()
    k=0

def convert():
    
    k=0



    
    

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
s1_pos = ctk.StringVar()
s1_connected = ctk.StringVar()
s1_homed = ctk.StringVar()

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
                    command = lambda: aq.acquire(stage1, progress_bar, progress_str),
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
                           )
term_out.config(insertbackground = 'lime',
                state = 'disabled'
                )
term_out.pack(pady = 5, padx = 10)

# ------- Terminal Window



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
tabs.add('Status')
tabs.add('Settings')
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
frame2 = ctk.CTkFrame(master = tabs.tab('Axes'),
                      width = 440,
                      height = 130,
                      border_width = 5,
                      border_color = f2_color2)
frame2.pack_propagate(False)
frame2.pack(pady = 10)

# ------- Jog Label
jog_label = ctk.CTkLabel(master = frame2,
                         text = "Jog:",
                         font = percent_font,
                         text_color = f2_color1)
jog_label.place(x = 20,
                y = 20)
# ------- Jog Label

# ------- Jog Entry
jog_entry = ctk.CTkEntry(master = frame2,
                         text_color = f2_color1,
                         font = percent_font)
jog_entry.place(x = 80,
                y = 20) 
jog_label1 = ctk.CTkLabel(master = frame2,
                     text = "mm",
                     font = percent_font,
                     text_color = f2_color1)
jog_label1.place(x = 230,
                 y = 20)

# ------- Jog Entry

# ------- Jog Button Positive
jog_pos = ctk.CTkButton(master = frame2, 
                    text = '+', 
                    command = lambda: stage1.jog_stage_pos(jog_entry),
                    font = percent_font,
                    text_color = f2_color1,
                    fg_color = "gray17",
                    border_color = f2_color2,
                    hover_color = f2_color3,
                    border_width = 2,
                    width = 70)
jog_pos.place(x = 270,
              y = 20)
# ------- Jog Button Positive

# ------- Jog Button Negative
jog_neg = ctk.CTkButton(master = frame2, 
                    text = '-', 
                    command = lambda: stage1.jog_stage_neg(jog_entry),
                    font = percent_font,
                    text_color = f2_color1,
                    fg_color = "gray17",
                    border_color = f2_color2,
                    hover_color = f2_color3,
                    border_width = 2,
                    width = 70)
jog_neg.place(x = 350,
              y = 20)
# ------- Jog Button Negative

# ------- Move To Label
move_label = ctk.CTkLabel(master = frame2,
                         text = "Move \nTo:",
                         font = percent_font,
                         text_color = f2_color1)
move_label.place(x = 20,
                 y = 60)
# ------- Move To Label

# ------- Move To Entry
move_entry = ctk.CTkEntry(master = frame2,
                         text_color = f2_color1,
                         font = percent_font)
move_entry.place(x = 80,
                 y = 80) 
move_label1 = ctk.CTkLabel(master = frame2,
                     text = "mm",
                     font = percent_font,
                     text_color = f2_color1)
move_label1.place(x = 230,
                  y = 80)
# ------- Move To Entry

# ------- Move To Button 
move_pos = ctk.CTkButton(master = frame2, 
                    text = 'Move', 
                    command = lambda: stage1.move_stage(move_entry),
                    font = percent_font,
                    text_color = f2_color1,
                    fg_color = "gray17",
                    border_color = f2_color2,
                    hover_color = f2_color3,
                    border_width = 2,
                    width = 150)
move_pos.place(x = 270,
              y = 80)
# ------- Move To Button 



# -----------------------
# ------- Control and Modify Axes (tab1)
# -------------------------------------------




# -------------------------------------------
# ------- Acquisition & Other Settings (tab4)
# -----------------------


f3_color1 = "#B587D4"
f3_color2 = "#70438E"
f3_color3 = "#331249"
frame3 = ctk.CTkFrame(master = tabs.tab("Settings"),
                      width = 440,
                      height = 150,
                      border_width = 5,
                      border_color = f3_color2)
#frame3.pack_propagate(False)
frame3.pack(pady = 10)

# ------- Stepsize Label
stepsize_label = ctk.CTkLabel(master = frame3,
                         text = "Stepsize:",
                         font = percent_font,
                         text_color = f3_color1)
stepsize_label.place(x = 20,
                     y = 20)
# ------- Stepsize Label

# ------- Stepsize Entry
stepsize_entry = ctk.CTkEntry(master = frame3,
                         text_color = f3_color1,
                         font = percent_font)
stepsize_entry.place(x = 140,
                     y = 20) 
stepsize_label1 = ctk.CTkLabel(master = frame3,
                     text = "mm",
                     font = percent_font,
                     text_color = f3_color1)
stepsize_label1.place(x = 290,
                      y = 20)
# ------- Stepsize Entry

# ------- Start Label
start_label = ctk.CTkLabel(master = frame3,
                         text = "Start:",
                         font = percent_font,
                         text_color = f3_color1)
start_label.place(x = 20,
                  y = 60)
# ------- Start Label

# ------- Start Entry
start_entry = ctk.CTkEntry(master = frame3,
                         text_color = f3_color1,
                         font = percent_font)
start_entry.place(x = 140,
                     y = 60) 
start_label1 = ctk.CTkLabel(master = frame3,
                     text = "mm",
                     font = percent_font,
                     text_color = f3_color1)
start_label1.place(x = 290,
                      y = 60)
# ------- Start Entry

# ------- End Label
end_label = ctk.CTkLabel(master = frame3,
                         text = "End:",
                         font = percent_font,
                         text_color = f3_color1)
end_label.place(x = 20,
                y = 100)
# ------- End Label

# ------- End Entry
end_entry = ctk.CTkEntry(master = frame3,
                         text_color = f3_color1,
                         font = percent_font)
end_entry.place(x = 140,
                y = 100) 
end_label1 = ctk.CTkLabel(master = frame3,
                     text = "mm",
                     font = percent_font,
                     text_color = f3_color1)
end_label1.place(x = 290,
                 y = 100)
# ------- End Entry

# ------- Input Parameters Button 
input_paramters = ctk.CTkButton(master = frame3, 
                    text = 'Input', 
                    command = lambda: read_input(),
                    font = percent_font,
                    text_color = f3_color1,
                    fg_color = "gray17",
                    border_color = f3_color2,
                    hover_color = f3_color3,
                    border_width = 2,
                    width = 80,
                    height = 110)
input_paramters.place(x = 340,
                      y = 20)
# ------- Input Parameters Button 




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
                         textvariable = s1_connected)
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
                         textvariable = s1_homed)
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