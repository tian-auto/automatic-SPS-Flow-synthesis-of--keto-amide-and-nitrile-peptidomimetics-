import re
from turtle import bgcolor
import pyvisa
from ctypes import *
from threading import Timer
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import time
import tempfile
from tkinter import Y, ttk
import re

"""Define parameters"""

txt_output_import = ("from mttkinter import mtTkinter as tk\n" +
                     "from tkinter import ttk\n" +
                     "from interfaceFn import *\n" +                    
                     "from heidolphFn import *\n" +
                     "from milliGATFn import *\n" +
                     "from valveFn import *\n" +
                     "from sf10Fn import *\n" +
                     "from asiapumpFn import *\n" +
                     "from oushishengFn import *\n" +
                     "from watsonFn import *\n" +
                     "import time\n" +
                     "import threading\n" +
                     "frame = InterfaceFn()\n" +
                     "fr_cmdInt = frame.fr_cmdInt\n"
                     )

txt_output_parahead = "#parameter\n"
txt_output_para = []
txt_output_paraend = "#endparameter\n"

txt_output_inithead = "#init\ndef autoprog_init():\n"
txt_output_init = []
txt_output_initend = "#endinit\n"

txt_output_cmdhead = "#cmd\ndef autoprog_start():\n"
txt_output_cmd = []
txt_output_cmdend = "\tautoprog_abort()\n#endcmd\n"

txt_output_aborthead = "#abort\ndef autoprog_abort():\n"
txt_output_abort = []
txt_output_abortend = "#endabort\n"

txt_output_interfacehead = "#label\n"
txt_output_interface = []
txt_output_interfaceend = "#endlabel\n"

timeline_head = "#timeline\n"
timeline = []
timeline_end ="#endtimeline\n"

txt_output_end = ("frame.btn_start['command']=lambda:threading.Thread(target=autoprog_start, name='StartThread').start()\n" +
                "frame.btn_abort['command']=lambda:threading.Thread(target=autoprog_abort, name='StartThread').start()\n" +
                "frame.btn_init['command']=lambda:threading.Thread(target=autoprog_init, name='StartThread').start()\n" +
                "frame.window.mainloop()\n")

file_path = ""

 
"""Define page switch"""

def topWin(frame):

    fr_asiapump.grid_remove()
    fr_sf10.grid_remove()
    fr_milliGAT.grid_remove()
    fr_heidolph.grid_remove()
    fr_valve.grid_remove()
    fr_oushisheng.grid_remove()
    fr_watson.grid_remove()

    frame.grid()

"""Define file button """
def recall_cmd():
    
    global txt_output_para
    global txt_output_init
    global txt_output_abort
    global txt_output_cmd
    global txt_output_interface
    global timeline
    global fr_cmdInt

    if txt_output_cmd:
        if 'global' not in txt_output_cmd[-1]:# update command
            txt_output_cmd = txt_output_cmd[:-1]
            txt_output_interface = txt_output_interface[:-1]
            fr_cmdInt.delete(tk.END)
            timeline = timeline[:-1]

        else:
            txt_output_para = txt_output_para[:-1]
            txt_output_init = txt_output_init[:-1]
            txt_output_abort = txt_output_abort[:-1]
            txt_output_cmd = txt_output_cmd[:-1]
            fr_cmdInt.delete(tk.END)
            timeline = timeline[:-1]

    else:
        print("There is no command as of yet.")

def insert():
    
    global txt_output_cmd
    global txt_output_interface
    global fr_cmdInt

    fr_cmdInt.insert(fr_cmdInt.curselection()[0],fr_cmdInt.get(tk.END))
    fr_cmdInt.delete(tk.END)

    txt_output_cmd.insert(fr_cmdInt.curselection()[0],txt_output_cmd[-1])
    txt_output_cmd.pop()

    txt_output_interface.insert(fr_cmdInt.curselection()[0],txt_output_cmd[-1])
    txt_output_interface.pop()

def txtclear():
    
    global txt_output_para
    global txt_output_init
    global txt_output_cmd
    global txt_output_abort
    global txt_output_interface

    txt_output_para = []
    txt_output_init = []
    txt_output_cmd = []
    txt_output_abort = []
    txt_output_interface = []

    fr_cmdInt.delete(0,tk.END)

def fileread(txt1, txt2, txtoutput, txt):
   
    templength = len(txtoutput)
   
    switch = False
   
    for line in txt:


        if re.match(txt1, line) != None:

            switch = True

        if re.match(txt2, line) != None:

            switch = False

            break

        if switch == True:
       
            txtoutput.append(line)

    try:
        
        del txtoutput[templength]
        
    except:
        
        None
        
    return txtoutput

def fileread_cmd(txt1, txt2, txtoutput, txt):
   
    templength = len(txtoutput)
   
    switch = False
   
    for line in txt:


        if re.match(txt1, line) != None:

            switch = True

        if re.match(txt2, line) != None:

            switch = False

            break

        if switch == True:
           
            newtxt = line[0:-10]
            txtoutput.append(newtxt)

    try:
        
        del txtoutput[templength]
        
    except:
        
        None
        
    return txtoutput

def openfile():

    global txt_output_para
    global txt_output_init
    global txt_output_cmd
    global txt_output_abort
    global txt_output_interface
    global timeline

    filepath = askopenfilename(filetypes=[("Text Files", "*.py"), ("All Files", "*.*")])

    text = ""

    if not filepath:

        return
   
    with open(filepath, "r") as file:

        readtext = file.readlines()

    file.close()
       
    # for label in Autoprogram
    # for label in output file

    for line in readtext:
       
        if re.match ("lbl_", line) != None:

            text = text + line
           
    textsplit = text.split("text = '")

    for items in textsplit:
   
        if items.find("'") !=-1:
           
            num = items.find("'")

            fr_cmdInt.insert(tk.END, items[0:num])
            txt_output_interface.append(items[0:num])
   

    # for command in output file

    txt_output_para = fileread("#parameter", "#endparameter", txt_output_para, readtext)
    txt_output_init = fileread("def autoprog_init", "#endinit", txt_output_init, readtext)
    txt_output_cmd = fileread_cmd("def autoprog_start", "\tautoprog_abort", txt_output_cmd, readtext)
    txt_output_abort = fileread("def autoprog_abort", "#endabort", txt_output_abort, readtext)
    timeline = fileread("#timeline", "#endtimeline", timeline, readtext)

    for i in range(len(timeline)):
        timeline[i] = int(timeline[i])

def savefile():
   
    filepath = asksaveasfilename(defaultextension=".py", filetypes=[("Text Files", "*.py"), ("All Files", "*.*")])

    if not filepath:

        return
       
    with open(filepath, "w+") as file:

        file.seek(0)
        file.truncate()

        file.write(txt_output_import)
       
        file.write(txt_output_parahead)
        for para in txt_output_para:
            file.write(para)
        file.write(txt_output_paraend)

        file.write(txt_output_inithead)
        for init in txt_output_init:
            file.write(init)
        file.write(txt_output_initend)

        file.write(txt_output_cmdhead)

        cmd_str = ''.join(txt_output_cmd)
        total_init = cmd_str.count('global')

        for cmd in range(len(txt_output_cmd)):
            if 'global' in txt_output_cmd[cmd]:
                file.write(txt_output_cmd[cmd])
            else:
                file.write("%s lbl_%d)\n"%(txt_output_cmd[cmd], cmd - total_init)) # assumes all steps start with init, needs fixing
        file.write(txt_output_cmdend)

        file.write(txt_output_aborthead)
        for abt in txt_output_abort:
            file.write(abt)
        file.write(txt_output_abortend)

        file.write(txt_output_interfacehead)
        for interface in range(len(txt_output_interface)):
            file.write("lbl_%d = tk.Label(fr_cmdInt, width = 75, text = '%s', anchor = 'w', justify = tk.LEFT)\n" %(interface,txt_output_interface[interface]))
            file.write("lbl_%d.pack()\n"%interface)
        file.write(txt_output_interfaceend)

        file.write(timeline_head)
        for timepoint in timeline:
            file.write("%d\n"%timepoint)
        file.write(timeline_end)

        file.write(txt_output_end)

        file.close()

def gen_fig():

    global canvas
    global timeline
    global fr_cmdInt

    #canvas.create_line(300,400,300,450,fill="blue")
    #canvas.create_rectangle(200,200,400,400,fill="red")
    #canvas.create_text(300,450,text="text",fill="blue")

    txt_temp = ''
    pos_lbl = 100
    pos_time = 100

    for i in range(fr_cmdInt.size()):

        if timeline[i] == 0:
           
            txt_temp = txt_temp + "step %d\t" %i

        else:
           
            canvas.create_line(300, pos_lbl, 340, pos_lbl,fill="black")
            canvas.create_text(350, pos_lbl, text=txt_temp, fill="black", anchor = "w")
           
            pos_time = pos_lbl + timeline[i]*5
            canvas.create_line(260, pos_time, 300, pos_time,fill="black")
            canvas.create_text(250, pos_time, text="%dmin"%timeline[i],fill="black", anchor = "e")

            pos_lbl = pos_lbl + timeline[i]*10
            txt_temp = "step %d\t" %i

    canvas.create_line(300, pos_lbl, 340, pos_lbl,fill="black")
    canvas.create_text(350,pos_lbl, text=txt_temp, fill="black", anchor = "w")

    canvas.create_line(300, 100, 300, pos_lbl,fill="black")
    canvas.configure(scrollregion=(0,0,580,pos_lbl+500))

    fr_cmdInt_sum.delete(0,tk.END)
    for i in range(fr_cmdInt.size()):
       
        fr_cmdInt_sum.insert(tk.END, "step %d,  "%i + fr_cmdInt.get(i))

"""Define initialization button """

