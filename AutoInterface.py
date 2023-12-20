        #mainframe               

"""Define window framework"""
window = tk.Tk()
window.title("Automation Program Execution")
window.geometry("1200x700+150+80")
window.rowconfigure(0,  weight=1)
window.columnconfigure(1, weight=1)
window.resizable(0,0)


"""Define Command Panel"""

fr_cmdPan = tk.Frame(window, width=600, height=700, relief=tk.FLAT, bd=2)
fr_cmdPan.grid_propagate(0)
fr_cmdPan.grid(row=0, column=2, padx=3,pady=3)
fr_cmdPan.rowconfigure(2, weight=1)

tk.Label(fr_cmdPan, text = "***** Welcome to Automation Programming  *****", height=1, font=("calibri",12,"bold"), relief=tk.FLAT).grid(row=0, column=0, padx=3, pady=3)


tk.Button(fr_cmdPan, text = "Start", width = 40, command = lambda:threading.Thread(target=autoprog_start, name='StartThread').start()).grid(row=2, column=0, padx=1, pady=1, sticky="w")
tk.Button(fr_cmdPan, text = "Abort", width = 40, fg = "red", command = lambda:threading.Thread(target=autoprog_abort, name='StartThread').start()).grid(row=2, column=0, padx=1, pady=1, sticky="e")

fr_canvas = tk.Frame(fr_cmdPan, width=585, height=600, relief=tk.GROOVE, bd=2)
fr_canvas.grid(row=1, column=0, padx=3, pady=3, sticky="wn")

canvas = tk.Canvas(fr_canvas,width=585, height=600, scrollregion=(0,0,100,2000), confine=False) 
canvas.pack()

fr_cmdInt = tk.Frame(canvas, width=585, height=590)


vbar = tk.Scrollbar(canvas, orient=tk.VERTICAL) 
vbar.place(x=568,width=20,height=590)
vbar.configure(command=canvas.yview)

canvas.config(yscrollcommand=vbar.set) 
canvas.create_window((280,20), window=fr_cmdInt) 

tk.Label(fr_cmdInt, width = 75, text = 'Successful example', bg="blue", anchor = 'w', justify = tk.LEFT).pack()
tk.Label(fr_cmdInt, width = 75, text = 'Failed example', bg="red", anchor = 'w', justify = tk.LEFT).pack()

    
"""Define Status Panel"""

fr_output = tk.Frame(window, width =550, height = 700,relief = tk.FLAT, bd =2)
fr_output.grid(row=0, column=1, padx=5,pady=5)
fr_output.grid_propagate(0)
fr_output.rowconfigure(4, weight=1)
fr_output.columnconfigure(0, weight=1)

tk.Label(fr_output, text = "Instruments Initialization", width=550, height=1, font=("calibri",12,"bold")).grid(row=0, column=0, padx=3, pady=3)

lbl_init = tk.Label(fr_output, anchor="w", width=550, height=10, justify=tk.LEFT, relief=tk.GROOVE)
lbl_init.grid(row=1, column=0, padx=3, pady=3)

tk.Button(fr_output, width=8,text = "Initialize", command = lambda:threading.Thread(target=autoprog_init, name='StartThread').start()).grid(row=2, column=0, padx=1, pady=1, sticky="ew")         

tk.Label(fr_output, text = "Instruments Status", width=550, height=1, font=("calibri",12,"bold")).grid(row=3, column=0, padx=3, pady=3)


""" Define Instrument Status Panel """

tab_instru_status = ttk.Notebook(fr_output, width=550, height=400)

tab_instru_status.grid(row=4, column=0, padx=3, pady=3)

ttk.Style().configure('TNotebook.Tab', width = 10, height = 2, anchor = "ew")


fr_asiapump_status =tk.Frame(tab_instru_status, width=550, height=400)
fr_vaptpump_status =tk.Frame(tab_instru_status, width=550, height=400)
fr_millipump_status =tk.Frame(tab_instru_status, width=550, height=400)
fr_valve_status = tk.Frame(tab_instru_status, width=550, height=400)
fr_stirplate_status = tk.Frame(tab_instru_status, width=550, height=400)
fr_oushisheng_status = tk.Frame(tab_instru_status, width=550, height=400)


