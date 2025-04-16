# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 15:08:36 2025

@author: kcube2
"""

import kcube_functions

stage1 = kcube_functions.kcube()

stage1.connect_stage()


stage1.home_stage()

test = False

while test == False:
    print("Please input jog value: ")
    k = input()
    
    
    if k == "exit":
        test = True
        print('Exiting...')
    else:
        print("Jogging...")
        stage1.jog_stage_pos(float(k))

    

stage1.disconnect_stage()



