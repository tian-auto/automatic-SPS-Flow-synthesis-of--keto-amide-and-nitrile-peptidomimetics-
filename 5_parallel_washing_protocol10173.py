from mttkinter import mtTkinter as tk
from tkinter import ttk
from interfaceFn import *
from heidolphFn import *
from milliGATFn import *
from valveFn import *
from sf10Fn import *
from asiapumpFn import *
from oushishengFn import *
from watsonFn import *
import time
import threading
frame = InterfaceFn()
fr_cmdInt = frame.fr_cmdInt
#parameter
milliGAT_I=milliGATFn()
milliGAT_J=milliGATFn()
milliGAT_G=milliGATFn()
milliGAT_H=milliGATFn()
milliGAT_L=milliGATFn()
valve_1=valveFn()
valve_2=valveFn()
#endparameter
#init
def autoprog_init():
    global milliGAT_G
    milliGAT_G.milliGAT_init('COM38', 'G', frame.lbl_init)
    milliGAT_G.lbl_milliGAT_sta = lbl_milliGAT_B_sta
    global milliGAT_H
    milliGAT_H.milliGAT_init('COM38', 'H', frame.lbl_init)
    milliGAT_H.lbl_milliGAT_sta = lbl_milliGAT_C_sta
    global milliGAT_I
    milliGAT_I.milliGAT_init('COM38', 'I', frame.lbl_init)
    milliGAT_I.lbl_milliGAT_sta = lbl_milliGAT_D_sta
    global milliGAT_J
    milliGAT_J.milliGAT_init('COM38', 'J', frame.lbl_init)
    milliGAT_J.lbl_milliGAT_sta = lbl_milliGAT_E_sta
    global milliGAT_L
    milliGAT_L.milliGAT_init('COM38', 'L', frame.lbl_init)
    milliGAT_L.lbl_milliGAT_sta = lbl_milliGAT_F_sta
    global valve_1
    valve_1.valve_init('COM37', 1, frame.lbl_init)
    valve_1.lbl_valve_sta = lbl_valve_1_sta
    global valve_2
    valve_2.valve_init('COM36', 2, frame.lbl_init)
    valve_2.lbl_valve_sta = lbl_valve_2_sta
#endinit
#cmd
def autoprog_start():
    global milliGAT_G
    global milliGAT_H
    global milliGAT_I
    global milliGAT_J
    global milliGAT_L
    global valve_1
    global valve_2
    valve_1.valve_go(0, 1, lbl_0)
    valve_2.valve_go(0, 1, lbl_1)
    milliGAT_G.milliGAT_pumping('G', 0, 5000, lbl_2)
    milliGAT_H.milliGAT_pumping('H', 0, 5000, lbl_3)
    milliGAT_I.milliGAT_pumping('I', 0, 5000, lbl_4)
    milliGAT_J.milliGAT_pumping('J', 0, 5000, lbl_5)
    milliGAT_L.milliGAT_pumping('L', 0, 5000, lbl_6)
    valve_1.valve_go(2, 2, lbl_7)
    valve_2.valve_go(0, 2, lbl_8)
    valve_1.valve_go(2, 3, lbl_9)
    valve_2.valve_go(0, 3, lbl_10)
    valve_1.valve_go(2, 4, lbl_11)
    valve_2.valve_go(0, 4, lbl_12)
    valve_1.valve_go(2, 5, lbl_13)
    valve_2.valve_go(0, 5, lbl_14)
    valve_1.valve_go(2, 6, lbl_15)
    valve_2.valve_go(0, 6, lbl_16)
    valve_1.valve_go(2, 7, lbl_17)
    valve_2.valve_go(0, 7, lbl_18)
    valve_1.valve_go(2, 8, lbl_19)
    valve_2.valve_go(0, 8, lbl_20)
    valve_1.valve_go(2, 9, lbl_21)
    valve_2.valve_go(0, 9, lbl_22)
    valve_1.valve_go(2, 10, lbl_23)
    valve_2.valve_go(0, 10, lbl_24)
    valve_1.valve_go(2, 11, lbl_25)
    valve_2.valve_go(0, 11, lbl_26)
    valve_1.valve_go(2, 12, lbl_27)
    valve_2.valve_go(0, 12, lbl_28)
    valve_1.valve_go(2, 13, lbl_29)
    valve_1.valve_go(2, 14, lbl_30)
    milliGAT_G.milliGAT_stoping('G', 2, lbl_31)
    milliGAT_H.milliGAT_stoping('H', 0, lbl_32)
    milliGAT_I.milliGAT_stoping('I', 0, lbl_33)
    milliGAT_J.milliGAT_stoping('J', 0, lbl_34)
    milliGAT_L.milliGAT_stoping('L', 0, lbl_35)
    autoprog_abort()
#endcmd
#abort
def autoprog_abort():
    milliGAT_U.close('G')
    milliGAT_V.close('H')
    milliGAT_I.close('I')
    milliGAT_J.close('J')
    milliGAT_L.close('L')
    valve_1.close()
    valve_2.close()
