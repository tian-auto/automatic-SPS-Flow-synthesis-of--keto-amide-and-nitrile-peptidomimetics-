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
    valve_1.valve_go(0, 1, lbl_0) # 1: lactam
    valve_2.valve_go(0, 1, lbl_1) # position 1 recirculation: lactam
    milliGAT_G.milliGAT_pumping('G', 0, 5000, lbl_2)
    milliGAT_H.milliGAT_pumping('H', 0, 5000, lbl_3)
    milliGAT_I.milliGAT_pumping('I', 0, 5000, lbl_4)
    milliGAT_J.milliGAT_pumping('J', 0, 5000, lbl_5)
    milliGAT_L.milliGAT_pumping('L', 0, 5000, lbl_6)
    valve_1.valve_go(1200, 11, lbl_7) # MeOH wash
    valve_2.valve_go(0, 11, lbl_8) # to waste 1
    valve_1.valve_go(20, 12, lbl_9) # DMF wash
    valve_2.valve_go(0, 12, lbl_10) # to waste 2
    valve_1.valve_go(20, 2, lbl_11) # 2: piperidine
    valve_2.valve_go(0, 2, lbl_12) # piperidine recirculation
    valve_1.valve_go(20, 13, lbl_13) # DCM wash
    valve_2.valve_go(0, 12, lbl_14) # to waste 2
    valve_1.valve_go(20, 3, lbl_15) # 3: EDCI 1st coupling
    valve_2.valve_go(0, 3, lbl_16) # 1st coupling recirculation
    valve_1.valve_go(120, 13, lbl_17) # DCM wash
    valve_2.valve_go(0, 12, lbl_18) # to waste 2
    milliGAT_G.milliGAT_pumping('G', 20, 2000, lbl_19) # change flow rate
    milliGAT_H.milliGAT_pumping('H', 0, 2000, lbl_20)
    milliGAT_I.milliGAT_pumping('I', 0, 2000, lbl_21)
    milliGAT_J.milliGAT_pumping('J', 0, 2000, lbl_22)
    milliGAT_L.milliGAT_pumping('L', 0, 2000, lbl_23)
    valve_1.valve_go(0, 4, lbl_24) # 4: Reduction
    valve_2.valve_go(0, 4, lbl_25)
    valve_1.valve_go(120, 13, lbl_26) # DCM wash
    valve_2.valve_go(0, 12, lbl_27)
    milliGAT_G.milliGAT_pumping('G', 20, 5000, lbl_28) # change flow rate
    milliGAT_H.milliGAT_pumping('H', 0, 5000, lbl_29)
    milliGAT_I.milliGAT_pumping('I', 0, 5000, lbl_30)
    milliGAT_J.milliGAT_pumping('J', 0, 5000, lbl_31)
    milliGAT_L.milliGAT_pumping('L', 0, 5000, lbl_32)
    valve_1.valve_go(20, 11, lbl_33) # MeOH wash
    valve_1.valve_go(20, 12, lbl_34) # DMF wash
    valve_1.valve_go(20, 5, lbl_35) # 5: oxidation
    valve_2.valve_go(0, 5, lbl_36)
    valve_1.valve_go(240, 12, lbl_37) # DMF wash
    valve_2.valve_go(0, 12, lbl_38)
    valve_1.valve_go(20, 13, lbl_39) # DCM wash
    valve_1.valve_go(20, 6, lbl_40) # 6: 3-PCR
    valve_2.valve_go(0, 6, lbl_41)
    valve_1.valve_go(360, 12, lbl_42) # DMF wash
    valve_2.valve_go(0, 12, lbl_43)
    valve_1.valve_go(20, 2, lbl_44) # 2: piperidine
    valve_2.valve_go(0, 2, lbl_45)
    valve_1.valve_go(20, 12, lbl_46) # DMF wash
    valve_2.valve_go(0, 12, lbl_47)
    valve_1.valve_go(20, 7, lbl_48) # 7: HATU 2nd coupling
    valve_2.valve_go(0, 7, lbl_49)
    valve_1.valve_go(360, 12, lbl_50) # DMF wash
    valve_2.valve_go(0, 12, lbl_51)
    valve_1.valve_go(20, 2, lbl_52) # 2: piperidine
    valve_2.valve_go(0, 2, lbl_53)
    valve_1.valve_go(20, 13, lbl_54) # DCM wash
    valve_2.valve_go(0, 12, lbl_55)
    valve_1.valve_go(20, 8, lbl_56) # 8: EDCI 3rd coupling
    valve_2.valve_go(0, 8, lbl_57)    
    valve_1.valve_go(120, 13, lbl_58) # DCM wash
    valve_2.valve_go(0, 12, lbl_59)
    valve_1.valve_go(20, 14, lbl_60) # H2O/MeOH/THF wash
    valve_1.valve_go(20, 9, lbl_61) # 9: NaOH hydrolysis
    valve_2.valve_go(0, 9, lbl_62)
    valve_1.valve_go(120, 11, lbl_63) # MeOH wash
    valve_2.valve_go(0, 12, lbl_64)
    valve_1.valve_go(20, 12, lbl_65) # DMF wash
    valve_1.valve_go(20, 5, lbl_66) # 5: oxidation
    valve_2.valve_go(0, 5, lbl_67)
    valve_1.valve_go(240, 12, lbl_68) # DMF wash
    valve_2.valve_go(0, 12, lbl_69)
    valve_1.valve_go(20, 13, lbl_70) # DCM wash
    valve_1.valve_go(20, 10, lbl_71) # 10: TFA cleavage
    valve_2.valve_go(0, 10, lbl_72)
    valve_1.valve_go(360, 13, lbl_73) # DCM flush
    milliGAT_G.milliGAT_stoping('G', 10, lbl_74)
    milliGAT_H.milliGAT_stoping('H', 0, lbl_75)
    milliGAT_I.milliGAT_stoping('I', 0, lbl_76)
    milliGAT_J.milliGAT_stoping('J', 0, lbl_77)
    milliGAT_L.milliGAT_stoping('L', 0, lbl_78)
    autoprog_abort()
