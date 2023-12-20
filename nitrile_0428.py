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
milliGAT_L=milliGATFn()
valve_1=valveFn()
valve_2=valveFn()
#endparameter
#init
def autoprog_init():
	global milliGAT_L
	milliGAT_L.milliGAT_init('COM38', 'L', frame.lbl_init)
	milliGAT_L.lbl_milliGAT_sta = lbl_milliGAT_B_sta
	global valve_1
	valve_1.valve_init('COM37', 1, frame.lbl_init)
	valve_1.lbl_valve_sta = lbl_valve_1_sta
	global valve_2
	valve_2.valve_init('COM36', 2, frame.lbl_init)
	valve_2.lbl_valve_sta = lbl_valve_2_sta
#endinit
#cmd
def autoprog_start():
	global milliGAT_L
	global valve_1
	global valve_2
	valve_1.valve_go(0, 1, lbl_0) # 1:lactam
	valve_2.valve_go(0, 1, lbl_1) # position 1 recirculation: lactam
	milliGAT_L.milliGAT_pumping('L', 0, 5000, lbl_2) # milliGAT starts pumping
	valve_2.valve_go(1080, 11, lbl_3) # to waste 1
	valve_1.valve_go(0, 11, lbl_4) # MeOH wash
	valve_1.valve_go(20, 12, lbl_5) # DMF wash
	valve_2.valve_go(0, 12, lbl_6) # to waste 2
	valve_1.valve_go(20, 2, lbl_7) # 2:piperidine
	valve_2.valve_go(0, 2, lbl_8) 
	valve_1.valve_go(20, 12, lbl_9) # DMF wash
	valve_2.valve_go(0, 12, lbl_10)
	valve_1.valve_go(20, 3, lbl_11) #3:1st amide coupling
	valve_2.valve_go(0, 3, lbl_12)
	valve_1.valve_go(120, 12, lbl_13) # DMF wash
	valve_2.valve_go(0, 12, lbl_14)
	valve_1.valve_go(20, 2, lbl_15) # 2:piperidine
	valve_2.valve_go(0, 2, lbl_16)
	valve_1.valve_go(20, 12, lbl_17) # DMF wash
	valve_2.valve_go(0, 12, lbl_18)
	valve_1.valve_go(20, 4, lbl_19) # 4:2nd amide coupling 
	valve_2.valve_go(0, 4, lbl_20)
	valve_1.valve_go(360, 12, lbl_21) # DMF wash
	valve_2.valve_go(0, 12, lbl_22)
	valve_1.valve_go(20, 2, lbl_23) # 2:piperidine
	valve_2.valve_go(0, 2, lbl_24)
	valve_1.valve_go(20, 12, lbl_25) # DMF wash
	valve_2.valve_go(0, 12, lbl_26)
	valve_1.valve_go(20, 5, lbl_27) # 5:3rd amide coupling
	valve_2.valve_go(0, 5, lbl_28)
	valve_1.valve_go(120, 14, lbl_29) # THF/MeOH/H2O wash
	valve_2.valve_go(0, 12, lbl_30)
	valve_1.valve_go(20, 6, lbl_31) # 6:hydrolysis
	valve_2.valve_go(0, 6, lbl_32)
	valve_1.valve_go(60, 11, lbl_33) # MeOH wash
	valve_2.valve_go(0, 12, lbl_34)
	valve_1.valve_go(20, 15, lbl_35) # 0.1M HCl in THF wash
	valve_1.valve_go(10, 16, lbl_36) # THF wash
	valve_1.valve_go(20, 7, lbl_37) # 7: CDI
	valve_2.valve_go(0, 7, lbl_38)
	valve_1.valve_go(30, 16, lbl_39) # THF wash
	valve_2.valve_go(0, 12, lbl_40) 
	valve_1.valve_go(10, 8, lbl_41) # 8: aminolysis
	valve_2.valve_go(0, 8, lbl_42)
	milliGAT_L.milliGAT_pumping('L', 0, 2000, lbl_43)
	valve_1.valve_go(120, 11, lbl_44) # MeOH wash
	milliGAT_L.milliGAT_pumping('L', 0, 5000, lbl_45)
	valve_2.valve_go(0, 12, lbl_46) 
	valve_1.valve_go(20, 13, lbl_47) # DCM wash
	valve_1.valve_go(20, 9, lbl_48) # 9: Burgess
	valve_2.valve_go(0, 9, lbl_49)
	valve_1.valve_go(360, 13, lbl_50) # DCM wash
	valve_2.valve_go(0, 12, lbl_51)
	valve_1.valve_go(20, 16, lbl_52) # THF wash
	valve_1.valve_go(20, 10, lbl_53) # 10: cleavage
	valve_2.valve_go(0, 10, lbl_54)
	valve_1.valve_go(120, 16, lbl_55)
	milliGAT_L.milliGAT_stoping('L', 10, lbl_56)
	autoprog_abort()
