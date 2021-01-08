############## Module that processes the commands from the user ##############

import global_variables as g

import Command_Dict

import datetime

import time

import os 

from math import exp, log

import asyncio #timing to work right asychronous call - go and read the data and the meanwhile you can do other things


class Command_Proc():
    """docstring for Command_Proc"""

    def __init__(self, dl):

        self.dl = dl

        self.switch = ['off', 'on']

        self.err = 0.0
        self.err_1 = 0.0                            # Previous value of error
        self.errDot = 0.0                           # Derivative of error at iternation n
        self.errSum = 0.0   
        self.deltaT = 3.0 #machine cycle is roughly 3 seconds 

    def Do_it(self, time_stamp, string):

        ############# Function that executes the command #############s
    
        #print(self.strings)

        self.time_stamp = time_stamp

        self.string = string

        self.strings =  self.string.split('\n')[0].split(' ')

        if self.strings in ([u''], [u'\n'], [u'\r']): # User enters a new line or does not enter anything - no action requied, return False
            
            return False

        elif self.string == 'c-check\n':

            return 'Ok\n'

        elif self.strings[0] == 's': #Check to see if command is a set command
        
            print(self.strings)
                
        if self.strings[1] in self.dl.getParmDict().keys(): # Check if the variable to be set is legit
                    
            #print(float(self.strings[2]))

            #print(self.strings[1])

            ###### check if self.strings[1] is a parameter that can actually be set or if it is a readonly paramter
            if self.strings[1] == "ByPass":

                os.system("megaio 0 rwrite 8 "+self.switch[int(self.strings[2])])

                current_time = time.time() # current time 

                time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

                g.gv.dl.setParm(self.strings[1], int(self.strings[2]), time_stamp)

                Output_string = 'e 0'

                #return(Output_string)

                elif self.strings[1] == "IRGA_pump":

                    os.system("megaio 0 rwrite 8 "+self.switch[int(self.strings[2])])

                    current_time = time.time() # current time 

                    time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

                    g.gv.dl.setParm(self.strings[1], int(self.strings[2]), time_stamp)

                    Output_string = 'e 0'

                    #return(Output_string)

                elif self.strings[1][0:2] == "SC":

                    #Need to check if the self.strings[2] (set point) is a legit value - float/int, within range

                    Output_string = g.gv.TC_SC.write_command(Command_Dict.Command_Dict[self.strings[1]+'_write'], int(float(self.strings[2])*100)) # Performing set operation, return string - Done, Input Error, Checksum Error

                    print(Output_string)

                    if Output_string == "Done":

                        current_time = time.time() # current time 

                        time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

                        g.gv.dl.setParm(self.strings[1], g.gv.TC_SC.read_value(Command_Dict.Command_Dict[self.strings[1]+'_read'])/100.0, time_stamp)

                        Output_string = 'e 0'

                        #return(Output_string)

                elif self.strings[1][0:2] == "CC":

                    #Need to check if the set point is a legit value - float/int, within range
                        
                    Output_string = g.gv.TC_CC.write_command(Command_Dict.Command_Dict[self.strings[1]+'_write'], int(float(self.strings[2])*100))

                    print(Output_string)

                    if Output_string == "Done":

                        current_time = time.time() # current time 

                        time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

                        g.gv.dl.setParm(self.strings[1], g.gv.TC_CC.read_value(Command_Dict.Command_Dict[self.strings[1]+'_read'])/100.0, time_stamp)

                        Output_string = 'e 0'

                        #return(Output_string)

                elif self.strings[1] == "DPG_power":

                    Output_string = g.gv.TC_DPG.write_command(Command_Dict.Command_Dict[self.strings[1]+'_write'], int(float(self.strings[2])*100))

                    print(Output_string)

                    if Output_string == "Done":

                        current_time = time.time() # current time 

                        time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

                        g.gv.dl.setParm(self.strings[1], g.gv.TC_DPG.read_value(Command_Dict.Command_Dict[self.strings[1]+'_read'])/100.0, time_stamp)

                        Output_string = 'e 0'

                elif self.strings[1]== "pH2O_P":
            
                    current_time = time.time() # current time 

                    time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

                    g.gv.dl.setParm(self.strings[1], float(self.strings[2]), time_stamp)

                    self.dl.cfg["pH2O_P"] = float(self.strings[2])

                    self.dl.cfg.update()

                    Output_string = 'e 0'
                        

                elif self.strings[1]== "pH2O_I":
            
                    current_time = time.time() # current time 

                    time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

                    g.gv.dl.setParm(self.strings[1], float(self.strings[2]), time_stamp)

                    self.dl.cfg["pH2O_I"] = float(self.strings[2])

                    self.dl.cfg.update()

                    Output_string = 'e 0'

                elif self.strings[1]== "pH2O_D":
            
                    current_time = time.time() # current time 

                    time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')            

                    g.gv.dl.setParm(self.strings[1], float(self.strings[2]), time_stamp)

                    self.dl.cfg["pH2O_D"] = float(self.strings[2])

                    self.dl.cfg.update()

                    Output_string = 'e 0'

                elif self.strings[1] == "DPG_set": 
                
                    current_time = time.time() # current time 

                    time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

                    g.gv.dl.setParm("DPG_set", float(self.strings[2]),time_stamp)

                    g.gv.dl.setParm("RH_set", 0.0, time_stamp)

                    g.gv.dl.setParm("pH2O_set", 0.0, time_stamp)

                    Output_string = 'e 0'

                elif self.strings[1] == "RH_set":
                
                    current_time = time.time() # current time 

                    time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

                    g.gv.dl.setParm("DPG_set", 0.0, time_stamp)

                    g.gv.dl.setParm("RH_set", float(self.strings[2]), time_stamp)

                    g.gv.dl.setParm("pH2O_set", 0.0, time_stamp)

                    Output_string = 'e 0'

                elif self.strings[1] == "pH2O_set":

                    current_time = time.time() # current time 

                    time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

                    g.gv.dl.setParm("DPG_set", 0.0, time_stamp)

                    g.gv.dl.setParm("RH_set", 0.0, time_stamp)

                    g.gv.dl.setParm("pH2O_set", float(self.strings[2]), time_stamp)

                    Output_string = 'e 0'

                    #DPG_set = Convert_to_DPG_set(self.strings[1], self.strings[2])

                    #Need to check if the set point is a legit value - float/int, within range - input validation done on TAGUI end 

                    #Output_string = g.gv.TC_DPG.write_command(Command_Dict.Command_Dict[self.strings[1]+'_write'], int(float(self.strings[2])*100))

                    #return(Output_string)

                else: 

                    Output_string = 'e 3' #readonly paramter

                    #return(Output_string) 

            else:

                Output_string = 'e 2' # Variable does not exist, return error message string  

                return(Output_string)

        elif self.strings[0] == 'g': #Check to see if command is a get command     

            #print(self.strings)
            
            if self.strings[1] == 'all':

                #print('getting all data')

                return(self.dl.get_all_data())

            elif self.strings[1] == 'cal_variables':
            
                print('g cal_variables command received')

                return(self.dl.get_cal_data())


            elif self.strings[1] in self.dl.getParmDict().keys(): # Check if the variable requeseted is legit

                return(self.dl.getParm(self.strings[-1])) # Obtain value from register, return tuple to lab PC
                
            else:
                
                return('e 2') # Variable does not exist, return error message string 
        else:
                
            print(self.strings)

            return('e 1') # Wrong command

    def Set_DPG_ctrl(self, DPG_ctrl):

        print(type(DPG_ctrl))

        Output_string = g.gv.TC_DPG.write_command(Command_Dict.Command_Dict['DPG_set_write'], int(DPG_ctrl)*100)
    
        print('Check point')

        return(Output_string)

    def Convert_to_DPG_ctrl(self):

        Ctrl_type = None

        DPG_ctrl = 0.0
            
        ph2oNeed = 0.0

        if self.dl.getParm('DPG_set')[0]!=0:

            DPG_ctrl = float(self.dl.getParm('DPG_set')[0])

            Ctrl_type = "TDPG"

            #return(DPG_ctrl)

        elif self.dl.getParm('RH_set')[0]!=0:

            #print('RH_set, SC_T, pH2O_sat = ', self.dl.getParm('RH_set')[0], self.dl.getParm('SC_T')[0], self.ph2oSat(self.dl.getParm('SC_T')[0]))

            ph2oNeed =  float(self.dl.getParm('RH_set')[0])*self.ph2oSat(self.dl.getParm('SC_T')[0])/100

            Ctrl_type = "RH"

            #print('ph2oNeed', ph2oNeed)

        elif self.dl.getParm('pH2O_set')[0]!=0:

            ph2oNeed = float(self.dl.getParm('pH2O_set')[0])

            print('ph2oNeed',ph2oNeed)

            Ctrl_type = "pH2O"

        else:

            #print('RH_set, SC_T, pH2O_sat = ', self.dl.getParm('RH_set')[0], self.dl.getParm('SC_T')[0], self.ph2oSat(self.dl.getParm('SC_T')[0]))

            ph2oNeed =  self.dl.getParm('RH_set')[0]*self.ph2oSat(self.dl.getParm('SC_T')[0])/100

            #print('ph2oNeed', ph2oNeed)

        if ph2oNeed!=0:    

            DPG_ctrl = self.dewPointTemp(ph2oNeed*self.dl.getParm('CellP')[0])

            #print('DPG_ctrl', DPG_ctrl)

        self.err = DPG_ctrl - self.dewPointTemp(self.dl.getParm('pH2O')[0]*self.dl.getParm('CellP')[0]) #Error

        self.errDot = (self.err - self.err_1) / self.deltaT     # Error derivative value
        self.err_1 = self.err                                   # Save the error value
        self.errSum += self.err                                 # Error sum value
            
        #print('DPG_ctrl', DPG_ctrl)

        print('pH2O', self.dl.getParm('pH2O')[0])

        print('DPT', self.dewPointTemp(self.dl.getParm('pH2O')[0]*self.dl.getParm('CellP')[0]))

        print('Error', self.err)

        #print('Error derivative', self.errDot)

        #print('Error sum', self.errSum)

        self.DPG_ctrl = (self.dl.getParm('pH2O_P')[0]*self.err + self.dl.getParm('pH2O_D')[0]*self.errDot + self.dl.getParm('pH2O_I')[0]*self.errSum)

        # Now, we need the limiter
        limit = min(self.dl.getParm('SC_T')[0], self.dl.getParm('CC_T')[0])
        if self.DPG_ctrl > limit :
            self.DPG_ctrl = limit
        return self.DPG_ctrl

    def ph2oSat(self, T) :
            
        return 610.78 * exp((T * 17.2684) / (T + 238.3))

    def dewPointTemp(self, ph2o) :
        w = log(ph2o / 610.78)
        return w * 238.3 / (17.294 - w)

