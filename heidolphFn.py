import tkinter
import time
import pyvisa

class heidolphFn:

    heidolph = pyvisa.Resource

    lbl_heidolph_sta = tkinter.Label


    def heidolph_init(self, COM, num, lbl_init):

        try:

            self.heidolph = pyvisa.ResourceManager().open_resource(COM)

            time.sleep(0.5)

            self.heidolph.write("PA_NEW")

            time.sleep(0.5)

            self.heidolph.write("OUT_MODE_4 0")

            time.sleep(0.5)
        
            lbl_init["text"] += "Connect to Heidolph %d successfully\n" %num
        
        except:

            lbl_init["text"] += "Fail to find Heidolph %d\n" %num

    def heidolph_status_update(self):

        heidolph = self.heidolph
    


    def heidolph_lbl_update(self, value, lbl):

        lbl["text"] = time.strftime("%Y-%m-%d %H:%M:%S\n\t",time.localtime()) + lbl["text"]

        if value:

            lbl.configure(bg = "blue")

        else:

            lbl.configure(bg = "red")
   

    def heidolph_heating(self, timeEntry, temp, lbl):

        try:

            heidolph = self.heidolph

            time.sleep(timeEntry*60)
    
            heidolph.write("OUT_SP_1 %d"%temp)

            time.sleep(0.5)

            heidolph.write("START_1")

            time.sleep(0.5)

            self.heidolph_lbl_update(True, lbl)

        except:

            self.heidolph_lbl_update(False, lbl)



    def heidolph_rotating(self, timeEntry, rpm, lbl):

        try:
            
            heidolph = self.heidolph

            time.sleep(timeEntry*60)

            heidolph.write("OUT_SP_3 %d"%rpm)

            time.sleep(0.5)

            heidolph.write("START_2")

            time.sleep(0.5)

            self.heidolph_lbl_update(True, lbl)

        except:

            self.heidolph_lbl_update(False, lbl)


    def heidolph_stop_heating(self, timeEntry, lbl):

        try:

            heidolph = self.heidolph

            time.sleep(timeEntry*60)

            heidolph.write("STOP_1")

            time.sleep(0.5)

            self.heidolph_lbl_update(True, lbl)

        except:

            self.heidolph_lbl_update(False, lbl)            


    def heidolph_stop_rotating(self, timeEntry, lbl):

        try:

            heidolph = self.heidolph

            time.sleep(timeEntry*60)

            heidolph.write("STOP_2")

            time.sleep(0.5)

            self.heidolph_lbl_update(True, lbl)

        except:

            self.heidolph_lbl_update(False, lbl)   


    def write(self, cmd):
    
        self.heidolph.write(cmd)


    def read(self):

        self.heidolph.read()

    def close(self):
        
        self.heidolph.write("STOP_2")
        
        time.sleep(0.5)
        
        self.heidolph.write("STOP_1")

        time.sleep(0.5)
        
        self.heidolph.close()


    


