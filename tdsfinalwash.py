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
milliGAT_V=milliGATFn()
milliGAT_U=milliGATFn()
milliGAT_L=milliGATFn()
valve_1=valveFn()
valve_2=valveFn()
#endparameter
#init
def autoprog_init():
    global milliGAT_V
    milliGAT_V.milliGAT_init('COM38', 'V', frame.lbl_init)
    milliGAT_V.lbl_milliGAT_sta = lbl_milliGAT_B_sta
    global milliGAT_U
    milliGAT_U.milliGAT_init('COM38', 'U', frame.lbl_init)
    milliGAT_U.lbl_milliGAT_sta = lbl_milliGAT_C_sta
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
    global milliGAT_V
    global milliGAT_U
    global milliGAT_I
    global milliGAT_J
    global milliGAT_L
    global valve_1
    global valve_2
    milliGAT_V.milliGAT_pumping('V', 0, 5000, lbl_2)
    milliGAT_U.milliGAT_pumping('U', 0, 5000, lbl_3)
    milliGAT_I.milliGAT_pumping('I', 0, 5000, lbl_4)
    milliGAT_J.milliGAT_pumping('J', 0, 5000, lbl_5)
    milliGAT_L.milliGAT_pumping('L', 0, 5000, lbl_6)
    valve_1.valve_go(0, 13, lbl_73) # DCM flush
    milliGAT_V.milliGAT_stoping('V', 10, lbl_74)
    milliGAT_U.milliGAT_stoping('U', 0, lbl_75)
    milliGAT_I.milliGAT_stoping('I', 0, lbl_76)
    milliGAT_J.milliGAT_stoping('J', 0, lbl_77)
    milliGAT_L.milliGAT_stoping('L', 0, lbl_78)
    autoprog_abort()
#endcmd
#abort
def autoprog_abort():
    milliGAT_V.close('V')
    milliGAT_U.close('U')
    milliGAT_I.close('I')
    milliGAT_J.close('J')
    milliGAT_L.close('L')
    valve_1.close()
    valve_2.close()
