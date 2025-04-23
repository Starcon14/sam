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
import ttkbootstrap as ttkb
import kcube_functions

stage1 = kcube_functions.kcube()




def position_updater():
    s1_pos.set(str(stage1.position))
    s1_connected.set(str(stage1.isconnected))
    s1_homed.set(str(stage1.ishomed))
    window.after(250, position_updater)


def convert():
    
    but_input = entry_int.get()
    but_output = but_input * 1.61
    
    output_string.set(but_output)
    



# ----- Initial Window
window = ctk.CTk()
window.title("KCube Automate Panel")
window.geometry("800x630")
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

# ------ Variables

#------------------------------
frame_col0 = ctk.CTkFrame(master = window,
                      width = 450,
                      height = 700,
                      fg_color = "gray15")
frame_col0.grid(row = 0, column = 1)
#------------------------------


#------------------------------
frame_col1 = ctk.CTkFrame(master = window,
                      width = 300,
                      height = 700,
                      fg_color = "gray15")
frame_col1.grid(row = 0, column = 2)
#------------------------------


# -------------------------------------------
# ------- Progress, Position, and Start Frame (frame1)
# -----------------------



f1_color1 = "#03C03C"
f1_color2 = "#289A4A"
f1_color3 = "#26362B"
frame1 = ctk.CTkFrame(master = frame_col0,
                      width = 440,
                      height = 250,
                      border_width = 5,
                      border_color = f1_color2)
frame1.pack_propagate(False)
frame1.pack(pady = 10)

# ------- Progress Bar
progress_bar = ctk.CTkProgressBar(master = frame1,
                                 orientation="horizontal",
                                 height = 40,
                                 width = 400,
                                 corner_radius = 10,
                                 progress_color = f1_color2)
progress_bar.set(0.9)
progress_bar.pack(pady = 20,
                  padx = 20)
# ------- Progress Bar

# ------- Pecentage Label
percent_label = ctk.CTkLabel(master = frame1,
                             text = "100.0%",
                             font = percent_font,
                             fg_color = "transparent",
                             text_color = "gray74")
percent_string = ctk.StringVar()
percent_label.place(x = 65,
                    y = 40,
                    anchor = "center")
# ------- Pecentage Label

# ------- Current Position Label
c_pos = ctk.CTkLabel(master = frame1,
                     text = "00.023423443",
                     width = 300,
                     font = pos_font1,
                     text_color = f1_color1,
                     textvariable = s1_pos,
                     anchor = "e")
c_pos.place(x = 20,
            y = 75)
c_pos1 = ctk.CTkLabel(master = frame1,
                     text = "mm",
                     font = pos_font1,
                     text_color = f1_color1)
c_pos1.place(x = 330,
            y = 75)
# ------- Current Position Label

# ------- Start Button
aquire_button = ctk.CTkButton(master = frame1, 
                    text = ' Start \nAquisition', 
                    command = convert,
                    font = aquire_font,
                    text_color = f1_color1,
                    fg_color = "gray17",
                    border_color = f1_color2,
                    hover_color = f1_color3,
                    border_width = 2)
aquire_button.place(x = 20,
                    y = 130)
# ------- Start Button

# ------- Stop Button
stop_button = ctk.CTkButton(master = frame1, 
                    text = ' Stop \nAquisition', 
                    command = convert,
                    font = aquire_font,
                    text_color = "FireBrick3",
                    fg_color = "gray17",
                    border_color = "FireBrick3",
                    hover_color = "FireBrick2",
                    border_width = 2)
stop_button.place(x = 230,
                  y = 130)
# ------- Stop Button

# ------- Confirm Stop Button
stop_checkbox = ctk.CTkCheckBox(master = frame1,
                                text = "Confirm Stop",
                                font = base_font,
                                text_color = "FireBrick3",
                                hover_color = "FireBrick2",
                                border_color = "FireBrick4",
                                fg_color = "FireBrick4")
stop_checkbox.place(x = 260,
                   y = 215)
# ------- Confirm Stop Button




