
 #################################  Import relevant packages  ################################# 

import DataLib

import serial

import IRGA

import TC

import Command_proc

import datetime

import time

import global_variables as g

import Command_Dict

def main():

    #################################  Turn power on and set control type  ################################# 

    g.gv.TC_CC.send_command(Command_Dict.Command_Dict['set_ctl_type'], 1)

    g.gv.TC_CC.send_command(Command_Dict.Command_Dict['power_write'], 1)

    #TC_SC.power_off()

    #TC_DPG.power_off()

    try:

        while True:

           #################################  Machine loop  ################################# 
            
            current_time = time.time() # current time 
        
            time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S') # create time stamp in specific format
            
            Read_Instruments(g.gv.dl, g.gv.irga, g.gv.TC_SC, g.gv.TC_CC, g.gv.TC_DPG, time_stamp)  # read all instruments

            Cmd_prc = Command_proc.Command_Proc(g.gv.dl, g.gv.ser_PC.readline().decode(), time_stamp) # perform user directed action from command line
            
            Output = Cmd_prc.Do_it() # Output of said action from command processor
            
            #print(type(Output))

            ########## Checking nature of output from command processor and write back to lab PC accordingly  ####### 
            
            if isinstance(Output, bool): # Pass if False 
                
                pass

            elif isinstance(Output, tuple):  # Write to PC if output is a tuple
            
                g.gv.ser_PC.write((str(Output[0])+'---'+str(Output[1])).encode())
            
                g.gv.ser_PC.write(('\r'+'\n').encode())

            else:

                g.gv.ser_PC.write(Output.encode()) # Likely a string - display string on PC and then go to newline 
                
                g.gv.ser_PC.write(('\r'+'\n').encode())
          
            
            #print('Timestamp: '+ str(time_stamp))
            
            #print('pCO2: '+ str(dl.getParm('pCO2'))+ ' ppm')
            
            #print('pH2O: '+ str(dl.getParm('pH2O'))+ ' ppt')
            
            #print('Cell Temp: ' + str(dl.getParm('Cell_temp'))+ ' C')
            
            #print('Cell Pressure: ' + str(dl.getParm('Cell_pressure'))+ ' kPa')

            #print('Cell Voltage: ' + str(dl.getParm('IVOLT'))+ ' V')
            
            #print('\n')
        
    except KeyboardInterrupt:
     g.gv.TC_CC.send_command(Command_Dict.Command_Dict['power_write'], 0)
     print('Terminated')
    
 
def Read_Instruments(dl, irga, TC_SC, TC_CC, TC_DPG, time_stamp):

   #Function to read instruments - IRGA, TC_SC, TC_CC, TC_DPG

    #print(irga.read_IRGA())
   
   #print('reading instruments')
   
   IRGA_list = g.gv.irga.read_IRGA() # Read IRGA 

   #TC_list = [0,0,0,0]

   TC_list.append(g.gv.TC_SC.read_temperature(Command_Dict.Command_Dict['T_SC'], 0)) # read thermistor 1 of SC

   TC_list.append(g.gv.TC_SC.read_temperature(Command_Dict.Command_Dict['T_TB'], 0)) # read thermistor 2 of SC

   TC_list.append(g.gv.TC_CC.read_temperature(Command_Dict.Command_Dict['T_CC'], 0)) # read thermistor 1 of CC

   TC_list.append(g.gv.TC_DPG.read_temperature(Command_Dict.Command_Dict['T_DPG'], 0)) # read thermistor 1 of DPG

   # Updated the registers with the most recently read system variables in 

   g.gv.dl.setParm('pCO2', IRGA_list[0], time_stamp) 

   g.gv.dl.setParm('pH2O', IRGA_list[1], time_stamp)
   
   g.gv.dl.setParm('Cell_pressure', IRGA_list[2], time_stamp)
   
   g.gv.dl.setParm('Cell_temp', IRGA_list[3], time_stamp)
   
   g.gv.dl.setParm('IVOLT', IRGA_list[4], time_stamp)

   g.gv.dl.setParm('SC_T1', TC_list[0], time_stamp)

   g.gv.dl.setParm('SC_T2', TC_list[1], time_stamp)

   g.gv.dl.setParm('CC_T1', TC_list[2], time_stamp)

   g.gv.dl.setParm('DPG_T1', TC_list[3], time_stamp)

main() # Call main
