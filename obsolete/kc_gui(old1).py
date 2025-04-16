# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 23:05:22 2025

@author: kcube
"""


import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk

def convert():
    
    but_input = entry_int.get()
    but_output = but_input * 1.61
    
    output_string.set(but_output)


# ----- Initial Window
window = ctk.CTk()
window.title("KCube Automate Panel")
window.geometry("800x700")
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
# ------ Font Definitions



# -------------------------------------------
# ------- Progress, Position, and Start Frame (frame1)
# -----------------------



f1_color1 = "SpringGreen3"
f1_color2 = "SpringGreen4"
frame1 = ctk.CTkFrame(master = window,
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
                                 progress_color = f1_color1)
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
                     font = pos_font1,
                     text_color = f1_color1)
c_pos.place(x = 20,
            y = 75)
c_pos1 = ctk.CTkLabel(master = frame1,
                     text = "mm",
                     font = pos_font1,
                     text_color = f1_color2)
c_pos1.place(x = 330,
            y = 75)
# ------- Current Position Label

# ------- Start Button
aquire_button = ctk.CTkButton(master = frame1, 
                    text = ' Start \nAquisition', 
                    command = convert,
                    font = aquire_font,
                    text_color = f1_color2,
                    fg_color = "gray17",
                    border_color = f1_color2,
                    hover_color = f1_color1,
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



f2_color1 = "#23CDCD"
f2_color2 = "#1A9999"
frame2 = ctk.CTkFrame(master = window,
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
jog_var = ctk.IntVar()
jog_entry = ctk.CTkEntry(master = frame2,
                         textvariable = jog_var,
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
                    command = convert,
                    font = percent_font,
                    text_color = f2_color1,
                    fg_color = "gray17",
                    border_color = f2_color2,
                    hover_color = f2_color2,
                    border_width = 2,
                    width = 70)
jog_pos.place(x = 270,
              y = 20)
# ------- Jog Button Positive

# ------- Jog Button Negative
jog_neg = ctk.CTkButton(master = frame2, 
                    text = '-', 
                    command = convert,
                    font = percent_font,
                    text_color = f2_color1,
                    fg_color = "gray17",
                    border_color = f2_color2,
                    hover_color = f2_color2,
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
move_var = ctk.IntVar()
move_entry = ctk.CTkEntry(master = frame2,
                         textvariable = move_var,
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
                    command = convert,
                    font = percent_font,
                    text_color = f2_color1,
                    fg_color = "gray17",
                    border_color = f2_color2,
                    hover_color = f2_color2,
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



f3_color1 = "#23CDCD"
f3_color2 = "#1A9999"
frame3 = ctk.CTkFrame(master = window,
                      width = 440,
                      height = 190,
                      border_width = 5,
                      border_color = f3_color2)
frame3.pack_propagate(False)
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
# steps_label1 = ctk.CTkLabel(master = frame3,
#                      text = "mm",
#                      font = percent_font,
#                      text_color = f3_color1)
# steps_label1.place(x = 290,
#                    y = 60)
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
                    border_color = f2_color2,
                    hover_color = f2_color2,
                    border_width = 2,
                    width = 80,
                    height = 120)
input_paramters.place(x = 340,
                      y = 30)
# ------- Input Parameters Button 





# -----------------------
# ------- Aquisition Paramter Frame (frame3)
# -------------------------------------------





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
input_frame.pack(pady = 10)
# ------ Input Field 1

# ------ Output Field 1
output_string = ctk.StringVar()
output_label = ctk.CTkLabel(
    master = window, 
    text = "Output", 
    textvariable = output_string)

output_label.pack(pady = 5)
# ------ Output Field 1

# ------ Run Main Loop
window.mainloop()
# ------ Run Main Loop