tab_instru_status.add(fr_asiapump_status, text = "Asia Pump")
tab_instru_status.add(fr_vaptpump_status, text = "SF 10")
tab_instru_status.add(fr_millipump_status, text = "MilliGAT")
tab_instru_status.add(fr_valve_status, text = "Valve")
tab_instru_status.add(fr_stirplate_status, text = "Stir Plate")
tab_instru_status.add(fr_oushisheng_status, text = "Ou Shisheng")


#fr_asiapump_status

fr_asiapump_status.grid_propagate(0)

for i in range(0,2):

        for j in [0,1]:

            tk.Label(fr_asiapump_status, text = "Asia Pump %d"%(i+1+j*2), width=37, height=1).grid(row=i*2, column=j, padx=1, pady=1)

            globals()["lbl_asiapump_%d_sta"%(i+1+j*2)] = tk.Label(fr_asiapump_status, text = "Null", anchor="w", width=37, height=9, justify=tk.LEFT, relief=tk.GROOVE)

            globals()["lbl_asiapump_%d_sta"%(i+1+j*2)].grid(row=i*2+1, column=j, padx=1, pady=1)
        

#fr_vaptpump_status

fr_vaptpump_status.grid_propagate(0)

for i in range(0,2):

        for j in [0,1]:

            tk.Label(fr_vaptpump_status, text = "SF10 %d"%(i+1+j*2), width=37, height=1).grid(row=i*2, column=j, padx=1, pady=1)

            globals()["lbl_sf10_%d_sta"%(i+1+j*2)] = tk.Label(fr_vaptpump_status, text = "Null", anchor="w", width=37, height=9, justify=tk.LEFT, relief=tk.GROOVE)

            globals()["lbl_sf10_%d_sta"%(i+1+j*2)].grid(row=i*2+1, column=j, padx=1, pady=1)
        

#fr_millipump_status

fr_millipump_status.grid_propagate(0)

for i in range(0,2):

        for j in [0,1]:

            lbl_millipump_index = ["A","B","C","D","E","F","G","H"][i+j*2]

            tk.Label(fr_millipump_status, text = "MilliGAT %s"%lbl_millipump_index, width=37, height=1).grid(row=i*2, column=j, padx=1, pady=1)

            globals()["lbl_milliGAT_%s_sta"%lbl_millipump_index] = tk.Label(fr_millipump_status, text = "Null", anchor="w", width=37, height=9, justify=tk.LEFT, relief=tk.GROOVE)

            globals()["lbl_milliGAT_%s_sta"%lbl_millipump_index].grid(row=i*2+1, column=j, padx=1, pady=1)


#fr_valve_status

fr_valve_status.grid_propagate(0)

for i in range(0,5):

        for j in [0,1]:

            tk.Label(fr_valve_status, text = "Valve %d Position"%(i+1+j*5), width=37, height=1).grid(row=i*2, column=j, padx=1, pady=1)

            globals()["lbl_valve_%d_sta"%(i+1+j*5)] = tk.Label(fr_valve_status, text = "Null", anchor="w", width=20, height=2, justify=tk.LEFT, relief=tk.GROOVE)

            globals()["lbl_valve_%d_sta"%(i+1+j*5)].grid(row=i*2+1, column=j, padx=1, pady=1)

#fr_stirplate_status

fr_stirplate_status.grid_propagate(0)

for i in range(0,2):

        for j in [0,1]:

            tk.Label(fr_stirplate_status, text = "Heating Stir Plate %d"%(i+1+j*2), width=37, height=1).grid(row=i*2, column=j, padx=1, pady=1)

            globals()["lbl_heidolph_%d_sta"%(i+1+j*2)] = tk.Label(fr_stirplate_status, text = "Null", anchor="w", width=37, height=9, justify=tk.LEFT, relief=tk.GROOVE)

            globals()["lbl_heidolph_%d_sta"%(i+1+j*2)].grid(row=i*2+1, column=j, padx=1, pady=1)
        
#fr_valve_status

fr_oushisheng_status.grid_propagate(0)

for i in range(0,2):

        for j in [0,1]:

            tk.Label(fr_oushisheng_status, text = "Ou Shisheng %d"%(i+1+j*2), width=37, height=1).grid(row=i*2, column=j, padx=1, pady=1)

            globals()["lbl_oushisheng_%d_sta"%(i+1+j*2)] = tk.Label(fr_oushisheng_status, text = "Null", anchor="w", width=37, height=9, justify=tk.LEFT, relief=tk.GROOVE)

            globals()["lbl_oushisheng_%d_sta"%(i+1+j*2)].grid(row=i*2+1, column=j, padx=1, pady=1)
