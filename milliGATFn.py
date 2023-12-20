import tkinter
import time
import pyvisa

class milliGATFn:

    milliGAT = pyvisa.Resource

    lbl_milliGAT_sta = tkinter.Label
    
    def milliGAT_init(self, COM, num, lbl_init):

        try:

            self.milliGAT = pyvisa.ResourceManager().open_resource(COM)
        
            lbl_init["text"] += "Connected to MilliGAT %s successfully\n" %num
        
        except:

            lbl_init["text"] += "Fail to find MilliGAT %s\n" %num

    def milliGAT_lbl_update(self, value, lbl):

        lbl["text"] = time.strftime("%Y-%m-%d %H:%M:%S\n\t",time.localtime()) + lbl["text"]

        if value:
    
            lbl.configure(bg = "blue")

        else:

            lbl.configure(bg = "red")

    def milliGAT_pumping(self, num, timeEntry, rate, lbl): 

        try:

            milliGAT = self.milliGAT

            time.sleep(timeEntry*60)

            milliGAT.write("%sSL=%d*EU"%(num, round(rate/60)))

            self.milliGAT_lbl_update(True, lbl)

            self.lbl_milliGAT_sta["text"] = ("State:\tPumping\n" +
                                            "Rate:\t%d ul/min\n" %rate 
                                            )

        except:

            self.milliGAT_lbl_update(False, lbl)

    
    def milliGAT_volumning(self, num, timeEntry, volumn, rate, lbl): #rate in ul/min

        try:

            milliGAT = self.milliGAT

            time.sleep(timeEntry*60)

            milliGAT.write("%sVM=%d*EU"%(num, round(rate/60)))
            milliGAT.write("%sMR=%d*EU"%(num, volumn))

            self.milliGAT_lbl_update(True, lbl)

            self.lbl_milliGAT_sta["text"]  = ("State:\tVolumning\n" +
                                         "Volumn:\t%d ul\n" %volumn +
                                         "Rate:\t%d ul/min\n" %rate
                                         )
        except:
            
            self.milliGAT_lbl_update(False, lbl)
          
    def milliGAT_stoping(self, num, timeEntry, lbl): 

        try:

            milliGAT = self.milliGAT

            time.sleep(timeEntry*60)

            milliGAT.write("%sSL=0"%num)

            self.milliGAT_lbl_update(True, lbl)

            self.lbl_milliGAT_sta["text"] = ("State:\tStop\n")

        except:

            self.milliGAT_lbl_update(False, lbl)
            

    def write(self, cmd):
    
        self.milliGAT.write(cmd)


    def read(self):

        self.milliGAT.read()

    
    def close(self, num):
        
        self.milliGAT.write("%sSL=0"%num)