# -----------------------
# ------- Progress, Position, and Start Frame (frame1)
# -------------------------------------------


# -------------------------------------------
# ------- Jog & Positioning Frame (frame2)
# -----------------------



f2_color1 = "#00C7E6"
f2_color2 = "#068599"
f2_color3 = "#133D44"
frame2 = ctk.CTkFrame(master = frame_col0,
                      width = 440,
                      height = 130,
                      border_width = 5,
                      border_color = f2_color2)
#frame2.pack_propagate(False)
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
# ------- Jog & Positioning Frame (frame2)
# -------------------------------------------



# -------------------------------------------
# ------- Aquisition Paramter Frame (frame3)
# -----------------------



f3_color1 = "#B587D4"
f3_color2 = "#70438E"
f3_color3 = "#331249"
frame3 = ctk.CTkFrame(master = frame_col0,
                      width = 440,
                      height = 190,
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
stepsize_var = ctk.IntVar()
stepsize_entry = ctk.CTkEntry(master = frame3,
                         textvariable = stepsize_var,
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

# ------- Steps Label
steps_label = ctk.CTkLabel(master = frame3,
                         text = "Steps:",
                         font = percent_font,
                         text_color = f3_color1)
steps_label.place(x = 20,
                  y = 60)
# ------- Steps Label

# ------- Steps Entry
steps_var = ctk.IntVar()
steps_entry = ctk.CTkEntry(master = frame3,
                         textvariable = steps_var,
                         text_color = f3_color1,
                         font = percent_font)
steps_entry.place(x = 140,
                  y = 60) 
# ------- Steps Entry

# ------- Start Label
stepsize_label = ctk.CTkLabel(master = frame3,
                         text = "Start:",
                         font = percent_font,
                         text_color = f3_color1)
stepsize_label.place(x = 20,
                     y = 100)
# ------- Start Label

# ------- Start Entry
start_var = ctk.IntVar()
start_entry = ctk.CTkEntry(master = frame3,
                         textvariable = start_var,
                         text_color = f3_color1,
                         font = percent_font)
start_entry.place(x = 140,
                     y = 100) 
start_label1 = ctk.CTkLabel(master = frame3,
                     text = "mm",
                     font = percent_font,
                     text_color = f3_color1)
start_label1.place(x = 290,
                      y = 100)
# ------- Start Entry

# ------- End Label
stepsize_label = ctk.CTkLabel(master = frame3,
                         text = "End:",
                         font = percent_font,
                         text_color = f3_color1)
stepsize_label.place(x = 20,
                     y = 140)
# ------- End Label

# ------- End Entry
end_var = ctk.IntVar()
end_entry = ctk.CTkEntry(master = frame3,
                         textvariable = end_var,
                         text_color = f3_color1,
                         font = percent_font)
end_entry.place(x = 140,
                     y = 140) 
end_label1 = ctk.CTkLabel(master = frame3,
                     text = "mm",
                     font = percent_font,
                     text_color = f3_color1)
end_label1.place(x = 290,
                      y = 140)
# ------- End Entry

# ------- Input Parameters Button 
input_paramters = ctk.CTkButton(master = frame3, 
                    text = 'Input', 
                    command = convert,
                    font = percent_font,
                    text_color = f3_color1,
                    fg_color = "gray17",
                    border_color = f3_color2,
                    hover_color = f3_color3,
                    border_width = 2,
                    width = 80,
                    height = 120)
input_paramters.place(x = 340,
                      y = 30)
# ------- Input Parameters Button 



# -----------------------
# ------- Aquisition Paramter Frame (frame3)
# -------------------------------------------




# -------------------------------------------
# ------- Stage and Spectrometer Recconect Buttons (frame4)
# -----------------------



f4_color1 = "#A98E7E"
f4_color2 = "#6E5749"
f4_color3 = "#3D3129"
frame4 = ctk.CTkFrame(master = frame_col1,
                      width = 340,
                      height = 210,
                      border_width = 5,
                      border_color = f4_color2)
frame4.pack_propagate(False)
frame4.pack(pady = 10, padx = 10)


# ------- Stage & Spectrometer Labels
stage_label = ctk.CTkLabel(master = frame4,
                         text = "Stage",
                         font = percent_font,
                         text_color = f4_color1)
stage_label.place(x = 60,
                  y = 20)
spectrometer_label = ctk.CTkLabel(master = frame4,
                         text = "Spectrometer",
                         font = percent_font,
                         text_color = f4_color1)
spectrometer_label.place(x = 175,
                         y = 20)
# ------- Stage & Spectrometer Labels

# ------- Stage Connect & Disconnect Buttons
stage_connect = ctk.CTkButton(master = frame4, 
                    text = 'Connect', 
                    command = lambda: stage1.connect_stage(),
                    font = percent_font,
                    text_color = f4_color1,
                    fg_color = "gray17",
                    border_color = f4_color2,
                    hover_color = f4_color3,
                    border_width = 2,
                    width = 140,
                    height = 60)
stage_connect.place(x = 20,
                      y = 60)
stage_disconnect = ctk.CTkButton(master = frame4, 
                    text = 'Disconnect', 
                    command = lambda: stage1.disconnect_stage(),
                    font = percent_font,
                    text_color = f4_color1,
                    fg_color = "gray17",
                    border_color = f4_color2,
                    hover_color = f4_color3,
                    border_width = 2,
                    width = 140,
                    height = 60)
stage_disconnect.place(x = 20,
                      y = 130)
# ------- Stage Connect & Disconnect Buttons  

# ------- Spectrometer Connect & Disconnect Buttons  
spec_connect = ctk.CTkButton(master = frame4, 
                    text = 'home stage', 
                    command = lambda: stage1.home_stage(),
                    font = percent_font,
                    text_color = f4_color1,
                    fg_color = "gray17",
                    border_color = f4_color2,
                    hover_color = f4_color3,
                    border_width = 2,
                    width = 140,
                    height = 60)
spec_connect.place(x = 180,
                      y = 60)
spec_disconnect = ctk.CTkButton(master = frame4, 
                    text = 'Disconnect', 
                    command = convert,
                    font = percent_font,
                    text_color = f4_color1,
                    fg_color = "gray17",
                    border_color = f4_color2,
                    hover_color = f4_color3,
                    border_width = 2,
                    width = 140,
                    height = 60)
spec_disconnect.place(x = 180,
                      y = 130)
# ------- Spectrometer Connect & Disconnect Buttons  




# -----------------------
# ------- Stage and Spectrometer Recconect Buttons (frame4)
# -------------------------------------------




# -------------------------------------------
# ------- Homing & Connection Status Frame (frame5)
# -----------------------



f5_color1 = "#D6AC38"
f5_color2 = "#9D7B20"
f5_color3 = "#594612"
frame5 = ctk.CTkFrame(master = frame_col1,
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
# ------- Homing & Connection Status Frame (frame5)
# -------------------------------------------


def convert():
    
    but_input = entry_int.get()
    but_output = but_input * 1.61
    
    output_string.set(but_output)


# ------ Input Field 1
input_frame = ctk.CTkFrame(master = window)
entry_int = ctk.IntVar()
entry = ctk.CTkEntry(master = input_frame, 
                     textvariable = entry_int)

button = ctk.CTkButton(master = input_frame, 
                    text = 'this is text test 0123456789', 
                    command = convert,
                    font = base_font)

entry.pack(side = 'left', 
           padx = 10)

button.pack(side = 'left')
input_frame.grid(row = 3, column = 1, pady = 10)
# ------ Input Field 1

# ------ Output Field 1
output_string = ctk.StringVar()
output_label = ctk.CTkLabel(
    master = window, 
    text = "Output", 
    textvariable = output_string)

output_label.grid(row = 4, column = 1, pady = 10)
# ------ Output Field 1

# ------ Run Main Loop
position_updater()
window.mainloop()
# ------ Run Main Loop