def instru_init(instru, num, COM):
   
    #sf10 valve heidolph milliGAT oushisheng watson asiapump
   
    #update the interface

    fr_cmdInt.insert(tk.END, "Initialize %s %s at %s" %(instru, num, COM))

    #write the command to file

    if instru == "asiapump":
        txt_output_para.append("%s_%s=%sFn()\n" %(instru,num,instru)+
                                "asiapump_%d.pumpNum = %d\n" %(num, num-1))
        txt_output_init.append("\tglobal %s_%s\n" %(instru, num) +
                               "\t%s_%s.lbl_%s_sta = lbl_%s_%s_sta\n" %(instru, num, instru, instru, num) +
                               "\t%s_%s.%s_init(frame.lbl_init)\n" %(instru, num, instru)
                               )
        
    elif instru == "oushisheng":
        txt_output_para.append("%s_%s=%sFn()\n" %(instru, num,instru)+
                                "oushisheng_%d.num=%d\n" %(num,num))

    elif instru == "milliGAT":
        txt_output_para.append("%s_%s=%sFn()\n" %(instru,num,instru))
        txt_output_init.append("\tglobal %s_%s\n" %(instru, num) +
                               "\t%s_%s.%s_init('%s', '%s', frame.lbl_init)\n" %(instru, num, instru, COM, num) +
                               "\t%s_%s.lbl_%s_sta = lbl_%s_%s_sta\n" %(instru, num, instru, instru, num)
                               )
        
    else:
        txt_output_para.append("%s_%s=%sFn()\n" %(instru,num,instru))
        txt_output_init.append("\tglobal %s_%s\n" %(instru, num) +
                               "\t%s_%s.%s_init('%s', %s, frame.lbl_init)\n" %(instru, num, instru, COM, num) +
                               "\t%s_%s.lbl_%s_sta = lbl_%s_%s_sta\n" %(instru, num, instru, instru, num)
                               )

    txt_output_cmd.append("\tglobal %s_%s\n" %(instru, num))

    if instru == "milliGAT":
        txt_output_abort.append("\t%s_%s.close('%s')\n" %(instru, num, num))
        
    else:
        txt_output_abort.append("\t%s_%s.close()\n" %(instru, num))
    
   
"""Define command button """

#for Aisa Pump

def asiapump_pumping(num, chan, timeEntry, rateEntry):  

    try:#check parameters
       
        time = int(timeEntry.get())
        rate = int(rateEntry.get())
        global lbl_index

        #update the interface

        fr_cmdInt.insert(tk.END, "After %d min, Asiapump %d channel %d pumps at %d ul/min" %(time, num, (chan+1), rate))
        fr_cmdInt.insert(tk.END, "After 0 min, Asiapump %d channel %d pumps at %d ul/min" %(num, (chan+1), rate))
        timeline.append(time)

        #write the interface to file

        txt_output_interface.append("After %d min, Asiapump %d channel %d pumps at %d ul/min"%(time, num, (chan+1), rate))
        txt_output_interface.append("After 0 min, Asiapump %d channel %d pumps at %d ul/min"%(num, (chan+1), rate))
   
        #write the command to file

        txt_output_cmd.append("\tasiapump_%d.asiapump_pumping(%d, %d, %d," %(num, chan, time, rate))
        txt_output_cmd.append("\tasiapump_%d.asiapump_pumping(%d, 0, %d," %(num, chan, rate))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")        

def asiapump_filling(num, chan, timeEntry, rateEntry):

    try:#check parameters
       
        time = int(timeEntry.get())
        rate = int(rateEntry.get())

        fr_cmdInt.insert(tk.END, "After %d min, Asiapump %d channel %d fills at %d ul/min" %(time, num, (chan+1), rate))
        fr_cmdInt.insert(tk.END, "After 0 min, Asiapump %d channel %d fills at %d ul/min" %(num, (chan+1), rate))
        timeline.append(time)

        txt_output_interface.append("After %d min, Asiapump %d channel %d fills at %d ul/min"%(time, num, (chan+1), rate))
        txt_output_interface.append("After 0 min, Asiapump %d channel %d fills at %d ul/min"%(num, (chan+1), rate))

        txt_output_cmd.append("\tasiapump_%d.asiapump_filling(%d, %d, %d,"%(num, chan, time, rate))
        txt_output_cmd.append("\tasiapump_%d.asiapump_filling(%d, 0, %d,"%(num, chan, rate))

    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")

def asiapump_emptying(num, chan, timeEntry, rateEntry):

    try:#check parameters
       
        time = int(timeEntry.get())
        rate = int(rateEntry.get())
       
        fr_cmdInt.insert(tk.END, "After %d min, Asiapump %d channel %d empties at %d ul/min" %(time, num, (chan+1), rate))
        fr_cmdInt.insert(tk.END, "After 0 min, Asiapump %d channel %d empties at %d ul/min" %(num, (chan+1), rate))
        timeline.append(time)

        txt_output_interface.append("After %d min, Asiapump %d channel %d empties at %d ul/min"%(time, num, (chan+1), rate))
        txt_output_interface.append("After 0 min, Asiapump %d channel %d empties at %d ul/min"%(num, (chan+1), rate))

        txt_output_cmd.append("\tasiapump_%d.asiapump_emptying(%d, %d, %d,"%(num, chan, time, rate))
        txt_output_cmd.append("\tasiapump_%d.asiapump_emptying(%d, 0, %d,"%(num, chan, rate))

    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")

def asiapump_stoping(num, chan, timeEntry):

    try:#check parameters
       
        time = int(timeEntry.get())

        fr_cmdInt.insert(tk.END, "After %d min, Asiapump %d channel %d stops" %(time, num, (chan+1)))
        fr_cmdInt.insert(tk.END, "After 0 min, Asiapump %d channel %d stops" %(num, (chan+1)))
        timeline.append(time)

        txt_output_interface.append("After %d min, Asiapump %d channel %d stops"%(time, num, (chan+1)))
        txt_output_interface.append("After 0 min, Asiapump %d channel %d stops"%(num, (chan+1)))

        txt_output_cmd.append("\tasiapump_%d.asiapump_stoping(%d, %d,"%(num, chan, time))
        txt_output_cmd.append("\tasiapump_%d.asiapump_stoping(%d, 0,"%(num, chan))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")

#for SF10
   
def sf10_pumping(num, chan, timeEntry, rateEntry): #Firstly, check the parametere. Secondly, write the command to file. Thirdly, update the interface.

    try:#check parameters
       
        time = int(timeEntry.get())
        rate = float(rateEntry.get())

        fr_cmdInt.insert(tk.END, "After %d min, SF10 %d valve %s pumps at %.1fml/min" %(time, num, chan, rate))
        timeline.append(time)

        txt_output_interface.append("After %d min, SF10 %d valve %s pumps at %.1fml/min"%(time, num, chan, rate))

        txt_output_cmd.append("\tsf10_%d.sf10_pumping('%s', %d, %.1f,"%(num, chan, time, rate))

    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")

def sf10_gaspumping(num, chan, timeEntry, rateEntry): #Firstly, check the parametere. Secondly, write the command to file. Thirdly, update the interface.

    try:#check parameters
       
        time = int(timeEntry.get())
        rate = int(rateEntry.get())
       
        fr_cmdInt.insert(tk.END, "After %d min, SF10 %d valve %s gaspumps at %.1fml/min" %(time, num, chan, rate))
        timeline.append(time)

        txt_output_interface.append("After %d min, SF10 %d valve %s gaspumps at %.1fml/min"%(time, num, chan, rate))

        txt_output_cmd.append("\tsf10_%d.sf10_gaspumping('%s', %d, %.1f,"%(num, chan, time, rate))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")      

def sf10_regpresing(num, chan, timeEntry, rateEntry): #Firstly, check the parametere. Secondly, write the command to file. Thirdly, update the interface.

    try:#check parameters
       
        time = int(timeEntry.get())
        rate = int(rateEntry.get())
       
        fr_cmdInt.insert(tk.END, "After %d min, SF10 %d valve %s sets gas regulator pressure at %1.f bar" %(time, num, chan, rate))
        timeline.append(time)

        txt_output_interface.append("After %d min, SF10 %d valve %s sets gas regulator pressure at %.1f bar"%(time, num, chan, rate))

        txt_output_cmd.append("\tsf10_%d.sf10_regpresing('%s', %d, %.1f,"%(num, chan, time, rate))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")
       
def sf10_setramping(num, chan, timeEntry, rateEntry_1, rateEntry_2, periodEntry): #Firstly, check the parametere. Secondly, write the command to file. Thirdly, update the interface.

    try:#check parameters
       
        time = int(timeEntry.get())
        rate_1 = float(rateEntry_1.get())
        rate_2 = float(rateEntry_2.get())
        period = float(periodEntry.get())

        fr_cmdInt.insert(tk.END, "After %d min, SF10 %d valve %s sets ramp speed from %.1f ml/min to %.1f ml/min over %.1f min" %(time, num, chan, rate_1, rate_2, period))
        timeline.append(time)

        txt_output_interface.append("After %d min, SF10 %d valve %s sets ramp speed from %.1f ml/min to %.1f ml/min over %.1f min"%(time, num, chan, rate_1, rate_2, period))

        txt_output_cmd.append("\tsf10_%d.sf10_setramping('%s', %d, %.1f, %.1f, %.1f,"%(num, chan, time, rate_1, rate_2, period))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")

def sf10_stoping(num, chan, timeEntry): #Firstly, check the parametere. Secondly, write the command to file. Thirdly, update the interface.

    try:#check parameters
       
        time = int(timeEntry.get())
        global lbl_index
       
        fr_cmdInt.insert(tk.END, "After %d min, SF10 %d valve %s stops" %(time, num, chan))
        timeline.append(time)

        txt_output_interface.append("After %d min, SF10 %d valve %s stops"%(time, num, chan))

        txt_output_cmd.append("\tsf10_%d.sf10_stoping('%s', %d,"%(num, chan, time))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")

# for MilliGAT

def milliGAT_pumping(num, timeEntry, rateEntry): #Firstly, check the parametere. Secondly, write the command to file. Thirdly, update the interface.

    try:#check parameters
       
        time = int(timeEntry.get())
        rate = int(rateEntry.get())
         
        fr_cmdInt.insert(tk.END, "After %d min, MilliGAT %s pumps at %d ul/min" %(time, num, rate))
        timeline.append(time)

        txt_output_interface.append("After %d min, MilliGAT %s pumps at %d ul/min"%(time, num, rate))

        txt_output_cmd.append("\tmilliGAT_%s.milliGAT_pumping('%s', %d, %d,"%(num, num, time, rate))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")

