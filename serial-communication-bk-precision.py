# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 15:08:33 2015

@author: termodinamica
"""
import matplotlib.pyplot as pyplot
import time
import serial
import re

# create new blank file
record = open('record.txt', 'w')

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate=19200, # default: 9600
	parity=serial.PARITY_ODD,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

if(ser.isOpen() == False):
    ser.open()

#ser.open()
#ser.isOpen()
print '\n'
print 'Enter your commands below.\r\nInsert "exit" to leave the application.'
print 'Enter "stream" to start streaming from multimeter.'

numList = []
powList = []
timeData = []
sleep = 0.4

input=1
while 1 :
	# get keyboard input
    input = raw_input(">> ")
        # Python 3 users
        # input = input(">> ")
    if input == 'exit':
		ser.close()
		exit()
    elif input == 'stream':
        out = ''   
        t = 0
        for x in range(0, 160):
          ser.write(':fetch?\n')   
          out = ''
          time.sleep(sleep)
          
          while ser.inWaiting() > 0:
			out += ser.read(1)
                   
          if out != '':
              sout = re.split('\s+', out) # Separates ':fetch?' from reading
              formatSout = sout[1].split('e') # Splits reading ####e## around 'e'
              num = float(formatSout[0]) # Stores the num before power              
              time.sleep(1)
              power = int(formatSout[1]) # Stores the power              
              t += sleep # Each reading is measured each 0.3 s
          
          numList.append(num) 
          powList.append(power)
          timeData.append(t)
         # print(out)
          
          record.writelines(sout[1] + '\n') 
          #print(sout[1])
          print(str(t) + ': ' + str(num) + ' x10 ' + str(power))
        record.close()
    else:
		# send the character to the device
		# (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
		ser.write(input + '\n')
		out = ''
		# let's wait one second before reading output (let's give device time to answer)
		time.sleep(1)
		while ser.inWaiting() > 0:
			out += ser.read(1)
			
		if out != '':
			print ">>" + out