#endabort
#label
lbl_0 = tk.Label(fr_cmdInt, width = 75, text = 'Lactam alkylation: After 0 min, Valve 1 goes to position 1', anchor = 'w', justify = tk.LEFT)
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
lbl_7 = tk.Label(fr_cmdInt, width = 75, text = 'MeOH wash: After 1200 min, Valve 1 goes to position 11', anchor = 'w', justify = tk.LEFT)
lbl_7.pack()
lbl_8 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 11', anchor = 'w', justify = tk.LEFT)
lbl_8.pack()
lbl_9 = tk.Label(fr_cmdInt, width = 75, text = 'DMF wash: After 20 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_9.pack()
lbl_10 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_10.pack()
lbl_11 = tk.Label(fr_cmdInt, width = 75, text = 'Fmoc deprotection: After 20 min, Valve 1 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_11.pack()
lbl_12 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_12.pack()
lbl_13 = tk.Label(fr_cmdInt, width = 75, text = 'DCM wash: After 20 min, Valve 1 goes to position 13', anchor = 'w', justify = tk.LEFT)
lbl_13.pack()
lbl_14 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_14.pack()
lbl_15 = tk.Label(fr_cmdInt, width = 75, text = 'First amide coupling: After 20 min, Valve 1 goes to position 3', anchor = 'w', justify = tk.LEFT)
lbl_15.pack()
lbl_16 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 3', anchor = 'w', justify = tk.LEFT)
lbl_16.pack()
lbl_17 = tk.Label(fr_cmdInt, width = 75, text = 'DCM wash: After 120 min, Valve 1 goes to position 13', anchor = 'w', justify = tk.LEFT)
lbl_17.pack()
lbl_18 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_18.pack()
lbl_19 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, MilliGAT G pumps at 2 mL/min', anchor = 'w', justify = tk.LEFT)
lbl_19.pack()
lbl_20 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT H pumps at 2 mL/min', anchor = 'w', justify = tk.LEFT)
lbl_20.pack()
lbl_21 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT I pumps at 2 mL/min', anchor = 'w', justify = tk.LEFT)
lbl_21.pack()
lbl_22 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT J pumps at 2 mL/min', anchor = 'w', justify = tk.LEFT)
lbl_22.pack()
lbl_23 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT L pumps at 2 mL/min', anchor = 'w', justify = tk.LEFT)
lbl_23.pack()
lbl_24 = tk.Label(fr_cmdInt, width = 75, text = 'LiBH4 reduction: After 0 min, Valve 1 goes to position 4', anchor = 'w', justify = tk.LEFT)
lbl_24.pack()
lbl_25 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 4', anchor = 'w', justify = tk.LEFT)
lbl_25.pack()
lbl_26 = tk.Label(fr_cmdInt, width = 75, text = 'DCM wash: After 120 min, Valve 1 goes to position 13', anchor = 'w', justify = tk.LEFT)
lbl_26.pack()
lbl_27 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_27.pack()
lbl_28 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, MilliGAT G pumps at 5 mL/min', anchor = 'w', justify = tk.LEFT)
lbl_28.pack()
lbl_29 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, MilliGAT H pumps at 5 mL/min', anchor = 'w', justify = tk.LEFT)
lbl_29.pack()
lbl_30 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, MilliGAT I pumps at 5 mL/min', anchor = 'w', justify = tk.LEFT)
lbl_30.pack()
lbl_31 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, MilliGAT J pumps at 5 mL/min', anchor = 'w', justify = tk.LEFT)
lbl_31.pack()
lbl_32 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, MilliGAT L pumps at 5 mL/min', anchor = 'w', justify = tk.LEFT)
lbl_32.pack()
lbl_33 = tk.Label(fr_cmdInt, width = 75, text = 'MeOH wash: After 0 min, Valve 1 goes to position 11', anchor = 'w', justify = tk.LEFT)
lbl_33.pack()
lbl_34 = tk.Label(fr_cmdInt, width = 75, text = 'DMF wash: After 20 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_34.pack()
lbl_35 = tk.Label(fr_cmdInt, width = 75, text = 'DMP oxidation: After 20 min, Valve 1 goes to position 5', anchor = 'w', justify = tk.LEFT)
lbl_35.pack()
lbl_36 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 5', anchor = 'w', justify = tk.LEFT)
lbl_36.pack()
lbl_37 = tk.Label(fr_cmdInt, width = 75, text = 'DMF wash: After 240 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_37.pack()
lbl_38 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_38.pack()
lbl_39 = tk.Label(fr_cmdInt, width = 75, text = 'DCM wash: After 20 min, Valve 1 goes to position 13', anchor = 'w', justify = tk.LEFT)
lbl_39.pack()
lbl_40 = tk.Label(fr_cmdInt, width = 75, text = '3-PCR: After 20 min, Valve 1 goes to position 6', anchor = 'w', justify = tk.LEFT)
lbl_40.pack()
lbl_41 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 6', anchor = 'w', justify = tk.LEFT)
lbl_41.pack()
lbl_42 = tk.Label(fr_cmdInt, width = 75, text = 'DMF wash: After 360 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_42.pack()
lbl_43 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_43.pack()
lbl_44 = tk.Label(fr_cmdInt, width = 75, text = 'Fmoc deprotection: After 20 min, Valve 2 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_44.pack()
lbl_45 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_45.pack()
lbl_46 = tk.Label(fr_cmdInt, width = 75, text = 'DMF wash: After 20 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_46.pack()
lbl_47 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_47.pack()
lbl_48 = tk.Label(fr_cmdInt, width = 75, text = 'Second amide coupling: After 20 min, Valve 1 goes to position 7', anchor = 'w', justify = tk.LEFT)
lbl_48.pack()
lbl_49 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 7', anchor = 'w', justify = tk.LEFT)
lbl_49.pack()
lbl_50 = tk.Label(fr_cmdInt, width = 75, text = 'DMF wash: After 360 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_50.pack()
lbl_51 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_51.pack()
lbl_52 = tk.Label(fr_cmdInt, width = 75, text = 'Fmoc deprotection: After 20 min, Valve 1 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_52.pack()
lbl_53 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_53.pack()
lbl_54 = tk.Label(fr_cmdInt, width = 75, text = 'DCM wash: After 20 min, Valve 1 goes to position 13', anchor = 'w', justify = tk.LEFT)
lbl_54.pack()
lbl_55 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_55.pack()
lbl_56 = tk.Label(fr_cmdInt, width = 75, text = 'Third amide coupling: After 20 min, Valve 1 goes to position 8', anchor = 'w', justify = tk.LEFT)
lbl_56.pack()
lbl_57 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 8', anchor = 'w', justify = tk.LEFT)
lbl_57.pack()
lbl_58 = tk.Label(fr_cmdInt, width = 75, text = 'DCM wash: After 120 min, Valve 1 goes to position 13', anchor = 'w', justify = tk.LEFT)
lbl_58.pack()
lbl_59 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_59.pack()
lbl_60 = tk.Label(fr_cmdInt, width = 75, text = 'H2O/MeOH/THF wash: After 20 min, Valve 1 goes to position 14', anchor = 'w', justify = tk.LEFT)
lbl_60.pack()
lbl_61 = tk.Label(fr_cmdInt, width = 75, text = 'NaOH hydrolysis: After 20 min, Valve 1 goes to position 9', anchor = 'w', justify = tk.LEFT)
lbl_61.pack()
lbl_62 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 9', anchor = 'w', justify = tk.LEFT)
lbl_62.pack()
lbl_63 = tk.Label(fr_cmdInt, width = 75, text = 'MeOH wash: After 60 min, Valve 1 goes to position 11', anchor = 'w', justify = tk.LEFT)
lbl_63.pack()
lbl_64 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_64.pack()
lbl_65 = tk.Label(fr_cmdInt, width = 75, text = 'DMF wash: After 20 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_65.pack()
lbl_66 = tk.Label(fr_cmdInt, width = 75, text = 'DMP oxidation: After 20 min, Valve 1 goes to position 5', anchor = 'w', justify = tk.LEFT)
lbl_66.pack()
lbl_67 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 5', anchor = 'w', justify = tk.LEFT)
lbl_67.pack()
lbl_68 = tk.Label(fr_cmdInt, width = 75, text = 'DMF wash: After 20 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_68.pack()
lbl_69 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_69.pack()
lbl_70 = tk.Label(fr_cmdInt, width = 75, text = 'DCM wash: After 20 min, Valve 1 goes to position 13', anchor = 'w', justify = tk.LEFT)
lbl_70.pack()
lbl_71 = tk.Label(fr_cmdInt, width = 75, text = 'TFA cleavage: After 20 min, Valve 1 goes to position 10', anchor = 'w', justify = tk.LEFT)
lbl_71.pack()
lbl_72 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 10', anchor = 'w', justify = tk.LEFT)
lbl_72.pack()
lbl_73 = tk.Label(fr_cmdInt, width = 75, text = 'DCM flush: After 360 min, Valve 1 goes to position 13', anchor = 'w', justify = tk.LEFT)
lbl_73.pack()
lbl_74 = tk.Label(fr_cmdInt, width = 75, text = 'After 10 min, MilliGAT G stops pumping', anchor = 'w', justify = tk.LEFT)
lbl_74.pack()
lbl_75 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT H stops pumping', anchor = 'w', justify = tk.LEFT)
lbl_75.pack()
lbl_76 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT I stops pumping', anchor = 'w', justify = tk.LEFT)
lbl_76.pack()
lbl_77 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT J stops pumping', anchor = 'w', justify = tk.LEFT)
lbl_77.pack()
lbl_78 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT L stops pumping', anchor = 'w', justify = tk.LEFT)
lbl_78.pack()
#endlabel

frame.btn_start['command']=lambda:threading.Thread(target=autoprog_start, name='StartThread').start()
frame.btn_abort['command']=lambda:threading.Thread(target=autoprog_abort, name='StartThread').start()
frame.btn_init['command']=lambda:threading.Thread(target=autoprog_init, name='StartThread').start()
frame.window.mainloop()

