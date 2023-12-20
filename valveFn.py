import tkinter
import time
import pyvisa


class valveFn:

    valve = pyvisa.Resource

    lbl_valve_sta = tkinter.Label


    def valve_init(self, COM, num, lbl_init):

        try:

            self.valve = pyvisa.ResourceManager().open_resource(COM)
        
            lbl_init["text"] += "Connected to Valve %d successfully\n" %num
        
        except:

            lbl_init["text"] += "Fail to find Valve %d \n" %num

    def valve_lbl_update(self, value, lbl):

        lbl["text"] = time.strftime("%Y-%m-%d %H:%M:%S\n\t",time.localtime()) + lbl["text"]

        if value:

            lbl.configure(bg = "blue")

        else:

            lbl.configure(bg = "red")


    def valve_go(self, timeEntry, pos, lbl): 

        try:

            time.sleep(timeEntry*60)

            trygo = self.valve.write('/ZGO %d'%pos)

            time.sleep(1)

            trygo = self.valve.write('/ZGO %d'%pos)

            self.valve_lbl_update(True, lbl)

            self.lbl_valve_sta["text"] = ("Current Position: %d" %pos)

        except:

            self.valve_lbl_update(False, lbl)


    def write(self, cmd):
    
        self.valve.write(cmd)


    def read(self):

        self.valve.read()

    def close(self):

        self.valve.close()