#endcmd
#abort
def autoprog_abort():
	milliGAT_L.close('L')
	valve_1.close()
	valve_2.close()
#endabort
#label
lbl_0 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 1 goes to position 1', anchor = 'w', justify = tk.LEFT)
lbl_0.pack()
lbl_1 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 1', anchor = 'w', justify = tk.LEFT)
lbl_1.pack()
lbl_2 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT L starts pumping at 5 mL/min', anchor = 'w', justify = tk.LEFT)
lbl_2.pack()
lbl_3 = tk.Label(fr_cmdInt, width = 75, text = 'After 1080 min, Valve 2 goes to position 11', anchor = 'w', justify = tk.LEFT)
lbl_3.pack()
lbl_4 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 1 goes to position 11', anchor = 'w', justify = tk.LEFT)
lbl_4.pack()
lbl_5 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_5.pack()
lbl_6 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12,', anchor = 'w', justify = tk.LEFT)
lbl_6.pack()
lbl_7 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, Valve 1 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_7.pack()
lbl_8 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_8.pack()
lbl_9 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_9.pack()
lbl_10 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_10.pack()
lbl_11 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, Valve 1 goes to position 3', anchor = 'w', justify = tk.LEFT)
lbl_11.pack()
lbl_12 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 3', anchor = 'w', justify = tk.LEFT)
lbl_12.pack()
lbl_13 = tk.Label(fr_cmdInt, width = 75, text = 'After 120 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_13.pack()
lbl_14 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_14.pack()
lbl_15 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, Valve 1 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_15.pack()
lbl_16 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_16.pack()
lbl_17 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_17.pack()
lbl_18 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_18.pack()
lbl_19 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, Valve 1 goes to position 4', anchor = 'w', justify = tk.LEFT)
lbl_19.pack()
lbl_20 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 4', anchor = 'w', justify = tk.LEFT)
lbl_20.pack()
lbl_21 = tk.Label(fr_cmdInt, width = 75, text = 'After 360 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_21.pack()
lbl_22 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_22.pack()
lbl_23 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, Valve 1 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_23.pack()
lbl_24 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 2', anchor = 'w', justify = tk.LEFT)
lbl_24.pack()
lbl_25 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, Valve 1 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_25.pack()
lbl_26 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_26.pack()
lbl_27 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, Valve 1 goes to position 5', anchor = 'w', justify = tk.LEFT)
lbl_27.pack()
lbl_28 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 5', anchor = 'w', justify = tk.LEFT)
lbl_28.pack()
lbl_29 = tk.Label(fr_cmdInt, width = 75, text = 'After 120 min, Valve 1 goes to position 14', anchor = 'w', justify = tk.LEFT)
lbl_29.pack()
lbl_30 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_30.pack()
lbl_31 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, Valve 1 goes to position 6', anchor = 'w', justify = tk.LEFT)
lbl_31.pack()
lbl_32 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 6', anchor = 'w', justify = tk.LEFT)
lbl_32.pack()
lbl_33 = tk.Label(fr_cmdInt, width = 75, text = 'After 60 min, Valve 1 goes to position 11', anchor = 'w', justify = tk.LEFT)
lbl_33.pack()
lbl_34 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_34.pack()
lbl_35 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, Valve 1 goes to position 15', anchor = 'w', justify = tk.LEFT)
lbl_35.pack()
lbl_36 = tk.Label(fr_cmdInt, width = 75, text = 'After 10 min, Valve 1 goes to position 16', anchor = 'w', justify = tk.LEFT)
lbl_36.pack()
lbl_37 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, Valve 1 goes to position 7', anchor = 'w', justify = tk.LEFT)
lbl_37.pack()
lbl_38 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 7', anchor = 'w', justify = tk.LEFT)
lbl_38.pack()
lbl_39 = tk.Label(fr_cmdInt, width = 75, text = 'After 30 min, Valve 1 goes to position 16', anchor = 'w', justify = tk.LEFT)
lbl_39.pack()
lbl_40 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_40.pack()
lbl_41 = tk.Label(fr_cmdInt, width = 75, text = 'After 10 min, Valve 1 goes to position 8', anchor = 'w', justify = tk.LEFT)
lbl_41.pack()
lbl_42 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 8', anchor = 'w', justify = tk.LEFT)
lbl_42.pack()
lbl_43 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT A pumps at 2000 ul/min', anchor = 'w', justify = tk.LEFT)
lbl_43.pack()
lbl_44 = tk.Label(fr_cmdInt, width = 75, text = 'After 60 min, Valve 1 goes to position 11', anchor = 'w', justify = tk.LEFT)
lbl_44.pack()
lbl_45 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, MilliGAT A pumps at 5000 ul/min', anchor = 'w', justify = tk.LEFT)
lbl_45.pack()
lbl_46 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_46.pack()
lbl_47 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, Valve 1 goes to position 13', anchor = 'w', justify = tk.LEFT)
lbl_47.pack()
lbl_48 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, Valve 1 goes to position 9', anchor = 'w', justify = tk.LEFT)
lbl_48.pack()
lbl_49 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 9', anchor = 'w', justify = tk.LEFT)
lbl_49.pack()
lbl_50 = tk.Label(fr_cmdInt, width = 75, text = 'After 360 min, Valve 1 goes to position 13', anchor = 'w', justify = tk.LEFT)
lbl_50.pack()
lbl_51 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 12', anchor = 'w', justify = tk.LEFT)
lbl_51.pack()
lbl_52 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, Valve 1 goes to position 16', anchor = 'w', justify = tk.LEFT)
lbl_52.pack()
lbl_53 = tk.Label(fr_cmdInt, width = 75, text = 'After 20 min, Valve 1 goes to position 10', anchor = 'w', justify = tk.LEFT)
lbl_53.pack()
lbl_54 = tk.Label(fr_cmdInt, width = 75, text = 'After 0 min, Valve 2 goes to position 10', anchor = 'w', justify = tk.LEFT)
lbl_54.pack()
lbl_55 = tk.Label(fr_cmdInt, width = 75, text = 'After 120 min, Valve 1 goes to position 16', anchor = 'w', justify = tk.LEFT)
lbl_55.pack()
lbl_56 = tk.Label(fr_cmdInt, width = 75, text = 'After 10 min, MilliGAT A stops', anchor = 'w', justify = tk.LEFT)
lbl_56.pack()
#endlabel

frame.btn_start['command']=lambda:threading.Thread(target=autoprog_start, name='StartThread').start()
frame.btn_abort['command']=lambda:threading.Thread(target=autoprog_abort, name='StartThread').start()
frame.btn_init['command']=lambda:threading.Thread(target=autoprog_init, name='StartThread').start()
frame.window.mainloop()
