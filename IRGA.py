
#IRGA module - 

import serial

import time 

import datetime

import re

import xml.etree.ElementTree as ET


class IRGA():

    def __init__(self, ser):

        # When an instance of this class is created, the serial port is initialized and the OUTRATE is set to zero

        # This makes sure the IRGA only sends values when requested

        #self.ser.write('<LI840> <CFG> <OUTRATE>0</OUTRATE> </CFG> <RS232> <STRIP>FALSE</STRIP> <ECHO>FALSE</ECHO> <CELL TEMP>TRUE</CELL TEMP> <CO2>TRUE</CO2> <CO2ABS>FALSE</CO2ABS> <H2O>TRUE</H2O> <H2OABS>FALSE</H2OABS> <CELLPRES>TRUE</CELLPRES> <IVOLT>TRUE</IVOLT> </RS232> </LI840>')
        
        self.ser = ser
        
        #self.string = '<LI840><CFG><OUTRATE>0</OUTRATE></CFG><RS232><STRIP>FALSE</STRIP><ECHO>FALSE</ECHO><CELL TEMP>TRUE</CELL TEMP><CO2>TRUE</CO2><CO2ABS>FALSE</CO2ABS><CELLPRES>TRUE</CELLPRES><IVOLT>TRUE</IVOLT></RS232></LI840'
        
        #self.string = '<LI840> <CFG> <OUTRATE> 0 </OUTRATE> </CFG> </LI840>'
        
        #self.string_as_bytes = self.string.encode()
        
        #self.ser.write(self.string_as_bytes)
        
        self.ser.write('<LI840> <CFG> <OUTRATE> 0 </OUTRATE> </CFG> </LI840>'.encode()) #Set the OUTRATE to 0
        
        self.xmlstring = self.ser.readline().decode() 
	
        self.ser.write('<LI840><DATA>?</DATA></LI840>'.encode())

        self.return_list = []

    def read_IRGA(self):
        
        self.return_list = []

        #self.ser.reset_input_buffer()

        #self.ser.reset_output_buffer()

        self.xmlstring = self.ser.readline().decode() # Reading the output as an XML string 

        self.ser.write('<LI840><DATA>?</DATA></LI840>'.encode()) #Command to request output from IRGA

        #self.xmlstring = re.search('<li840>(.*)</li840>',self.xmlstring).group(0)
        
        #print('xml string is ', self.xmlstring)
        
        self.root = ET.fromstring(self.xmlstring)
        
        #print(self.root)

        #################### Add IRGA output to the return list #################### 
            
        self.return_list.append(float(self.root[0].find('co2').text))

        self.return_list.append(float(self.root[0].find('h2o').text))

        self.return_list.append(float(self.root[0].find('cellpres').text))

        self.return_list.append(float(self.root[0].find('celltemp').text))

        self.return_list.append(float(self.root[0].find('ivolt').text))

        self.return_list.append(float(self.root[0].find('h2odewpoint').text))
            
        return(self.return_list)