#endcmd
#abort
def autoprog_abort():
    milliGAT_G.close('G')
    milliGAT_H.close('H')
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
lbl_28 = tk.Label(fr_cmdInt, width = 75, text = 'MeOH wash: After 20 min, Valve 1 goes to position 11', anchor = 'w', justify = tk.LEFT)
lbl_28.pack()
lbl_29 = tk.Label(fr_cmdInt, width = 75, text = 'DMF wash: After 20 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_29.pack()
lbl_30 = tk.Label(fr_cmdInt, width = 75, text = 'DMP oxidation: After 20 min, Valve 1 goes to position 5', anchor = 'w', justify = tk.LEFT)
lbl_30.pack()
lbl_31 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 5', anchor = 'w', justify = tk.LEFT)
lbl_31.pack()
lbl_32 = tk.Label(fr_cmdInt, width = 75, text = 'DMF wash: After 240 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_32.pack()
lbl_33 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_33.pack()
lbl_34 = tk.Label(fr_cmdInt, width = 75, text = 'DCM wash: After 20 min, Valve 1 goes to position 13', anchor = 'w', justify = tk.LEFT)
lbl_34.pack()
lbl_35 = tk.Label(fr_cmdInt, width = 75, text = '3-PCR: After 20 min, Valve 1 goes to position 6', anchor = 'w', justify = tk.LEFT)
lbl_35.pack()
lbl_36 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 6', anchor = 'w', justify = tk.LEFT)
lbl_36.pack()
lbl_37 = tk.Label(fr_cmdInt, width = 75, text = 'DMF wash: After 360 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_37.pack()
lbl_38 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_38.pack()
lbl_39 = tk.Label(fr_cmdInt, width = 75, text = 'Fmoc deprotection: After 20 min, Valve 2 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_39.pack()
lbl_40 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_40.pack()
lbl_41 = tk.Label(fr_cmdInt, width = 75, text = 'DMF wash: After 20 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_41.pack()
lbl_42 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_42.pack()
lbl_43 = tk.Label(fr_cmdInt, width = 75, text = 'Second amide coupling: After 20 min, Valve 1 goes to position 7', anchor = 'w', justify = tk.LEFT)
lbl_43.pack()
lbl_44 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 7', anchor = 'w', justify = tk.LEFT)
lbl_44.pack()
lbl_45 = tk.Label(fr_cmdInt, width = 75, text = 'DMF wash: After 360 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_45.pack()
lbl_46 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_46.pack()
lbl_47 = tk.Label(fr_cmdInt, width = 75, text = 'Fmoc deprotection: After 20 min, Valve 1 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_47.pack()
lbl_48 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_48.pack()
lbl_49 = tk.Label(fr_cmdInt, width = 75, text = 'DCM wash: After 20 min, Valve 1 goes to position 13', anchor = 'w', justify = tk.LEFT)
lbl_49.pack()
lbl_50 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_50.pack()
lbl_51 = tk.Label(fr_cmdInt, width = 75, text = 'Third amide coupling: After 20 min, Valve 1 goes to position 8', anchor = 'w', justify = tk.LEFT)
lbl_51.pack()
lbl_52 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 8', anchor = 'w', justify = tk.LEFT)
lbl_52.pack()
lbl_53 = tk.Label(fr_cmdInt, width = 75, text = 'DCM wash: After 120 min, Valve 1 goes to position 13', anchor = 'w', justify = tk.LEFT)
lbl_53.pack()
lbl_54 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_54.pack()
lbl_55 = tk.Label(fr_cmdInt, width = 75, text = 'H2O/MeOH/THF wash: After 20 min, Valve 1 goes to position 14', anchor = 'w', justify = tk.LEFT)
lbl_55.pack()
lbl_56 = tk.Label(fr_cmdInt, width = 75, text = 'NaOH hydrolysis: After 20 min, Valve 1 goes to position 9', anchor = 'w', justify = tk.LEFT)
lbl_56.pack()
lbl_57 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 9', anchor = 'w', justify = tk.LEFT)
lbl_57.pack()
lbl_58 = tk.Label(fr_cmdInt, width = 75, text = 'MeOH wash: After 120 min, Valve 1 goes to position 11', anchor = 'w', justify = tk.LEFT)
lbl_58.pack()
lbl_59 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_59.pack()
lbl_60 = tk.Label(fr_cmdInt, width = 75, text = 'DMF wash: After 20 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_60.pack()
lbl_61 = tk.Label(fr_cmdInt, width = 75, text = 'DMP oxidation: After 20 min, Valve 1 goes to position 5', anchor = 'w', justify = tk.LEFT)
lbl_61.pack()
lbl_62 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 5', anchor = 'w', justify = tk.LEFT)
lbl_62.pack()
lbl_63 = tk.Label(fr_cmdInt, width = 75, text = 'DMF wash: After 20 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_63.pack()
lbl_64 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_64.pack()
lbl_65 = tk.Label(fr_cmdInt, width = 75, text = 'DCM wash: After 20 min, Valve 1 goes to position 13', anchor = 'w', justify = tk.LEFT)
lbl_65.pack()
lbl_66 = tk.Label(fr_cmdInt, width = 75, text = 'TFA cleavage: After 20 min, Valve 1 goes to position 10', anchor = 'w', justify = tk.LEFT)
lbl_66.pack()
lbl_67 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 10', anchor = 'w', justify = tk.LEFT)
lbl_67.pack()
lbl_68 = tk.Label(fr_cmdInt, width = 75, text = 'DCM flush: After 360 min, Valve 1 goes to position 13', anchor = 'w', justify = tk.LEFT)
lbl_68.pack()
lbl_69 = tk.Label(fr_cmdInt, width = 75, text = 'After 10 min, MilliGAT G stops pumping', anchor = 'w', justify = tk.LEFT)
lbl_69.pack()
lbl_70 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT H stops pumping', anchor = 'w', justify = tk.LEFT)
lbl_70.pack()
lbl_71 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT I stops pumping', anchor = 'w', justify = tk.LEFT)
lbl_71.pack()
lbl_72 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT J stops pumping', anchor = 'w', justify = tk.LEFT)
lbl_72.pack()
lbl_73 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT L stops pumping', anchor = 'w', justify = tk.LEFT)
lbl_73.pack()
#endlabel

frame.btn_start['command']=lambda:threading.Thread(target=autoprog_start, name='StartThread').start()
frame.btn_abort['command']=lambda:threading.Thread(target=autoprog_abort, name='StartThread').start()
frame.btn_init['command']=lambda:threading.Thread(target=autoprog_init, name='StartThread').start()
frame.window.mainloop()
