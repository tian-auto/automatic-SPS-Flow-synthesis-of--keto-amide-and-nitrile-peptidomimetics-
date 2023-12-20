import tkinter
import time
import pyvisa
from threading import Timer

class oushishengFn:

    oushisheng = pyvisa.Resource
    
    lbl_oushisheng_sta = tkinter.Label

    num = 1

    pressure = 0

    rate = 0
    
    def oushisheng_init(self, COM, num, lbl_init):

        try:

            self.oushisheng = pyvisa.ResourceManager().open_resource(COM)

            self.num = num

            self.oushisheng_lbl_status()
            
            lbl_init["text"] += "Connect to Ou Shisheng %d successfully\n" %num
        
        except:

            lbl_init["text"] += "Fail to find Ou Shisheng %d\n" %num

    def oushisheng_lbl_update(self, value, lbl):

        lbl["text"] = time.strftime("%Y-%m-%d %H:%M:%S\n\t",time.localtime()) + lbl["text"]

        if value:

            lbl.configure(bg = "blue")

        else:

            lbl.configure(bg = "red")


    def oushisheng_lbl_status(self):

        
        self.oushisheng_getpressure()

        self.lbl_oushisheng_sta["text"] = ("Rate:\t%d ul/min\n" %self.rate +
                                           "Pressure:\t%.1f bar\n" %self.pressure
                                           )

        Timer(3,self.oushisheng_lbl_status,()).start()
       

    def oushisheng_getpressure(self):

        oushisheng = self.oushisheng
        num = self.num

        oushisheng.write('P%d,Q2'%num)

        value = oushisheng.read()

        pressure_s = value[17:20]

        self.pressure = int(pressure_s)/10
        

    def oushisheng_pumping(self, timeEntry, rateEntry, lbl): 

        oushisheng = self.oushisheng
        num = self.num
        pressure = self.pressure
        
        time.sleep(timeEntry*60)

        try:
            
            oushisheng.write('P%d,S3,%05d'%(num,rateEntry))

            self.rate = rateEntry
            
            self.oushisheng_lbl_update(True, lbl)


        except:

            self.oushisheng_lbl_update(False, lbl)


        
    def oushisheng_stoping(self, timeEntry, lbl): 

        oushisheng = self.oushisheng
        num = self.num
        
        
        time.sleep(timeEntry*60)

        try:
            
            oushisheng.write('P%d,G1,0'%num)
    
            self.oushisheng_lbl_update(True, lbl)

            self.rate = 0
            
        except:

            self.oushisheng_lbl_update(False, lbl)
   

    def write(self, cmd):
    
        self.oushisheng.write(cmd)


    def read(self):

        self.oushisheng.read()

    def close(self):

        self.oushisheng.write('P%d,G1,0'%self.num)
        self.oushisheng.close()


