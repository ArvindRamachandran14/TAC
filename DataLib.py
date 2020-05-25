
# -*- coding: utf-8 -*-

""" DataLib.py

        Adapted from  Original issue - 03/12/2019 - KDT
"""

import time 

import datetime

class Register():
    def __init__(self, _i, _n, _v, _ts):
        self.index  = _i
        self.name = _n
        self.value = _v
        self.time_stamp = _ts

class DataLib():

    # Controller data manager

    def __init__(self):
        
        # Thermocouples

        init_ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        self.SC_T = Register(1, 'SC_T', 0.0, init_ts) #Temperature inside the sample chamber
        self.SC_Tblock = Register(2, 'SC_Tblock', 0.0, init_ts) # Temperature of the temperature block /gas pre heater
        self.CC_T = Register(3, 'CC_T', 0.0, init_ts) 
        self.DPG_T = Register(4, 'DPG_T', 0.0, init_ts) #Set point temperature of the dew point generator
        #Temperature of the conditioning chamber

        # Setpoints
        self.SC_set = Register(5, 'SC_set', 0.0, init_ts) #Sample chamber temp controller set point
        self.DPG_set = Register(6, 'CC_set', 0.0, init_ts) #Conditioning chamber temp controller set point
        self.CC_set = Register(7, 'DPG_set', 0.0, init_ts) #Dew point generator temp controller set point

        # SC paramters
        self.SC_P = Register(8, 'SC_P', 0.0, init_ts) #Sample chamber temp controller proportional gain
        self.SC_I = Register(9, 'SC_I', 0.0, init_ts) #Sample chamber temp controller integral gain
        self.SC_D = Register(10, 'SC_D', 0.0, init_ts) #Sample chamber temp controller differential gain
        self.SC_power = Register(11, 'SC_power', 0.0, init_ts) #Sample chamber temp controller differential gain
        self.SC_output = Register(12, 'SC_output', 0.0, init_ts) #Sample chamber temp controller differential gain

        #CC parameters

        self.CC_P = Register(13, 'CC_P', 0.0, init_ts) #Conditioning chamber temp controller proportional gain
        self.CC_I = Register(14, 'CC_I', 0.0, init_ts) #Conditioning chamber temp controller proportional gain
        self.CC_D = Register(15, 'CC_D', 0.0, init_ts) #Conditioning chamber temp controller proportional gain
        self.CC_power = Register(16,'CC_power', 0, init_ts)
        self.CC_output = Register(17,'CC_output', 0.0, init_ts)

        self.DPG_P = Register(18, 'DPG_P', 0.0, init_ts) #DPG  temp controller proportional gain
        self.DPG_I = Register(19, 'DPG_I', 0.0, init_ts) #DPG  temp controllerintegral gain
        self.DPG_D = Register(20, 'DPG_D', 0.0, init_ts) #DPG  temp controller differential gain
        self.DPG_power = Register(21,'DPG_power', 0, init_ts)
        self.DPG_output = Register(22,'DPG_output', 0.0, init_ts)

        # IRGA
        self.CellP = Register(23,'CellP', 0.0, init_ts) #Cell Pressure
        self.CellT = Register(24,'CellT', 0.0, init_ts) # Cell Temp
        self.IVOLT = Register(25, 'IVOLT', 0.0, init_ts) # Voltage supplied to IRGA
        self.pH2O = Register(26, 'pH2O', 0.0, init_ts)    # Partial pressure H20 (Pa)
        self.pCO2 = Register(27, 'pCO2', 0.0, init_ts)   # Partial pressure CO2 (Pa)
        self.DPT = Register(28, 'DPT', 0.0, init_ts)

        #Others
        self.WGT = Register(29, 'WGT', 0.0, init_ts) #Weight of the sample
        self.ByPass = Register(30, 'ByPass',0.0, init_ts) #Desired valve state – bypass/norma

        #Status 

        self.Status = Register(31, "Status", 0, init_ts)

        # The parameter dictionary with register objects
        self.parmDict = {
            self.SC_T.name : self.SC_T,
            self.SC_Tblock.name : self.SC_Tblock, 
            self.DPG_T.name : self.DPG_T,
            self.CC_T.name :  self.CC_T,
            self.SC_set.name : self.SC_set,
            self.CC_set.name: self.CC_set,
            self.DPG_set.name: self.DPG_set,
            self.SC_P.name : self.SC_P, 
            self.SC_I.name : self.SC_I,
            self.SC_D.name : self.SC_D,
            self.SC_power.name : self.SC_power,
            self.SC_output.name : self.SC_output,
            self.DPG_P.name : self.DPG_P, 
            self.DPG_I.name : self.DPG_I,
            self.DPG_D.name : self.DPG_D,
            self.CC_power.name: self.CC_power,
            self.CC_output.name: self.CC_output,
            self.CC_P.name : self.CC_P, 
            self.CC_I.name : self.CC_I,
            self.CC_D.name : self.CC_D,
            self.DPG_power.name : self.DPG_power,
            self.DPG_output.name : self.DPG_output,
            self.CellP.name: self.CellP,
            self.CellT.name: self.CellT,
            self.IVOLT.name: self.IVOLT,
            self.pH2O.name: self.pH2O,
            self.pCO2.name: self.pCO2,
            self.DPT.name: self.DPT,
            self.WGT.name: self.WGT,
            self.ByPass.name: self.ByPass,
            self.Status.name: self.Status
        }

    def getParmDict(self):
        
        return self.parmDict

    def get_all_data(self):

        ######### Function to get all the data at once from TA #########

        all_data_dict = {}

        string = ""

        for key in ['SC_T', 'SC_Tblock', 'CC_T', 'DPG_T', 'pH2O', 'pCO2', 'DPT', 'WGT', 'Status']:

            string += str(self.parmDict[key].value) 

            string += ','

        return(string)

    def setParm(self, key, value, time_stamp):
        ######### Function to set a certain system variable's value #########
        if key in self.parmDict:
            self.parmDict[key].value = value
            self.parmDict[key].time_stamp = time_stamp
            return True
        else:
            return False

    def getParm(self, key):
        ######### Function to get a certain system variable's value #########
        if key in self.parmDict:
            value = self.parmDict[key].value
            time_stamp = self.parmDict[key].time_stamp
        else:
            value = float('NaN')
            time_stamp = 'NaN'
        return value, time_stamp

    def parmName(self, key):
        ######### Function to get a certain system variable's name #########
        if key in self.parmDict:
            name = self.parmDict[key].name
        else:
            name = ''
        return name