#endabort
#label
lbl_0 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 1 goes to position 1', anchor = 'w', justify = tk.LEFT)
lbl_0.pack()
lbl_1 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 1', anchor = 'w', justify = tk.LEFT)
lbl_1.pack()
lbl_2 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT G starts pumping at 5 mL/min', anchor = 'w', justify = tk.LEFT)
lbl_2.pack()
lbl_3 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT H starts pumping at 5 mL/min', anchor = 'w', justify = tk.LEFT)
lbl_3.pack()
lbl_4 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT I starts pumping at 5 mL/min', anchor = 'w', justify = tk.LEFT)
lbl_4.pack()
lbl_5 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT J starts pumping at 5 mL/min', anchor = 'w', justify = tk.LEFT)
lbl_5.pack()
lbl_6 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT L starts pumping at 5 mL/min', anchor = 'w', justify = tk.LEFT)
lbl_6.pack()
lbl_7 = tk.Label(fr_cmdInt, width = 75, text = 'After 2 min, Valve 1 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_7.pack()
lbl_8 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_8.pack()
lbl_9 = tk.Label(fr_cmdInt, width = 75, text = 'After 2 min, Valve 1 goes to position 3', anchor = 'w', justify = tk.LEFT)
lbl_9.pack()
lbl_10 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 3', anchor = 'w', justify = tk.LEFT)
lbl_10.pack()
lbl_11 = tk.Label(fr_cmdInt, width = 75, text = 'After 2 min, Valve 1 goes to position 4', anchor = 'w', justify = tk.LEFT)
lbl_11.pack()
lbl_12 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 4', anchor = 'w', justify = tk.LEFT)
lbl_12.pack()
lbl_13 = tk.Label(fr_cmdInt, width = 75, text = 'After 2 min, Valve 1 goes to position 5', anchor = 'w', justify = tk.LEFT)
lbl_13.pack()
lbl_14 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 5', anchor = 'w', justify = tk.LEFT)
lbl_14.pack()
lbl_15 = tk.Label(fr_cmdInt, width = 75, text = 'After 2 min, Valve 1 goes to position 6', anchor = 'w', justify = tk.LEFT)
lbl_15.pack()
lbl_16 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 6', anchor = 'w', justify = tk.LEFT)
lbl_16.pack()
lbl_17 = tk.Label(fr_cmdInt, width = 75, text = 'After 2 min, Valve 1 goes to position 7', anchor = 'w', justify = tk.LEFT)
lbl_17.pack()
lbl_18 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 7', anchor = 'w', justify = tk.LEFT)
lbl_18.pack()
lbl_19 = tk.Label(fr_cmdInt, width = 75, text = 'After 2 min, Valve 1 goes to position 8', anchor = 'w', justify = tk.LEFT)
lbl_19.pack()
lbl_20 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 8', anchor = 'w', justify = tk.LEFT)
lbl_20.pack()
lbl_21 = tk.Label(fr_cmdInt, width = 75, text = 'After 2 min, Valve 1 goes to position 9', anchor = 'w', justify = tk.LEFT)
lbl_21.pack()
lbl_22 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 9', anchor = 'w', justify = tk.LEFT)
lbl_22.pack()
lbl_23 = tk.Label(fr_cmdInt, width = 75, text = 'After 2 min, Valve 1 goes to position 10', anchor = 'w', justify = tk.LEFT)
lbl_23.pack()
lbl_24 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 10', anchor = 'w', justify = tk.LEFT)
lbl_24.pack()
lbl_25 = tk.Label(fr_cmdInt, width = 75, text = 'After 2 min, Valve 1 goes to position 11', anchor = 'w', justify = tk.LEFT)
lbl_25.pack()
lbl_26 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 11', anchor = 'w', justify = tk.LEFT)
lbl_26.pack()
lbl_27 = tk.Label(fr_cmdInt, width = 75, text = 'After 2 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_27.pack()
lbl_28 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_28.pack()
lbl_29 = tk.Label(fr_cmdInt, width = 75, text = 'After 2 min, Valve 1 goes to position 13', anchor = 'w', justify = tk.LEFT)
lbl_29.pack()
lbl_30 = tk.Label(fr_cmdInt, width = 75, text = 'After 2 min, Valve 1 goes to position 14', anchor = 'w', justify = tk.LEFT)
lbl_30.pack()
lbl_31 = tk.Label(fr_cmdInt, width = 75, text = 'After 2 min, MilliGAT G stops pumping', anchor = 'w', justify = tk.LEFT)
lbl_31.pack()
lbl_32 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT H stops pumping', anchor = 'w', justify = tk.LEFT)
lbl_32.pack()
lbl_33 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT I stops pumping', anchor = 'w', justify = tk.LEFT)
lbl_33.pack()
lbl_34 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT J stops pumping', anchor = 'w', justify = tk.LEFT)
lbl_34.pack()
lbl_35 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT L stops pumping', anchor = 'w', justify = tk.LEFT)
lbl_35.pack()
#endlabel

frame.btn_start['command']=lambda:threading.Thread(target=autoprog_start, name='StartThread').start()
frame.btn_abort['command']=lambda:threading.Thread(target=autoprog_abort, name='StartThread').start()
frame.btn_init['command']=lambda:threading.Thread(target=autoprog_init, name='StartThread').start()
frame.window.mainloop()