def milliGAT_volumning(num, timeEntry, volumnEntry, rateEntry): #Firstly, check the parametere. Secondly, write the command to file. Thirdly, update the interface.

    try:#check parameters
       
        time = int(timeEntry.get())
        rate = int(rateEntry.get())
        volumn = int(volumnEntry.get())

        fr_cmdInt.insert(tk.END, "After %d min, MilliGAT %s pumps %d ul at %d ul/min" %(time, num, volumn, rate))
        timeline.append(time)

        txt_output_interface.append("After %d min, MilliGAT %s pumps %d ul at %d ul/min"%(time, num, volumn, rate))

        txt_output_cmd.append("\tmilliGAT_%s.milliGAT_volumning('%s', %d, %d, %d,"%(num, num, time, volumn, rate))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")

def milliGAT_stoping(num, timeEntry): #Firstly, check the parametere. Secondly, write the command to file. Thirdly, update the interface.

    try:#check parameters
       
        time = int(timeEntry.get())
     
        fr_cmdInt.insert(tk.END, "After %d min, MilliGAT %s stops" %(time, num))
        timeline.append(time)

        txt_output_interface.append("After %d min, MilliGAT %s stops"%(time, num))

        txt_output_cmd.append("\tmilliGAT_%s.milliGAT_stoping('%s', %d,"%(num, num, time))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")
                             
#for Valve

def valve_going(num, timeEntry, position):

    try:#check parameters
       
        time = int(timeEntry.get())
        position = float(position.get())
       
        fr_cmdInt.insert(tk.END, "After %d min, Valve %d goes to position %d" %(time, num, position))
        timeline.append(time)

        txt_output_interface.append("After %d min, Valve %d goes to position %d"%(time, num, position))

        txt_output_cmd.append("\tvalve_%d.valve_go(%d, %d,"%(num, time, position))

    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")

#for Ou Shisheng

def oushisheng_pumping(num, timeEntry, rateEntry, pumptype):

    try:#check parameters
       
        time = int(timeEntry.get())

        if pumptype ==1:
            rate = int(rateEntry.get())
        else:
            rate = round(float(rateEntry.get())*10)

        fr_cmdInt.insert(tk.END, "After %d min, Ou Shisheng %d pumps at %d ul/min" %(time, num, rate))
        timeline.append(time)

        txt_output_interface.append("After %d min, Ou Shisheng %d pumps at %d ul/min"%(time, num, rate))

        txt_output_cmd.append("\toushisheng_%d.oushisheng_pumping(%d, %d,"%(num, time, rate))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")

def oushisheng_stoping(num, timeEntry):

    try:#check parameters
       
        time = int(timeEntry.get())

        fr_cmdInt.insert(tk.END, "After %d min, Ou Shisheng %d stops" %(time, num))
        timeline.append(time)

        txt_output_interface.append("'After %d min, Ou Shisheng %d stops"%(time, num))

        txt_output_cmd.append("\toushisheng_%d.oushisheng_stoping(%d,"%(num, time))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")

# for Heidolph

def heidolph_rotating(num, timeEntry, rateEntry): #Firstly, check the parametere. Secondly, write the command to file. Thirdly, update the interface.

    try:#check parameters
       
        time = float(timeEntry.get())
        rate = int(rateEntry.get())

        fr_cmdInt.insert(tk.END, "After %.2f min, Heidolph %d rotates at %d rpm" %(time, num, rate))
        timeline.append(time)

        txt_output_interface.append("After %.2f min, Heidolph %d rotates at %d rpm"%(time, num, rate))

        txt_output_cmd.append("\theidolph_%d.heidolph_rotating(%d, %f,"%(num, time, rate))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")

def heidolph_heating(num, timeEntry, rateEntry): #Firstly, check the parametere. Secondly, write the command to file. Thirdly, update the interface.

    try:#check parameters
       
        time = float(timeEntry.get())
        rate = int(rateEntry.get())
       
        fr_cmdInt.insert(tk.END, "After %.2f min, Heidolph %d heats to %d degree Celsius" %(time, num, rate))
        timeline.append(time)

        txt_output_interface.append("After %.2f min, Heidolph %d heats to %d degree Celsius"%(time, num, rate))

        txt_output_cmd.append("\theidolph_%d.heidolph_heating(%d, %f,"%(num, time, rate))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")

def heidolph_stop_rotating(num, timeEntry): #Firstly, check the parametere. Secondly, write the command to file. Thirdly, update the interface.

    try:#check parameters
       
        time = float(timeEntry.get())

        fr_cmdInt.insert(tk.END, "After %.2f min, Heidolph %d stops rotating" %(time, num))
        timeline.append(time)

        txt_output_interface.append("After %.2f min, Heidolph %d stops rotating"%(time, num))

        txt_output_cmd.append("\theidolph_%d.heidolph_stop_rotating(%d,"%(num, time))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")

def heidolph_stop_heating(num, timeEntry): #Firstly, check the parametere. Secondly, write the command to file. Thirdly, update the interface.

    try:#check parameters
       
        time = float(timeEntry.get())
       
        fr_cmdInt.insert(tk.END, "After %.2f min, Heidolph %d stops heating" %(time, num))
        timeline.append(time)

        txt_output_interface.append("After %.2f min, Heidolph %d stops heating"%(time, num))

        txt_output_cmd.append("\theidolph_%d.heidolph_stop_heating(%d,"%(num, time))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")

#for Watson Marlow
   
def watson_pumping(num, chan, timeEntry, rateEntry): #Firstly, check the parametere. Secondly, write the command to file. Thirdly, update the interface.

    try:#check parameters
       
        time = int(timeEntry.get())
        rate = float(rateEntry.get())

        fr_cmdInt.insert(tk.END, "After %d min, Watson Marlow %d direction %s pumps at %.1fRPM" %(time, num, chan, rate))
        timeline.append(time)

        txt_output_interface.append("After %d min, Watson Marlow %d direction %s pumps at %.1f RPM"%(time, num, chan, rate))

        txt_output_cmd.append("\twatson_%d.watson_pumping('%s', %d, %.1f,"%(num, chan, time, rate))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")

def watson_dosing(num, chan, timeEntry, rateEntry): #Firstly, check the parametere. Secondly, write the command to file. Thirdly, update the interface.

    try:#check parameters
       
        time = int(timeEntry.get())
        rate = int(rateEntry.get())

        fr_cmdInt.insert(tk.END, "After %d min, Watson Marlow %d direction %s doses %.1f tacho" %(time, num, chan, rate))
        timeline.append(time)

        txt_output_interface.append("After %d min, Watson Marlow %d direction %s doses %.1f tacho"%(time, num, chan, rate))

        txt_output_cmd.append("\twatson_%d.watson_dosing('%s', %d, %.1f,"%(num, chan, time, rate))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")      

def watson_stoping(num, chan, timeEntry): #Firstly, check the parametere. Secondly, write the command to file. Thirdly, update the interface.

    try:#check parameters
       
        time = int(timeEntry.get())

        fr_cmdInt.insert(tk.END, "After %d min, Watson Marlow %d direction %s stops" %(time, num, chan))
        timeline.append(time)

        txt_output_interface.append("After %d min, Watson Marlow %d direction %s stops"%(time, num, chan))

        txt_output_cmd.append("\twatson_%d.watson_stoping('%s', %d,"%(num, chan, time))
       
    except:
       
        tk.messagebox.showinfo("Warning", "An unexpected error occured!!\n")
       
 
"""Define window framework"""

window = tk.Tk()
window.title("Automation Program")
window.geometry("1250x700+150+80")
window.rowconfigure(0,  weight=1)
window.columnconfigure(2, weight=1)
window.resizable(0,0)


"""Define Command Panel"""

fr_cmdPan = tk.Frame(window, width=700, height=700, relief=tk.FLAT, bd=2)
fr_cmdPan.grid_propagate(0)
fr_cmdPan.grid(row=0, column=2, padx=3,pady=3)
fr_cmdPan.rowconfigure(4, minsize=10, weight=1)

tk.Label(fr_cmdPan, text = "\n***** Welcome to Automation Programming  *****\n", font=("calibri",12,"bold"),relief=tk.FLAT).grid(row=0, column=0, padx=3, pady=3)

#Command menu

tab_output = ttk.Notebook(fr_cmdPan, width=600, height=500)
tab_output.grid(row=2, column=0, padx=3, pady=3)

ttk.Style().configure('TNotebook.Tab', width = 20, height = 22, anchor = "ew")

#Command_cmd panel

fr_cmdInt_scroll = tk.Frame(tab_output, relief=tk.FLAT, bd=2)
fr_cmdInt_scroll.pack()

scrollbar_cmd = tk.Scrollbar(fr_cmdInt_scroll)
scrollbar_cmd.pack(side=tk.RIGHT, fill=tk.Y)

fr_cmdInt = tk.Listbox(fr_cmdInt_scroll, width=85, height=30, selectmode= tk.SINGLE, yscrollcommand = scrollbar_cmd.set )
fr_cmdInt.pack(side =tk.LEFT, fill=tk.BOTH)

scrollbar_cmd.configure(command = fr_cmdInt.yview)

tab_output.add(fr_cmdInt_scroll, text = "Commands")

#Canvas panel

fr_canvas = tk.Frame(tab_output,width=85, height=30, relief=tk.GROOVE, bd=2)
fr_canvas.pack()

