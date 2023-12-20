import tkinter
import time
import pyvisa

class watsonFn:

    watson = pyvisa.Resource
    
    lbl_watson_sta = tkinter.Label

    pumpstatus = ""

    def watson_init(self, COM, num, lbl_init):

        try:

            self.watson = pyvisa.ResourceManager().open_resource(COM)
        
            lbl_init["text"] += "Connect to Watson Marlow %d successfully\n" %num

            #check parameter to determine status

            self.watson.write("RS")
            status = self.watson.read().split(",")
        
            addresscheck = status[1]
            pumptypecheck = status[2]
            pumpheadcheck = status[3]
            tubesizecheck = status[4]

            self.pumpstatus = "Address: %s\nPump Type: %s\nPump Head: %s\nTube Size: %s\n" %(addresscheck, pumptypecheck, pumpheadcheck, tubesizecheck)
            self.lbl_watson_sta["text"] = (self.pumpstatus)

        except:

            lbl_init["text"] += "Fail to find Watson Marlow %d\n" %num

    def watson_lbl_update(self, value, lbl):

        lbl["text"] = time.strftime("%Y-%m-%d %H:%M:%S\n\t",time.localtime()) + lbl["text"]

        if value == True:

            lbl.configure(bg = "cyan")

        else:

            lbl.configure(bg = "red")
        
        self.watson_status_update()

    def watson_status_update(self):

        watson = self.watson

        watson.write("RS")
        status = watson.read().split(",")
        
        #check parameter to determine status

        speedcheck = status[5]
        directioncheck = status[6]

        if status[-8] == "1":
            runcheck = "Running"
        else:
            runcheck = "Stopped"

        if status[-7] == "1":
            leakcheck = "Leaking"
        else:
            leakcheck = "No leaking"

        self.lbl_watson_sta["text"] = (self.pumpstatus + "Speed: %s\n, Direction: %s\n, Status: %s\n, Leak Check: %s\n"%(speedcheck, directioncheck, runcheck, leakcheck))     

    def watson_pumping(self, chan, timeEntry, rate, lbl): 
        try: 
            watson = self.watson
        
            time.sleep(timeEntry*60)

            watson.write(chan)
            watson.write('SP %d' %rate)
            watson.write('GO')
        
            self.watson_lbl_update(True, lbl)

        except: 
            
            self.watson_lbl_update(False, lbl)
            
    def watson_dosing(self, chan, timeEntry, rate, lbl): 
        try: 
            watson = self.watson
        
            time.sleep(timeEntry*60)

            watson.write(chan)
            watson.write('DO %d' %rate)
            watson.write('GO')
        
            self.watson_lbl_update(True, lbl)

        except: 
            
            self.watson_lbl_update(False, lbl)

    def watson_stoping(self, chan, timeEntry, lbl): 
        try: 
            watson = self.watson
        
            time.sleep(timeEntry*60)

            watson.write("ST")
        
            self.watson_lbl_update(True, lbl)

        except: 
            
            self.watson_lbl_update(False, lbl)
        
        
  

    def write(self, cmd):
    
        self.watson.write(cmd)


    def read(self):

        self.watson.read()

    def close(self):
        
        self. watson.write("ST")
        self.watson.close()


