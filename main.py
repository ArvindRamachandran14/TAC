
import DataLib

import serial

import IRGA

import TC

import Command_proc

import datetime as dt

import time

from datetime import datetime

import global_variables as g

import Command_Dict

import json

import megaio as m

<<<<<<< HEAD
import asyncio  

async def main():
=======
import asyncio

class TAC():
>>>>>>> 86924a4c99d766db76d4b87263449191ae7ad0bc

    def __init__(self):

        self.sem = asyncio.Semaphore(1)  

        self.bdone = False

<<<<<<< HEAD
    deltaT = 2
    
    try:
=======
    async def Read_Instruments():
>>>>>>> 86924a4c99d766db76d4b87263449191ae7ad0bc

        try:

            while not self.bdone:

                async with self.sem:

                    current_time = time.time() # current time 
                    
                    time_stamp = dt.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S.%f') # create time stamp in specific format        

<<<<<<< HEAD
            #print('RH_set', g.gv.dl.getParm('RH_set'))

            #print('pH2O_set', g.gv.dl.getParm('pH2O_set'))
=======
                    IRGA_list = g.gv.irga.read_IRGA() # Read IRGA 

                    # Updated the registers with the most recently read system variables in 
>>>>>>> 86924a4c99d766db76d4b87263449191ae7ad0bc

                    g.gv.dl.setParm('pCO2', IRGA_list[0], time_stamp) 

                    g.gv.dl.setParm('pH2O', IRGA_list[1], time_stamp)
         
                    g.gv.dl.setParm('CellP', IRGA_list[2], time_stamp)

                    CellT = IRGA_list[3]
         
                    g.gv.dl.setParm('CellT', CellT, time_stamp)
         
                    g.gv.dl.setParm('IVOLT', IRGA_list[4], time_stamp)

                    DPT =  IRGA_list[5]

                    g.gv.dl.setParm('DPT', DPT, time_stamp)

                    SC_T = g.gv.TC_SC.read_value(Command_Dict.Command_Dict['SC_T_read'])/100.0

                    g.gv.dl.setParm('SC_T', SC_T, time_stamp)

                    SC_Tblock = g.gv.TC_SC.read_value(Command_Dict.Command_Dict['SC_Tblock_read'])/100.0

                    g.gv.dl.setParm('SC_Tblock', SC_Tblock, time_stamp)

                    SC_output = ((g.gv.TC_SC.read_value(Command_Dict.Command_Dict['SC_output_read'])/100.0)/5.11)*100.0 #convert to decimal then convert to %

                    g.gv.dl.setParm('SC_output', SC_output, time_stamp)

                    CC_T = g.gv.TC_CC.read_value(Command_Dict.Command_Dict['CC_T_read'])/100.0

                    g.gv.dl.setParm('CC_T', CC_T, time_stamp)

                    CC_output = ((g.gv.TC_CC.read_value(Command_Dict.Command_Dict['CC_output_read'])/100.0)/5.11)*100.0 #convert to decimal then convert to %

                    g.gv.dl.setParm('CC_output', CC_output, time_stamp)

                    DPG_T = g.gv.TC_DPG.read_value(Command_Dict.Command_Dict['DPG_T_read'])/100.0

                    g.gv.dl.setParm('DPG_T', DPG_T, time_stamp)

                    DPG_output = ((g.gv.TC_DPG.read_value(Command_Dict.Command_Dict['DPG_output_read'])/100.0)/5.11)*100.0 #convert to decimal then convert to %

                    g.gv.dl.setParm('DPG_output', DPG_output, time_stamp)

                    WGT = ((m.get_adc(0,1))/4096.0)*10

                    g.gv.dl.setParm('WGT', WGT, time_stamp)

                     ################### Check for normal operation of TA ################### 

                 if CellT > 50.0 and DPT < 45.0 and DPT > CC_T and CC_T > SC_T and SC_T > DPG_T:
                    
                     pass
                    
                 else:

                    g.gv.dl.setParm('Status', 1, time_stamp)

                await asyncio.sleep(0.050)

        except (ZeroDivisionError, RuntimeError, TypeError, NameError, KeyboardInterrupt) as e:

            self.Terminate()
   

    async def doCmd(self):

        try:

            while not self.bdone:

                async with self.sem:

                    user_input = g.gv.ser_PC.readline().decode()

                    Output = Cmd_prc.Do_it(user_input)

                    if g.gv.dl.getParm("DPG_power")[0] !=0:  

                        DPG_ctrl = Cmd_prc.Convert_to_DPG_ctrl()

                        #print(DPG_ctrl)

                        #Output_string = Cmd_prc.Set_DPG_ctrl(DPG_ctrl)  

                        #print(Output_string)

                        #print(type(Output))

                    ########## Checking nature of output from command processor and write back to lab PC accordingly  ####### 
                        
                    if isinstance(Output, bool): # Pass if False 
                                
                        pass

                    elif isinstance(Output, dict):

                        print('output is a dictionary')

                        #xmlstring = dicttoxml.dicttoxml(Output)

                        #result_string = json.dumps(Output) 

                        #g.gv.ser_PC.write(xmlstring)

                        #g.gv.ser_PC.write(('\r'+'\n').encode())


                    elif isinstance(Output, tuple):  # Write to PC if output is a tuple
                        
                        g.gv.ser_PC.write((str(Output[0])+'---'+str(Output[1])+'\n').encode())
                                
                        #g.gv.ser_PC.write(('\r'+'\n').encode())

                    else:
        
                        g.gv.ser_PC.write((Output+'\n').encode()) # Likely a string with error code - display string on PC and then go to newline 
                    
                        await asyncio.sleep(0.050)

        except (ZeroDivisionError, RuntimeError, TypeError, NameError, KeyboardInterrupt) as e:

            self.Terminate() 

    self.Terminate(self):

        g.gv.TC_SC.write_command(Command_Dict.Command_Dict['SC_power_write'], 0) #Turn power off

        g.gv.TC_CC.write_command(Command_Dict.Command_Dict['CC_power_write'], 0) #Turn power off

        g.gv.TC_DPG.write_command(Command_Dict.Command_Dict['DPG_power_write'], 0) #Turn power off

        power_CC = g.gv.TC_CC.read_value(Command_Dict.Command_Dict['CC_power_read'])
       
        power_SC = g.gv.TC_SC.read_value(Command_Dict.Command_Dict['SC_power_read'])
        
        power_DPG = g.gv.TC_DPG.read_value(Command_Dict.Command_Dict['DPG_power_read'])
 
        if power_CC == power_SC == power_DPG == 0: #Check that power was turned off

            print('Controllers turned off')

        else:

            print('One or more of the controllers still on')

        print('Terminated because ' + str(e)) #Print error messahe

async def main() :

    current_time = time.time()

    time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S.%f')

    tac = TAC()

    cmd_prc = Command_proc.Command_Proc(g.gv.dl)

    task1 = asyncio.create_task(tac.read_instruments())

    task2 = asyncio.create_task(tac.doCmd())

    await task1
    await task2
       
    print('Done')

asyncio.run(main())