xbar = tk.Scrollbar(fr_canvas, orient=tk.HORIZONTAL)
xbar.pack(side=tk.BOTTOM, fill=tk.X)
vbar = tk.Scrollbar(fr_canvas, orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas = tk.Canvas(fr_canvas,width=575, height=560, scrollregion=(0,0,580,2000000), confine=False, xscrollcommand=xbar.set, yscrollcommand=vbar.set,bg="white")

canvas.pack()

xbar.configure(command=canvas.xview)
vbar.configure(command=canvas.yview)

tab_output.add(fr_canvas, text = "Figure")

#Command_summary panel

fr_cmdInt_sum_scroll = tk.Frame(tab_output, relief=tk.FLAT, bd=2)
fr_cmdInt_sum_scroll.pack()

scrollbar_sum = tk.Scrollbar(fr_cmdInt_sum_scroll)
scrollbar_sum.pack(side=tk.RIGHT, fill=tk.Y)

fr_cmdInt_sum = tk.Listbox(fr_cmdInt_sum_scroll, width=85, height=30, selectmode= tk.SINGLE, yscrollcommand = scrollbar_cmd.set )
fr_cmdInt_sum.pack(side =tk.LEFT, fill=tk.BOTH)

scrollbar_sum.configure(command = fr_cmdInt_sum.yview)

tab_output.add(fr_cmdInt_sum_scroll, text = "Summary")

#Define Button Area

fr_cmdBtn = tk.Frame(fr_cmdPan, relief=tk.GROOVE, bd=2)
fr_cmdBtn.grid(row=3, column=0, padx=1, pady=1)

fr_cmdBtn.columnconfigure(8, weight =9)

btn_open = tk.Button(fr_cmdBtn, width=8, text = "Open", command = openfile)
btn_open.grid(row=0, column=1, padx=1, pady=1)

btn_clear = tk.Button(fr_cmdBtn, width=8,text = "Clear", command = txtclear)
btn_clear.grid(row=0, column=2, padx=1, pady=1)

btn_open = tk.Button(fr_cmdBtn, width=8, text = "Recall", command = recall_cmd)
btn_open.grid(row=0, column=3, padx=1, pady=1)

btn_open = tk.Button(fr_cmdBtn, width=8, text = "Insert", command = insert)
btn_open.grid(row=0, column=4, padx=1, pady=1)

btn_fig = tk.Button(fr_cmdBtn, width=8, text = "Figure", command = gen_fig)
btn_fig.grid(row=0, column=5, padx=1, pady=1)

btn_save = tk.Button(fr_cmdBtn, width=8, text = "Save", command = savefile)
btn_save.grid(row=0, column=6, padx=1, pady=1)


""" Command Editor """

#Asia Pump Panel

fr_asiapump = tk.Frame(window, width =450, height = 700,relief = tk.FLAT, bd =2)
fr_asiapump.grid(row=0, column=1, padx=5,pady=5)
fr_asiapump.grid_propagate(0)
fr_asiapump.rowconfigure(4, weight=1)
fr_asiapump.columnconfigure(0, weight=1)

com_value = []
for i in range (1,31):
    com_value.append("COM%d"%i)
   
#Asia Pump Initialization
    
tk.Label(fr_asiapump, text = "Asia Pump Initialization Command Editor", width=50, height=2, font=("calibri",12,"bold")).grid(row=0, column=0, padx=3, pady=3)

fr_asiapump_init = tk.Frame(fr_asiapump, width=65, height = 185, relief=tk.GROOVE, bd=2)
fr_asiapump_init.grid(row=1, column=0, padx=3, pady=3, sticky="nsew")

for i in range(0,3):

    for j in [0,3]:

        tk.Label(fr_asiapump_init, text = "Asia Pump %d"%(i+1+j), width=10, height=2).grid(row=i, column=j, padx=3, pady=3)    

        globals()["com_asiapump_%d_init"%(i+1+j)] = ttk.Combobox(fr_asiapump_init, width=8, value = com_value)
       
        globals()["com_asiapump_%d_init"%(i+1+j)].grid(row=i, column=j+1, padx=3, pady=3)
       
tk.Button(fr_asiapump_init, text = "Add", width=5, height=1, command = lambda:instru_init("asiapump",1,com_asiapump_1_init.get())).grid(row=0, column=2, padx=3, pady=3)
tk.Button(fr_asiapump_init, text = "Add", width=5, height=1, command = lambda:instru_init("asiapump",2,com_asiapump_2_init.get())).grid(row=1, column=2, padx=3, pady=3)
tk.Button(fr_asiapump_init, text = "Add", width=5, height=1, command = lambda:instru_init("asiapump",3,com_asiapump_3_init.get())).grid(row=2, column=2, padx=3, pady=3)
tk.Button(fr_asiapump_init, text = "Add", width=5, height=1, command = lambda:instru_init("asiapump",4,com_asiapump_4_init.get())).grid(row=0, column=5, padx=3, pady=3)
tk.Button(fr_asiapump_init, text = "Add", width=5, height=1, command = lambda:instru_init("asiapump",5,com_asiapump_5_init.get())).grid(row=1, column=5, padx=3, pady=3)
tk.Button(fr_asiapump_init, text = "Add", width=5, height=1, command = lambda:instru_init("asiapump",6,com_asiapump_6_init.get())).grid(row=2, column=5, padx=3, pady=3)


#Asia Pump Number

fr_asiapump_num = tk.Frame(fr_asiapump, width=65, height = 100, relief=tk.FLAT, bd=2)
fr_asiapump_num.grid(row=2, column=0, padx=3, pady=3, sticky="nsew")

tk.Label(fr_asiapump_num, text = "\tCommand Editor for Asia Pump ", width=40, height=2, font=("calibri",12,"bold")).grid(row=0, column=0, padx=3, pady=3)

com_asiapump = []
for i in range (1,7):
    com_asiapump.append(i)

com_asiapump_num = ttk.Combobox(fr_asiapump_num, width=4, height=6, font=("calibri",12,"bold"), value = com_asiapump)
com_asiapump_num.grid(row=0, column=1, padx=3, pady=3)

#Asia Pump Function

fr_asiapump_fn = tk.Frame(fr_asiapump, width=65, height = 375, relief=tk.GROOVE, bd=2)
fr_asiapump_fn.grid(row=3, column=0, padx=3, pady=3, sticky="nsew")
fr_asiapump_fn.rowconfigure(5, minsize=10, weight=1)
fr_asiapump_fn.columnconfigure(6, minsize=10, weight=1)
fr_asiapump_fn.grid_propagate(0)

tk.Label(fr_asiapump_fn, text = "Channel 1", width=10, height=1).grid(row=0, column=1, padx=3,pady=3)
tk.Label(fr_asiapump_fn, text = "Channel 2", width=10, height=1).grid(row=0, column=4, padx=3,pady=3)

tk.Label(fr_asiapump_fn, text = "After", width=8, height=2).grid(row=1, column=0, padx=3,pady=3)
tk.Label(fr_asiapump_fn, text = "Pump", width=8, height=2).grid(row=2, column=0, padx=3,pady=3)
tk.Label(fr_asiapump_fn, text = "Fill", width=8, height=2).grid(row=3, column=0, padx=3,pady=3)
tk.Label(fr_asiapump_fn, text = "Empty", width=8, height=2).grid(row=4, column=0, padx=3,pady=3)
tk.Label(fr_asiapump_fn, text = "Stop", width=8, height=2).grid(row=5, column=0, padx=3,pady=3)
 

for i in range(1,5):

    for j in [1,4]: # for entry

        globals()["ent_" + str(i) + str(j)] = tk.StringVar()
        globals()["ent_" + str(i) + str(j)].set(0)
       
        tk.Entry(fr_asiapump_fn, textvariable = globals()["ent_" + str(i) + str(j)], width=10).grid(row=i, column=j, padx=3, pady=3)

    for j in [2,5]: # for label

        if i == 1:

            tk.Label(fr_asiapump_fn, text = "min", width=5, height=2).grid(row=i, column=j, padx=3, pady=3)

        if i in range (2,5):

            tk.Label(fr_asiapump_fn, text = "ul/min", width=5, height=2).grid(row=i, column=j, padx=3, pady=3)

#for button

tk.Button(fr_asiapump_fn, text = "Add", width=5, height=1, command = lambda:asiapump_pumping(int(com_asiapump_num.get()), 0, ent_11, ent_21)).grid(row=2, column=3, padx=3, pady=3)
tk.Button(fr_asiapump_fn, text = "Add", width=5, height=1, command = lambda:asiapump_filling(int(com_asiapump_num.get()), 0, ent_11, ent_31)).grid(row=3, column=3, padx=3, pady=3)
tk.Button(fr_asiapump_fn, text = "Add", width=5, height=1, command = lambda:asiapump_emptying(int(com_asiapump_num.get()), 0, ent_11, ent_41)).grid(row=4, column=3, padx=3, pady=3)
tk.Button(fr_asiapump_fn, text = "Add", width=5, height=1, command = lambda:asiapump_stoping(int(com_asiapump_num.get()), 0,ent_11)).grid(row=5, column=3, padx=3, pady=3)

tk.Button(fr_asiapump_fn, text = "Add", width=5, height=1, command = lambda:asiapump_pumping(int(com_asiapump_num.get()), 1, ent_14, ent_24)).grid(row=2, column=6, padx=3, pady=3)
tk.Button(fr_asiapump_fn, text = "Add", width=5, height=1, command = lambda:asiapump_filling(int(com_asiapump_num.get()), 1, ent_14, ent_34)).grid(row=3, column=6, padx=3, pady=3)
tk.Button(fr_asiapump_fn, text = "Add", width=5, height=1, command = lambda:asiapump_emptying(int(com_asiapump_num.get()), 1, ent_14, ent_44)).grid(row=4, column=6, padx=3, pady=3)
tk.Button(fr_asiapump_fn, text = "Add", width=5, height=1, command = lambda:asiapump_stoping(int(com_asiapump_num.get()), 1, ent_14)).grid(row=5, column=6, padx=3, pady=3)


#SF10 Panel

fr_sf10 = tk.Frame(window, width =450, height = 700,relief = tk.FLAT, bd =2)
fr_sf10.grid(row=0, column=1, padx=5,pady=5)
fr_sf10.grid_propagate(0)
fr_sf10.rowconfigure(4, weight=1)
fr_sf10.columnconfigure(0, weight=1)
   

#SF10 Initialization

tk.Label(fr_sf10, text = "SF10 Initialization Command Editor", width=50, height=2, font=("calibri",12,"bold")).grid(row=0, column=0, padx=3, pady=3)

fr_sf10_init = tk.Frame(fr_sf10, width=65, height = 185, relief=tk.GROOVE, bd=2)
fr_sf10_init.grid(row=1, column=0, padx=3, pady=3, sticky="nsew")

for i in range(0,3):

    for j in [0,3]:

        tk.Label(fr_sf10_init, text = "SF10 %d"%(i+1+j), width=10, height=2).grid(row=i, column=j, padx=3, pady=3)    

        globals()["com_sf10_%d_init"%(i+1+j)] = ttk.Combobox(fr_sf10_init, width=8, value = com_value)
       
        globals()["com_sf10_%d_init"%(i+1+j)].grid(row=i, column=j+1, padx=3, pady=3)
       
        tk.Button(fr_sf10_init, text = "Add", width=5, height=1, command = lambda:asiapump_init((i+1+j),globals()["com_sf10_%d_init"%(i+1+j)].get())).grid(row=i, column=j+2, padx=3, pady=3)

tk.Button(fr_sf10_init, text = "Add", width=5, height=1, command = lambda:instru_init("sf10",1,com_sf10_1_init.get())).grid(row=0, column=2, padx=3, pady=3)
tk.Button(fr_sf10_init, text = "Add", width=5, height=1, command = lambda:instru_init("sf10",2,com_sf10_2_init.get())).grid(row=1, column=2, padx=3, pady=3)
tk.Button(fr_sf10_init, text = "Add", width=5, height=1, command = lambda:instru_init("sf10",3,com_sf10_3_init.get())).grid(row=2, column=2, padx=3, pady=3)
tk.Button(fr_sf10_init, text = "Add", width=5, height=1, command = lambda:instru_init("sf10",4,com_sf10_4_init.get())).grid(row=0, column=5, padx=3, pady=3)
tk.Button(fr_sf10_init, text = "Add", width=5, height=1, command = lambda:instru_init("sf10",5,com_sf10_5_init.get())).grid(row=1, column=5, padx=3, pady=3)
tk.Button(fr_sf10_init, text = "Add", width=5, height=1, command = lambda:instru_init("sf10",6,com_sf10_6_init.get())).grid(row=2, column=5, padx=3, pady=3)

#SF10 number
       
fr_sf10_num = tk.Frame(fr_sf10, width=65, height = 100, relief=tk.FLAT, bd=2)
fr_sf10_num.grid(row=2, column=0, padx=3, pady=3, sticky="nsew")

tk.Label(fr_sf10_num, text = "\tCommand Editor for SF10 ", width=40, height=2, font=("calibri",12,"bold")).grid(row=0, column=0, padx=3, pady=3)

com_sf10 = []
for i in range (1,7):
    com_sf10.append(i)

com_sf10_num = ttk.Combobox(fr_sf10_num, width=4, height=6, font=("calibri",12,"bold"), value = com_sf10)
com_sf10_num.grid(row=0, column=1, padx=3, pady=3)

#SF10 Function
       
fr_sf10_fn = tk.Frame(fr_sf10, width=65, height = 380, relief=tk.GROOVE, bd=2)
fr_sf10_fn.grid(row=3, column=0, padx=3, pady=3, sticky="nsew")
fr_sf10_fn.rowconfigure(8, minsize=10, weight=1)
fr_sf10_fn.columnconfigure(7, minsize=10, weight=1)
fr_sf10_fn.grid_propagate(0)

tk.Label(fr_sf10_fn, text = "Valve A", width=10, height=1).grid(row=0, column=1)
tk.Label(fr_sf10_fn, text = "Valve B", width=10, height=1).grid(row=0, column=4)

tk.Label(fr_sf10_fn, text = "After", width=8, height=2).grid(row=1, column=0, padx=3,pady=3)
tk.Label(fr_sf10_fn, text = "Flowrate", width=8, height=2).grid(row=2, column=0, padx=3,pady=3)
tk.Label(fr_sf10_fn, text = "Gas\nRlowrate", width=8, height=2).grid(row=3, column=0, padx=3,pady=3)
tk.Label(fr_sf10_fn, text = "Reg\nPressure", width=8, height=2).grid(row=4, column=0, padx=3,pady=3)
tk.Label(fr_sf10_fn, text = "Set Ramp", width=8, height=2).grid(row=5, column=0, padx=3,pady=3)
tk.Label(fr_sf10_fn, text = "Stop", width=8, height=2).grid(row=8, column=0, padx=3,pady=3)
 
for i in range(1,8):

    for j in [1,4]: # for entry

        globals()["ent_sf10_" + str(i) + str(j)] = tk.StringVar()
        globals()["ent_sf10_" + str(i) + str(j)].set(0)
       
        tk.Entry(fr_sf10_fn, textvariable = globals()["ent_sf10_" + str(i) + str(j)], width=10).grid(row=i, column=j, padx=3, pady=3)


for i in [2,5]: # for label

    tk.Label(fr_sf10_fn, text = "min", width=5, height=2).grid(row=1, column=i, padx=3, pady=3)
    tk.Label(fr_sf10_fn, text = "ml/min", width=5, height=2).grid(row=2, column=i, padx=3, pady=3)
    tk.Label(fr_sf10_fn, text = "ssc/min", width=5, height=2).grid(row=3, column=i, padx=3, pady=3)
    tk.Label(fr_sf10_fn, text = "bar", width=5, height=2).grid(row=4, column=i, padx=3, pady=3)
    tk.Label(fr_sf10_fn, text = "ml/min", width=5, height=2).grid(row=5, column=i, padx=3, pady=3)
    tk.Label(fr_sf10_fn, text = "ml/min", width=5, height=2).grid(row=6, column=i, padx=3, pady=3)
    tk.Label(fr_sf10_fn, text = "min", width=5, height=2).grid(row=7, column=i, padx=3, pady=3)

    # for button

tk.Button(fr_sf10_fn, text = "Add", width=5, height=1, command = lambda:sf10_pumping(int(com_sf10_num.get()), "A", ent_sf10_11, ent_sf10_21)).grid(row=2, column=3, padx=3, pady=3)
tk.Button(fr_sf10_fn, text = "Add", width=5, height=1, command = lambda:sf10_gaspumping(int(com_sf10_num.get()), "A", ent_sf10_11, ent_sf10_31)).grid(row=3, column=3, padx=3, pady=3)
tk.Button(fr_sf10_fn, text = "Add", width=5, height=1, command = lambda:sf10_regpresing(int(com_sf10_num.get()), "A", ent_sf10_11, ent_sf10_41)).grid(row=4, column=3, padx=3, pady=3)
tk.Button(fr_sf10_fn, text = "Add", width=5, height=1, command = lambda:sf10_setramping(int(com_sf10_num.get()), "A", ent_sf10_11, ent_sf10_51, ent_sf10_61, ent_sf10_71)).grid(row=7, column=3, padx=3, pady=3)
tk.Button(fr_sf10_fn, text = "Add", width=5, height=1, command = lambda:sf10_stoping(int(com_sf10_num.get()), "A", ent_sf10_11)).grid(row=8, column=3, padx=3, pady=3)

tk.Button(fr_sf10_fn, text = "Add", width=5, height=1, command = lambda:sf10_pumping(int(com_sf10_num.get()), "B", ent_sf10_14, ent_sf10_24)).grid(row=2, column=6, padx=3, pady=3)
tk.Button(fr_sf10_fn, text = "Add", width=5, height=1, command = lambda:sf10_gaspumping(int(com_sf10_num.get()), "B", ent_sf10_14, ent_sf10_34)).grid(row=3, column=6, padx=3, pady=3)
tk.Button(fr_sf10_fn, text = "Add", width=5, height=1, command = lambda:sf10_regpresing(int(com_sf10_num.get()), "B", ent_sf10_14, ent_sf10_44)).grid(row=4, column=6, padx=3, pady=3)
tk.Button(fr_sf10_fn, text = "Add", width=5, height=1, command = lambda:sf10_setramping(int(com_sf10_num.get()), "B", ent_sf10_14, ent_sf10_54, ent_sf10_64, ent_sf10_74)).grid(row=7, column=6, padx=3, pady=3)
tk.Button(fr_sf10_fn, text = "Add", width=5, height=1, command = lambda:sf10_stoping(int(com_sf10_num.get()), "B", ent_sf10_14)).grid(row=8, column=6, padx=3, pady=3)



#MilliGAT Panel

fr_milliGAT = tk.Frame(window, width =450, height = 700,relief = tk.FLAT, bd =2)
fr_milliGAT.grid(row=0, column=1, padx=5,pady=5)
fr_milliGAT.grid_propagate(0)
fr_milliGAT.rowconfigure(4, weight=1)
fr_milliGAT.columnconfigure(0, weight=1)

   
#MilliGAT Initialization

tk.Label(fr_milliGAT, text = "MilliGAT Initialization Command Editor", width=50, height=2, font=("calibri",12,"bold")).grid(row=0, column=0, padx=3, pady=3)

fr_milliGAT_init = tk.Frame(fr_milliGAT, width=65, height = 185, relief=tk.GROOVE, bd=2)
fr_milliGAT_init.grid(row=1, column=0, padx=3, pady=3, sticky="nsew")

for i in range(0,3):

    for j in [0,3]:

        tk.Label(fr_milliGAT_init, text = "MilliGAT %s"%["A","B","C","D","E","F"][(i+j)], width=10, height=2).grid(row=i, column=j, padx=3, pady=3)    

        globals()["com_milliGAT_%d_init"%(i+1+j)] = ttk.Combobox(fr_milliGAT_init, width=8, value = com_value)
       
        globals()["com_milliGAT_%d_init"%(i+1+j)].grid(row=i, column=j+1, padx=3, pady=3)
       
tk.Button(fr_milliGAT_init, text = "Add", width=5, height=1, command = lambda:instru_init("milliGAT","A",com_milliGAT_1_init.get())).grid(row=0, column=2, padx=3, pady=3)
tk.Button(fr_milliGAT_init, text = "Add", width=5, height=1, command = lambda:instru_init("milliGAT","B",com_milliGAT_2_init.get())).grid(row=1, column=2, padx=3, pady=3)
tk.Button(fr_milliGAT_init, text = "Add", width=5, height=1, command = lambda:instru_init("milliGAT","C",com_milliGAT_3_init.get())).grid(row=2, column=2, padx=3, pady=3)
tk.Button(fr_milliGAT_init, text = "Add", width=5, height=1, command = lambda:instru_init("milliGAT","D",com_milliGAT_4_init.get())).grid(row=0, column=5, padx=3, pady=3)
tk.Button(fr_milliGAT_init, text = "Add", width=5, height=1, command = lambda:instru_init("milliGAT","E",com_milliGAT_5_init.get())).grid(row=1, column=5, padx=3, pady=3)
tk.Button(fr_milliGAT_init, text = "Add", width=5, height=1, command = lambda:instru_init("milliGAT","F",com_milliGAT_6_init.get())).grid(row=2, column=5, padx=3, pady=3)

#MilliGAT Number

fr_milliGAT_num = tk.Frame(fr_milliGAT, width=65, height = 100, relief=tk.FLAT, bd=2)
fr_milliGAT_num.grid(row=2, column=0, padx=3, pady=3, sticky="nsew")

tk.Label(fr_milliGAT_num, text = "\tCommand Editor for MilliGAT ", width=40, height=2, font=("calibri",12,"bold")).grid(row=0, column=0, padx=3, pady=3)

com_milliGAT = ["A","B","C","D","E","F","G","H"]

com_milliGAT_num = ttk.Combobox(fr_milliGAT_num, width=4, height=6, font=("calibri",12,"bold"), value = com_milliGAT)
com_milliGAT_num.grid(row=0, column=1, padx=3, pady=3)


#MilliGAT Function

fr_milliGAT_fn = tk.Frame(fr_milliGAT, width=65, height = 375, relief=tk.GROOVE, bd=2)
fr_milliGAT_fn.grid(row=3, column=0, padx=3, pady=3, sticky="nsew")
fr_milliGAT_fn.rowconfigure(5, minsize=10, weight=1)
fr_milliGAT_fn.columnconfigure(6, minsize=10, weight=1)
fr_milliGAT_fn.grid_propagate(0)


tk.Label(fr_milliGAT_fn, text = "After", width=20, height=2).grid(row=0, column=0, padx=3,pady=3)
tk.Label(fr_milliGAT_fn, text = "Flow Mode", width=20, height=2).grid(row=1, column=0, padx=3,pady=3)
tk.Label(fr_milliGAT_fn, text = "Volumn Mode", width=20, height=2).grid(row=2, column=0, padx=3,pady=3)
tk.Label(fr_milliGAT_fn, text = "Stop", width=20, height=2).grid(row=4, column=0, padx=3,pady=3)

ent_milliGAT_11 = tk.Entry(fr_milliGAT_fn, width=10)
ent_milliGAT_11.grid(row=0, column=1, padx=3, pady=3)

ent_milliGAT_21 = tk.Entry(fr_milliGAT_fn, width=10)
ent_milliGAT_21.grid(row=1, column=1, padx=3, pady=3)

ent_milliGAT_31 = tk.Entry(fr_milliGAT_fn, width=10)
ent_milliGAT_31.grid(row=2, column=1, padx=3, pady=3)

ent_milliGAT_41 = tk.Entry(fr_milliGAT_fn, width=10)
ent_milliGAT_41.grid(row=3, column=1, padx=3, pady=3)

tk.Label(fr_milliGAT_fn, text = "min", width=10, height=2).grid(row=0, column=2, padx=3,pady=3)
tk.Label(fr_milliGAT_fn, text = "ul/min", width=10, height=2).grid(row=1, column=2, padx=3,pady=3)
tk.Label(fr_milliGAT_fn, text = "ul", width=10, height=2).grid(row=2, column=2, padx=3,pady=3)
tk.Label(fr_milliGAT_fn, text = "ul/min", width=10, height=2).grid(row=3, column=2, padx=3,pady=3)

tk.Button(fr_milliGAT_fn, text = "Add", width=5, height=1, command = lambda:milliGAT_pumping(com_milliGAT_num.get(), ent_milliGAT_11, ent_milliGAT_21)).grid(row=1, column=3, padx=3, pady=3)
tk.Button(fr_milliGAT_fn, text = "Add", width=5, height=1, command = lambda:milliGAT_volumning(com_milliGAT_num.get(), ent_milliGAT_11, ent_milliGAT_31, ent_milliGAT_41)).grid(row=3, column=3, padx=3, pady=3)
tk.Button(fr_milliGAT_fn, text = "Add", width=5, height=1, command = lambda:milliGAT_stoping(com_milliGAT_num.get(), ent_milliGAT_11)).grid(row=4, column=3, padx=3, pady=3)


#Heidolph Panel

fr_heidolph = tk.Frame(window, width =450, height = 700,relief = tk.FLAT, bd =2)
fr_heidolph.grid(row=0, column=1, padx=5,pady=5)
fr_heidolph.grid_propagate(0)
fr_heidolph.rowconfigure(4, weight=1)
fr_heidolph.columnconfigure(0, weight=1)

#Heidolph Initialization

tk.Label(fr_heidolph, text = "Heidolph Initialization Command Editor", width=50, height=2, font=("calibri",12,"bold")).grid(row=0, column=0, padx=3, pady=3)

fr_heidolph_init = tk.Frame(fr_heidolph, width=65, height = 185, relief=tk.GROOVE, bd=2)
fr_heidolph_init.grid(row=1, column=0, padx=3, pady=3, sticky="nsew")

for i in range(0,3):

    for j in [0,3]:

        tk.Label(fr_heidolph_init, text = "Heidolph %d"%(i+1+j), width=10, height=2).grid(row=i, column=j, padx=3, pady=3)    

        globals()["com_heidolph_%d_init"%(i+1+j)] = ttk.Combobox(fr_heidolph_init, width=8, value = com_value)
       
        globals()["com_heidolph_%d_init"%(i+1+j)].grid(row=i, column=j+1, padx=3, pady=3)
       
tk.Button(fr_heidolph_init, text = "Add", width=5, height=1, command = lambda:instru_init("heidolph",1,com_heidolph_1_init.get())).grid(row=0, column=2, padx=3, pady=3)
tk.Button(fr_heidolph_init, text = "Add", width=5, height=1, command = lambda:instru_init("heidolph",2,com_heidolph_2_init.get())).grid(row=1, column=2, padx=3, pady=3)
tk.Button(fr_heidolph_init, text = "Add", width=5, height=1, command = lambda:instru_init("heidolph",3,com_heidolph_3_init.get())).grid(row=2, column=2, padx=3, pady=3)
tk.Button(fr_heidolph_init, text = "Add", width=5, height=1, command = lambda:instru_init("heidolph",4,com_heidolph_4_init.get())).grid(row=0, column=5, padx=3, pady=3)
tk.Button(fr_heidolph_init, text = "Add", width=5, height=1, command = lambda:instru_init("heidolph",5,com_heidolph_5_init.get())).grid(row=1, column=5, padx=3, pady=3)
tk.Button(fr_heidolph_init, text = "Add", width=5, height=1, command = lambda:instru_init("heidolph",6,com_heidolph_6_init.get())).grid(row=2, column=5, padx=3, pady=3)

#Heidolph Number

fr_heidolph_num = tk.Frame(fr_heidolph, width=65, height = 100, relief=tk.FLAT, bd=2)
fr_heidolph_num.grid(row=2, column=0, padx=3, pady=3, sticky="nsew")

tk.Label(fr_heidolph_num, text = "\tCommand Editor for Heidolph ", width=40, height=2, font=("calibri",12,"bold")).grid(row=0, column=0, padx=3, pady=3)

com_heidolph = []
for i in range (1,7):
    com_heidolph.append(i)

com_heidolph_num = ttk.Combobox(fr_heidolph_num, width=4, height=6, font=("calibri",12,"bold"), value = com_heidolph)
com_heidolph_num.grid(row=0, column=1, padx=3, pady=3)


#Heidolph Function

fr_heidolph_fn = tk.Frame(fr_heidolph, width=65, height = 375, relief=tk.GROOVE, bd=2)
fr_heidolph_fn.grid(row=3, column=0, padx=3, pady=3, sticky="nsew")
fr_heidolph_fn.rowconfigure(5, minsize=10, weight=1)
fr_heidolph_fn.columnconfigure(6, minsize=10, weight=1)
fr_heidolph_fn.grid_propagate(0)

list_lbl_heidolph_1 = ["After","Speed","Temp","Rotation","Heating"]
for i in range(0,5):
    tk.Label(fr_heidolph_fn, text = list_lbl_heidolph_1[i], width=20, height=2).grid(row=i, column=0, padx=3,pady=3)

ent_heidolph_01 = tk.Entry(fr_heidolph_fn, width=10)
ent_heidolph_01.grid(row=0, column=1, padx=3, pady=3)
ent_heidolph_11 = tk.Entry(fr_heidolph_fn, width=10)
ent_heidolph_11.grid(row=1, column=1, padx=3, pady=3)
ent_heidolph_21 = tk.Entry(fr_heidolph_fn, width=10)
ent_heidolph_21.grid(row=2, column=1, padx=3, pady=3)

list_lbl_heidolph_2 = ["min","rpm","℃","Stop","Stop"]
for i in range(0,5):
    tk.Label(fr_heidolph_fn, text = list_lbl_heidolph_2[i], width=10, height=2).grid(row=i, column=2, padx=3,pady=3)

tk.Button(fr_heidolph_fn, text = "Add", width=5, height=1, command = lambda:heidolph_rotating(int(com_heidolph_num.get()), ent_heidolph_01, ent_heidolph_11)).grid(row=1, column=3, padx=3, pady=3)
tk.Button(fr_heidolph_fn, text = "Add", width=5, height=1, command = lambda:heidolph_heating(int(com_heidolph_num.get()), ent_heidolph_01, ent_heidolph_21)).grid(row=2, column=3, padx=3, pady=3)
tk.Button(fr_heidolph_fn, text = "Add", width=5, height=1, command = lambda:heidolph_stop_rotating(int(com_heidolph_num.get()), ent_heidolph_01)).grid(row=3, column=3, padx=3, pady=3)
tk.Button(fr_heidolph_fn, text = "Add", width=5, height=1, command = lambda:heidolph_stop_heating(int(com_heidolph_num.get()), ent_heidolph_01)).grid(row=4, column=3, padx=3, pady=3)


#Valve Panel

fr_valve = tk.Frame(window, width =450, height = 700,relief = tk.FLAT, bd =2)
fr_valve.grid(row=0, column=1, padx=5,pady=5)
fr_valve.grid_propagate(0)
fr_valve.rowconfigure(4, weight=1)
fr_valve.columnconfigure(0, weight=1)

#Valve Initialization

tk.Label(fr_valve, text = "Valve Initialization Command Editor", width=50, height=2, font=("calibri",12,"bold")).grid(row=0, column=0, padx=3, pady=3)

fr_valve_init = tk.Frame(fr_valve, width=65, height = 370, relief=tk.GROOVE, bd=2)
fr_valve_init.grid(row=1, column=0, padx=3, pady=3, sticky="nsew")

for i in range(0,6):

    for j in [0,3]:

        tk.Label(fr_valve_init, text = "Valve %d"%(i+1+j*2), width=10, height=2).grid(row=i, column=j, padx=3, pady=3)    

        globals()["com_valve_%d_init"%(i+1+j*2)] = ttk.Combobox(fr_valve_init, width=8, value = com_value)
       
        globals()["com_valve_%d_init"%(i+1+j*2)].grid(row=i, column=j+1, padx=3, pady=3)
       
tk.Button(fr_valve_init, text = "Add", width=5, height=1, command = lambda:instru_init("valve",1,com_valve_1_init.get())).grid(row=0, column=2, padx=3, pady=3)
tk.Button(fr_valve_init, text = "Add", width=5, height=1, command = lambda:instru_init("valve",2,com_valve_2_init.get())).grid(row=1, column=2, padx=3, pady=3)
tk.Button(fr_valve_init, text = "Add", width=5, height=1, command = lambda:instru_init("valve",3,com_valve_3_init.get())).grid(row=2, column=2, padx=3, pady=3)
tk.Button(fr_valve_init, text = "Add", width=5, height=1, command = lambda:instru_init("valve",4,com_valve_4_init.get())).grid(row=3, column=2, padx=3, pady=3)
tk.Button(fr_valve_init, text = "Add", width=5, height=1, command = lambda:instru_init("valve",5,com_valve_5_init.get())).grid(row=4, column=2, padx=3, pady=3)
tk.Button(fr_valve_init, text = "Add", width=5, height=1, command = lambda:instru_init("valve",6,com_valve_6_init.get())).grid(row=5, column=2, padx=3, pady=3)
tk.Button(fr_valve_init, text = "Add", width=5, height=1, command = lambda:instru_init("valve",7,com_valve_7_init.get())).grid(row=0, column=5, padx=3, pady=3)
tk.Button(fr_valve_init, text = "Add", width=5, height=1, command = lambda:instru_init("valve",8,com_valve_8_init.get())).grid(row=1, column=5, padx=3, pady=3)
tk.Button(fr_valve_init, text = "Add", width=5, height=1, command = lambda:instru_init("valve",9,com_valve_9_init.get())).grid(row=2, column=5, padx=3, pady=3)
tk.Button(fr_valve_init, text = "Add", width=5, height=1, command = lambda:instru_init("valve",10,com_valve_10_init.get())).grid(row=3, column=5, padx=3, pady=3)
tk.Button(fr_valve_init, text = "Add", width=5, height=1, command = lambda:instru_init("valve",11,com_valve_11_init.get())).grid(row=4, column=5, padx=3, pady=3)
tk.Button(fr_valve_init, text = "Add", width=5, height=1, command = lambda:instru_init("valve",12,com_valve_12_init.get())).grid(row=5, column=5, padx=3, pady=3)


#Valve Number

fr_valve_num = tk.Frame(fr_valve, width=65, height = 100, relief=tk.FLAT, bd=2)
fr_valve_num.grid(row=2, column=0, padx=3, pady=3, sticky="nsew")

tk.Label(fr_valve_num, text = "\tCommand Editor for Valve ", width=40, height=2, font=("calibri",12,"bold")).grid(row=0, column=0, padx=3, pady=3)

com_valve = []
for i in range (1,13):
    com_valve.append(i)

com_valve_num = ttk.Combobox(fr_valve_num, width=4, height=6, font=("calibri",12,"bold"), value = com_valve)
com_valve_num.grid(row=0, column=1, padx=3, pady=3)


#Valve Function

fr_valve_fn = tk.Frame(fr_valve, width=65, height = 190, relief=tk.GROOVE, bd=2)
fr_valve_fn.grid(row=3, column=0, padx=3, pady=3, sticky="nsew")
fr_valve_fn.rowconfigure(5, minsize=10, weight=1)
fr_valve_fn.columnconfigure(6, minsize=10, weight=1)
fr_valve_fn.grid_propagate(0)


tk.Label(fr_valve_fn, text = "After ", width=20, height=2).grid(row=0, column=0, padx=3,pady=3)

ent_valve_time = tk.StringVar()
       
tk.Entry(fr_valve_fn, textvariable = ent_valve_time, width=10).grid(row=0, column=1, padx=3, pady=3)

tk.Label(fr_valve_fn, text = "min ", width=8, height=2).grid(row=0, column=2, padx=3,pady=3)

tk.Label(fr_valve_fn, text = "Go to position ", width=20, height=2).grid(row=1, column=0, padx=3,pady=3)

ent_valve_position = tk.StringVar()
       
tk.Entry(fr_valve_fn, textvariable = ent_valve_position, width=10).grid(row=1, column=1, padx=3, pady=3)

tk.Button(fr_valve_fn, text = "Add", width=5, height=1, command = lambda:valve_going(int(com_valve_num.get()), ent_valve_time, ent_valve_position)).grid(row=1, column=2, padx=3, pady=3)

#Ou Shisheng Panel

fr_oushisheng = tk.Frame(window, width =450, height = 700,relief = tk.FLAT, bd =2)
fr_oushisheng.grid(row=0, column=1, padx=5,pady=5)
fr_oushisheng.grid_propagate(0)
fr_oushisheng.rowconfigure(4, weight=1)
fr_oushisheng.columnconfigure(0, weight=1)
   

#Ou Shisheng Initialization

tk.Label(fr_oushisheng, text = "Ou Shisheng Initialization Command Editor", width=50, height=2, font=("calibri",12,"bold")).grid(row=0, column=0, padx=3, pady=3)

fr_oushisheng_init = tk.Frame(fr_oushisheng, width=65, height = 185, relief=tk.GROOVE, bd=2)
fr_oushisheng_init.grid(row=1, column=0, padx=3, pady=3, sticky="nsew")

for i in range(0,3):

    for j in [0,3]:

        tk.Label(fr_oushisheng_init, text = "Ou %d"%(i+1+j), width=10, height=2).grid(row=i, column=j, padx=3, pady=3)    

        globals()["com_oushisheng_%d_init"%(i+1+j)] = ttk.Combobox(fr_oushisheng_init, width=8, value = com_value)
       
        globals()["com_oushisheng_%d_init"%(i+1+j)].grid(row=i, column=j+1, padx=3, pady=3)
       
        tk.Button(fr_oushisheng_init, text = "Add", width=5, height=1, command = lambda:oushisheng_init((i+1+j),globals()["com_oushisheng_%d_init"%(i+1+j)].get())).grid(row=i, column=j+2, padx=3, pady=3)

tk.Button(fr_oushisheng_init, text = "Add", width=5, height=1, command = lambda:instru_init("oushisheng",1,com_oushisheng_1_init.get())).grid(row=0, column=2, padx=3, pady=3)
tk.Button(fr_oushisheng_init, text = "Add", width=5, height=1, command = lambda:instru_init("oushisheng",2,com_oushisheng_2_init.get())).grid(row=1, column=2, padx=3, pady=3)
tk.Button(fr_oushisheng_init, text = "Add", width=5, height=1, command = lambda:instru_init("oushisheng",3,com_oushisheng_3_init.get())).grid(row=2, column=2, padx=3, pady=3)
tk.Button(fr_oushisheng_init, text = "Add", width=5, height=1, command = lambda:instru_init("oushisheng",4,com_oushisheng_4_init.get())).grid(row=0, column=5, padx=3, pady=3)
tk.Button(fr_oushisheng_init, text = "Add", width=5, height=1, command = lambda:instru_init("oushisheng",5,com_oushisheng_5_init.get())).grid(row=1, column=5, padx=3, pady=3)
tk.Button(fr_oushisheng_init, text = "Add", width=5, height=1, command = lambda:instru_init("oushisheng",6,com_oushisheng_6_init.get())).grid(row=2, column=5, padx=3, pady=3)

#Ou Shisheng number
       
fr_oushisheng_num = tk.Frame(fr_oushisheng, width=65, height = 100, relief=tk.FLAT, bd=2)
fr_oushisheng_num.grid(row=2, column=0, padx=3, pady=3, sticky="nsew")

tk.Label(fr_oushisheng_num, text = "\tCommand Editor for Ou Shisheng ", width=40, height=2, font=("calibri",12,"bold")).grid(row=0, column=0, padx=3, pady=3)

com_oushisheng = []
for i in range (1,7):
    com_oushisheng.append(i)

com_oushisheng_num = ttk.Combobox(fr_oushisheng_num, width=4, height=6, font=("calibri",12,"bold"), value = com_sf10)
com_oushisheng_num.grid(row=0, column=1, padx=3, pady=3)

#Ou Shisheng Function
       
fr_oushisheng_fn = tk.Frame(fr_oushisheng, width=65, height = 380, relief=tk.GROOVE, bd=2)
fr_oushisheng_fn.grid(row=3, column=0, padx=3, pady=3, sticky="nsew")
fr_oushisheng_fn.rowconfigure(8, minsize=10, weight=1)
fr_oushisheng_fn.columnconfigure(7, minsize=10, weight=1)
fr_oushisheng_fn.grid_propagate(0)

list_lbl_oushisheng=["After","Flow","","min","ul/min","ml/min","","for 20 ml range","for 200 ml range"]

for i in range(0,3):

    tk.Label(fr_oushisheng_fn, text = list_lbl_oushisheng[i], width=10, height=2).grid(row=i, column=0, padx=3,pady=3)    

    tk.Label(fr_oushisheng_fn, text = list_lbl_oushisheng[i+3], width=10, height=2).grid(row=i, column=2, padx=3,pady=3)

    tk.Label(fr_oushisheng_fn, text = list_lbl_oushisheng[i+6], width=15, height=2).grid(row=i, column=3, padx=3,pady=3)

ent_oushisheng_time = tk.Entry(fr_oushisheng_fn, width=10)
ent_oushisheng_time.grid(row=0, column=1, padx=3, pady=3)

ent_oushisheng_rate_1 = tk.Entry(fr_oushisheng_fn, width=10)
ent_oushisheng_rate_1.grid(row=1, column=1, padx=3, pady=3)

ent_oushisheng_rate_2 = tk.Entry(fr_oushisheng_fn, width=10)
ent_oushisheng_rate_2.grid(row=2, column=1, padx=3, pady=3)

tk.Button(fr_oushisheng_fn, text = "Add", width=5, height=1, command = lambda:oushisheng_pumping(int(com_oushisheng_num.get()), ent_oushisheng_time, ent_oushisheng_rate_1, 1)).grid(row=1, column=4, padx=3, pady=3)
tk.Button(fr_oushisheng_fn, text = "Add", width=5, height=1, command = lambda:oushisheng_pumping(int(com_oushisheng_num.get()), ent_oushisheng_time, ent_oushisheng_rate_2, 2)).grid(row=2, column=4, padx=3, pady=3)
tk.Button(fr_oushisheng_fn, text = "Stop", width=5, height=1, command = lambda:oushisheng_stoping(int(com_oushisheng_num.get()), ent_oushisheng_time)).grid(row=3, column=4, padx=3, pady=3)

#Watson Panel

fr_watson = tk.Frame(window, width =450, height = 700,relief = tk.FLAT, bd =2)
fr_watson.grid(row=0, column=1, padx=5,pady=5)
fr_watson.grid_propagate(0)
fr_watson.rowconfigure(4, weight=1)
fr_watson.columnconfigure(0, weight=1)
   

#Watson Initialization

tk.Label(fr_watson, text = "Watson Marlow Initialization Command Editor", width=50, height=2, font=("calibri",12,"bold")).grid(row=0, column=0, padx=3, pady=3)

fr_watson_init = tk.Frame(fr_watson, width=65, height = 185, relief=tk.GROOVE, bd=2)
fr_watson_init.grid(row=1, column=0, padx=3, pady=3, sticky="nsew")

for i in range(0,3):

    for j in [0,3]:

        tk.Label(fr_watson_init, text = "Watson %d"%(i+1+j), width=10, height=2).grid(row=i, column=j, padx=3, pady=3)    

        globals()["com_watson_%d_init"%(i+1+j)] = ttk.Combobox(fr_watson_init, width=8, value = com_value)
       
        globals()["com_watson_%d_init"%(i+1+j)].grid(row=i, column=j+1, padx=3, pady=3)
       
        tk.Button(fr_watson_init, text = "Add", width=5, height=1, command = lambda:watson_init((i+1+j),globals()["com_watson_%d_init"%(i+1+j)].get())).grid(row=i, column=j+2, padx=3, pady=3)

tk.Button(fr_watson_init, text = "Add", width=5, height=1, command = lambda:instru_init("watson",1,com_watson_1_init.get())).grid(row=0, column=2, padx=3, pady=3)
tk.Button(fr_watson_init, text = "Add", width=5, height=1, command = lambda:instru_init("watson",2,com_watson_2_init.get())).grid(row=1, column=2, padx=3, pady=3)
tk.Button(fr_watson_init, text = "Add", width=5, height=1, command = lambda:instru_init("watson",3,com_watson_3_init.get())).grid(row=2, column=2, padx=3, pady=3)
tk.Button(fr_watson_init, text = "Add", width=5, height=1, command = lambda:instru_init("watson",4,com_watson_4_init.get())).grid(row=0, column=5, padx=3, pady=3)
tk.Button(fr_watson_init, text = "Add", width=5, height=1, command = lambda:instru_init("watson",5,com_watson_5_init.get())).grid(row=1, column=5, padx=3, pady=3)
tk.Button(fr_watson_init, text = "Add", width=5, height=1, command = lambda:instru_init("watson",6,com_watson_6_init.get())).grid(row=2, column=5, padx=3, pady=3)

#Watson number
       
fr_watson_num = tk.Frame(fr_watson, width=65, height = 100, relief=tk.FLAT, bd=2)
fr_watson_num.grid(row=2, column=0, padx=3, pady=3, sticky="nsew")

tk.Label(fr_watson_num, text = "\tCommand Editor for Watson Marlow", width=40, height=2, font=("calibri",12,"bold")).grid(row=0, column=0, padx=3, pady=3)

com_watson = []
for i in range (1,7):
    com_watson.append(i)

com_watson_num = ttk.Combobox(fr_watson_num, width=4, height=6, font=("calibri",12,"bold"), value = com_watson)
com_watson_num.grid(row=0, column=1, padx=3, pady=3)

#Watson Function
       
fr_watson_fn = tk.Frame(fr_watson, width=65, height = 380, relief=tk.GROOVE, bd=2)
fr_watson_fn.grid(row=3, column=0, padx=3, pady=3, sticky="nsew")
fr_watson_fn.rowconfigure(8, minsize=10, weight=1)
fr_watson_fn.columnconfigure(7, minsize=10, weight=1)
fr_watson_fn.grid_propagate(0)

tk.Label(fr_watson_fn, text = "Direction A", width=10, height=1).grid(row=0, column=1)
tk.Label(fr_watson_fn, text = "Direction B", width=10, height=1).grid(row=0, column=4)

tk.Label(fr_watson_fn, text = "After", width=8, height=2).grid(row=1, column=0, padx=3,pady=3)
tk.Label(fr_watson_fn, text = "Speed", width=8, height=2).grid(row=2, column=0, padx=3,pady=3)
tk.Label(fr_watson_fn, text = "Dose", width=8, height=2).grid(row=3, column=0, padx=3,pady=3)
tk.Label(fr_watson_fn, text = "Stop", width=8, height=2).grid(row=4, column=0, padx=3,pady=3)

 
for i in range(1,4):

    for j in [1,4]: # for entry

        globals()["ent_watson_" + str(i) + str(j)] = tk.StringVar()
        globals()["ent_watson_" + str(i) + str(j)].set(0)
       
        tk.Entry(fr_watson_fn, textvariable = globals()["ent_watson_" + str(i) + str(j)], width=10).grid(row=i, column=j, padx=3, pady=3)


for i in [2,5]: # for label

    tk.Label(fr_watson_fn, text = "min", width=5, height=2).grid(row=1, column=i, padx=3, pady=3)
    tk.Label(fr_watson_fn, text = "RPM", width=5, height=2).grid(row=2, column=i, padx=3, pady=3)
    tk.Label(fr_watson_fn, text = "tacho", width=5, height=2).grid(row=3, column=i, padx=3, pady=3)
   

    # for button

tk.Button(fr_watson_fn, text = "Add", width=5, height=1, command = lambda:watson_pumping(int(com_watson_num.get()), "RL", ent_watson_11, ent_watson_21)).grid(row=2, column=3, padx=3, pady=3)
tk.Button(fr_watson_fn, text = "Add", width=5, height=1, command = lambda:watson_dosing(int(com_watson_num.get()), "RL", ent_watson_11, ent_watson_31)).grid(row=3, column=3, padx=3, pady=3)
tk.Button(fr_watson_fn, text = "Add", width=5, height=1, command = lambda:watson_stoping(int(com_watson_num.get()), "RL", ent_watson_11)).grid(row=4, column=3, padx=3, pady=3)


tk.Button(fr_watson_fn, text = "Add", width=5, height=1, command = lambda:watson_pumping(int(com_watson_num.get()), "RR", ent_watson_14, ent_watson_24)).grid(row=2, column=6, padx=3, pady=3)
tk.Button(fr_watson_fn, text = "Add", width=5, height=1, command = lambda:watson_dosing(int(com_watson_num.get()), "RR", ent_watson_14, ent_watson_34)).grid(row=3, column=6, padx=3, pady=3)
tk.Button(fr_watson_fn, text = "Add", width=5, height=1, command = lambda:watson_stoping(int(com_watson_num.get()), "RR", ent_watson_14)).grid(row=4, column=6, padx=3, pady=3)





"""Instrument list"""
fr_instru = tk.Frame(window, width = 150, height = 700, relief = tk.RAISED, bd =2, bg="grey")
fr_instru.grid(row=0, column=0, padx=5,pady=5)
fr_instru.rowconfigure(8, weight=1)
fr_instru.grid_propagate(0)

tk.Label(fr_instru, text = "Instruments", width=15, height=2, font=("calibri",12,"bold")).grid(row=0, column=0, padx=3, pady=3)

tk.Button(fr_instru, text = "Asia Pump", width=10, height=1,command = lambda:topWin(fr_asiapump)).grid(row = 1, column = 0, padx=3, pady=3)
tk.Button(fr_instru, text = "SF 10", width=10, height=1, command = lambda:topWin(fr_sf10)).grid(row = 2, column = 0, padx=3, pady=3)
tk.Button(fr_instru, text = "MilliGAT", width=10, height=1, command = lambda:topWin(fr_milliGAT)).grid(row = 3, column = 0, padx=3, pady=3)
tk.Button(fr_instru, text = "Ou Shisheng", width=10, height=1, command = lambda:topWin(fr_oushisheng)).grid(row = 4, column = 0, padx=3, pady=3)
tk.Button(fr_instru, text = "Heidolph", width=10, height=1, command = lambda:topWin(fr_heidolph)).grid(row = 5, column = 0, padx=3, pady=3)
tk.Button(fr_instru, text = "valve", width=10, height=1, command = lambda:topWin(fr_valve)).grid(row = 6, column = 0, padx=3, pady=3)
tk.Button(fr_instru, text = "Watson", width=10, height=1, command = lambda:topWin(fr_watson)).grid(row =7, column = 0, padx=3, pady=3)

window.mainloop()
