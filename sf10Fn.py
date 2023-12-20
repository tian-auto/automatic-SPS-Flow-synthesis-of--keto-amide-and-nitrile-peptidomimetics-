import tkinter
import time
import pyvisa

class sf10Fn:

    sf10 = pyvisa.Resource
    
    lbl_sf10_sta = tkinter.Label

    
    def sf10_init(self, COM, num, lbl_init):

        try:

            self.sf10 = pyvisa.ResourceManager().open_resource(COM)
        
            lbl_init["text"] += "Connect to SF10 %d successfully\n" %num
        
        except:

            lbl_init["text"] += "Fail to find SF10 %d\n" %num

    def sf10_lbl_update(self, value, lbl):
        
        lbl["text"] = time.strftime("%Y-%m-%d %H:%M:%S\n\t",time.localtime()) + lbl["text"]

        if value:

            lbl.configure(bg = "blue")

        else:

            lbl.configure(bg = "red")

    def sf10_pumping(self, chan, timeEntry, rate, lbl): 

        try:    
            sf10 = self.sf10
        
            time.sleep(timeEntry*60)

            step1 = sf10.query('VALVE %s' %chan)
            time.sleep(0.5)

            step2 = sf10.query('MODE FLOW')
            time.sleep(0.5)

            step3 = sf10.query('SETFLOW %f' %rate)
            time.sleep(0.5)

            step4 = sf10.query('START')

        
            if step1 == step2 == step3 == step4 == "OK\r\n":

                self.sf10_lbl_update(True, lbl)

                self.lbl_sf10_sta["text"] = ("State:\tSTART\n" +
                                     "Valve:\t%s\n" %chan +
                                    "Mode:\tFLOW\n" +
                                     "Rate:\t%.1f ml/min\n" %rate
                                      )           
            else:

                self.sf10_lbl_update(False, lbl)  
        except:
            
                self.sf10_lbl_update(False, lbl)  

    def sf10_gaspumping(self, chan, timeEntry, rate, lbl):

        sf10 = self.sf10
        
        time.sleep(timeEntry*60)

        step1 = sf10.query('VALVE %s' %chan)
        step2 = sf10.query('MODE GAS')
        step3 = sf10.query('SETGASFLOW %.1f' %rate)
        step4 = sf10.query('START')

        if step1 == step2 == step3 == step4 == "OK\r\n":

            self.sf10_lbl_update(True, lbl)

            self.lbl_sf10_sta["text"] = ("State:\tSTART\n" +
                                  "Valve:\t%s\n" %chan +
                                   "Mode:\tGAS FLOW\n" +
                                   "Rate:\t%.1f ml/min\n" %rate
                                   )

        else:
            
            self.sf10_lbl_update(False, lbl)  

        
    def sf10_regpresing(self, chan, timeEntry, rate, lbl): 

        sf10 = self.sf10
        
        time.sleep(timeEntry*60)

        step1 = sf10.query('VALVE %s' %chan)
        step2 = sf10.query('MODE REG')
        step3 = sf10.query('SETREG %.1f' %rate)
        step4 = sf10.query('START')

        if step1 == step2 == step3 == step4 == "OK\r\n":

            self.sf10_lbl_update(True, lbl)
        else:
            
            self.sf10_lbl_update(False, lbl)  
  
        self.lbl_sf10_sta["text"] = ("State:\tSTART\n" +
                                   "Valve:\t%s\n" %chan +
                                   "Mode:\tPRESSURE REGULATOR\n" +
                                   "Pres:\t%.1f bar\n" %rate
                                   )
        
    def sf10_setramping(self, chan, timeEntry, rate_1, rate_2, periodEntry, lbl): 

        sf10 = self.sf10
        
        time.sleep(timeEntry*60)

        step1 = sf10.query('VALVE %s' %chan)
        step2 = sf10.query('MODE RAMP')
        step3 = sf10.query('SETRAMP %.1f %.1f %.1f' %(rate_1, rate_2, periodEntry))
        step4 = sf10.query('START')

        if step1 == step2 == step3 == step4 == "OK\r\n":

            self.sf10_lbl_update(True, lbl)
        else:
            
            self.sf10_lbl_update(False, lbl)  

        self.lbl_sf10_sta["text"] = ("State:\tSTART\n" +
                                   "Valve:\t%s\n" %chan +
                                   "Mode:\tRAMP\n" +
                                   "Start rate:\t%.1f ml/min\n" %rate_1 +
                                   "End rate:\t%.1f ml/min\n" %rate_2 +
                                   "Period:\t%.1f min\n" %periodEntry
                                    )
        
    def sf10_stoping(self, chan, timeEntry, lbl): 

        try:
            sf10 = self.sf10
        
            time.sleep(timeEntry*60)

            step1 = sf10.query('STOP')
       
            if step1 == "OK\r\n":

                self.sf10_lbl_update(True, lbl)

            else:
            
                self.sf10_lbl_update(False, lbl)     
        

    
            self.lbl_sf10_sta["text"] = "State:\tSTOP\n"

        except:

            self.sf10_lbl_update(False, lbl)     

    

    def write(self, cmd):
    
        self.sf10.write(cmd)


    def read(self):

        self.sf10.read()

    def close(self):
        self.sf10.write("STOP")
        self.sf10.close()


