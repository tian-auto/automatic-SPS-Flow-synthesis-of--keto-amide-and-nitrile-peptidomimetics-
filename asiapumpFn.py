from ctypes import *
from threading import Timer
import tkinter
import time

class asiapumpFn:

    asiapump = cdll.LoadLibrary("C:\\Users\\Administrator\\Desktop\\pythonfile\\0304\\AsiaPumpInterface_x64.dll")

    pumpNum = 0

    lbl_asiapump_sta = tkinter.Label

#Get Pump Status

    def asiapump_status(self):

        asiapump = self.asiapump
        pumpNum = self.pumpNum

        #Get syringe size
        getSize_0 = c_float()
        pGetSize_0 = pointer(getSize_0)
        getSize_1 = c_float()    
        pGetSize_1 = pointer(getSize_1)
        
        tryGetSyringe_0 = asiapump.getSyringeSize(pumpNum,0,pGetSize_0)
        tryGetSyringe_1 = asiapump.getSyringeSize(pumpNum,1,pGetSize_1)

        syringeSize_0 = float(getSize_0.value)
        syringeSize_1 = float(getSize_1.value)
        
        #Get pump status 0
        
        chanErr_0 = c_int()
        pChanErr_0 = pointer(chanErr_0)
        chanPumpState_0 = c_int()
        pChanPumpState_0 = pointer(chanPumpState_0)
        chanPumpRate_0 = c_float()
        pChanPumpRate_0 = pointer(chanPumpRate_0)
        chanPres_0 = c_float()
        pChanPres_0 = pointer(chanPres_0)
        chanLastOverPres_0 = c_float()
        pChanLastOverPres_0 = pointer(chanLastOverPres_0)

        asiapump.pumpStatus(pumpNum,0,pChanErr_0,pChanPumpState_0,pChanPumpRate_0,pChanPres_0,pChanLastOverPres_0)

        flowrate_0 = float(chanPumpRate_0.value)
        pressure_0 = float(chanPres_0.value)

        #Get pump status 1
                                      
        chanErr_1 = c_int()
        pChanErr_1 = pointer(chanErr_1)
        chanPumpState_1 = c_int()
        pChanPumpState_1 = pointer(chanPumpState_1)
        chanPumpRate_1 = c_float()
        pChanPumpRate_1 = pointer(chanPumpRate_1)
        chanPres_1 = c_float()
        pChanPres_1 = pointer(chanPres_1)
        chanLastOverPres_1 = c_float()
        pChanLastOverPres_1 = pointer(chanLastOverPres_1)

        asiapump.pumpStatus(pumpNum,1,pChanErr_1,pChanPumpState_1,pChanPumpRate_1,pChanPres_1,pChanLastOverPres_1)

        flowrate_1 = float(chanPumpRate_1.value)
        pressure_1 = float(chanPres_1.value)

        return syringeSize_0, syringeSize_1, flowrate_0, flowrate_1, pressure_0, pressure_1

#Initialization

    def asiapump_keepActi(self):

        self.asiapump_status_update()
          
        Timer(5,self.asiapump_keepActi,()).start()

    def asiapump_init(self, lbl_init):

        asiapump = self.asiapump
        pumpNum = self.pumpNum
        
        tryscan = asiapump.scanForAsiaPumps()
   
        tryenter = asiapump.enterRemoteMode(pumpNum)

        self.asiapump_keepActi()

        if (tryscan & tryenter):
        
            lbl_init["text"] += "Connect to Asiapump successfully\n"
        
        else:
        
            lbl_init["text"] += "Fail to find Asiapump\n"


    def asiapump_status_update(self):

        syringesize_0, syringesize_1, flowrate_0, flowrate_1, pressure_0, pressure_1 = self.asiapump_status()
        
        self.lbl_asiapump_sta["text"] = "Syringe Size 1:\t%.2f ul\nSyringe Size 2:\t%.2f ul\nFlow Rate 1:\t%.2f ul/min\nFlow Rate 2:\t%.2f ul/min\nPump Pressure 1:\t%.2f\nPump Pressure 2:\t%.2f\n" %(syringesize_0,syringesize_1,flowrate_0,flowrate_1,pressure_0, pressure_1)
    

#Update label

    def asiapump_lbl_update(self, value, lbl):

        lbl["text"] = time.strftime("%Y-%m-%d %H:%M:%S\n\t",time.localtime()) + lbl["text"]

        if value:

            lbl.configure(bg = "blue")

        else:

            lbl.configure(bg = "red")
            GetLastError()

        self.asiapump_status_update()

#Fillup

    def asiapump_filling(self, channel, timeEntry, fillrate, lbl):

        asiapump = self.asiapump
        pumpNum = self.pumpNum
        
        time.sleep(timeEntry*60)
        
        tryfill = asiapump.fill(pumpNum,channel, c_float(fillrate))
        
        self.asiapump_lbl_update(tryfill, lbl)

#Empty

    def asiapump_emptying(self, channel, timeEntry, emptyrate, lbl):

        asiapump = self.asiapump
        pumpNum = self.pumpNum

        time.sleep(timeEntry*60)

        asiapump.pumpStop(pumpNum, channel)

        time.sleep(10)

        tryempty = asiapump.empty(pumpNum,channel,c_float(emptyrate))
        
        self.asiapump_lbl_update(tryempty, lbl)

#Pumping

    def asiapump_pumping(self, channel, timeEntry, pumprate, lbl):

        asiapump = self.asiapump
        pumpNum = self.pumpNum

        time.sleep(timeEntry*60)

        trypump = asiapump.pump(pumpNum,channel,c_float(pumprate))
        
        self.asiapump_lbl_update(trypump, lbl)

#Stoping

    def asiapump_stoping(self, channel, timeEntry, lbl):

        asiapump = self.asiapump
        pumpNum = self.pumpNum

        time.sleep(timeEntry*60)

        trystop = asiapump.pumpStop(pumpNum, channel)

        self.asiapump_lbl_update(trystop, lbl)
    
#Finishing

    def close(self):

        asiapump = self.asiapump
        pumpNum = self.pumpNum

        asiapump.stopAllPumps()
        asiapump.exitRemoteMode(pumpNum)
        asiapump.clearUp()

#Get Error

    def asiapump_getlasterror(self):

        asiapump = self.asiapump
        pumpNum = self.pumpNum

        txt = asiapump.getLastError(pumpNum)

        return txt

