# BYU-Idaho
# ECEN 361 - 6 July 2017
# YellowStone Bear World Bear Den Camera
# Troy Christensen, Daniel Martin, Tim Whitlock


# Import GPIO, time, serial, sys libraries
import RPi.GPIO as GPIO  
import time
import serial
import sys

# Set GPIO mode to BCM (Broadcom port numbering)
GPIO.setmode(GPIO.BCM)  


# Class Controller - Used to communicate to USB Servo Controller board
#					 by way of serial communication. Sets min and max angles 
#                    for set amount of servos used.
class Controller:
	def __init__(self,port= "/dev/ttyACM0"):
		self.ser = serial.Serial(port = port)
	def setAngle(self,channel, angle):
		minAngle = 0.0
		maxAngle = 180.0
		minTarget = 256.0
		maxTarget = 13120.0
		scaledValue = int((angle / ((maxAngle - minAngle) / (maxTarget - minTarget))) + minTarget)
		commandByte = chr(0x84)
		channelByte = chr(channel)
		lowTargetByte = chr(scaledValue & 0x7F)
		highTargetByte = chr((scaledValue >> 7) & 0x7F)
		command = commandByte + channelByte + lowTargetByte + highTargetByte
		self.ser.write(command)
		self.ser.flush()
	def close(self):
		self.ser.close()


# Set up the pinouts on Raspberry Pi for PIR sensor inputs
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
  
# Instantiate controller class as control variable
control = Controller()



# Define function for my_callback - Function for 1st PIR sensor
# on BCM pin 17 on Pi
def my_callback(channel):  
    
    # When 1st PIR sensor detects, print right movment to user
    print "Right Movement Detected" 
    
    # Linear servo = channel 5. Servo motor = channel 4 of USB servo 
    # controller board. 2nd argument in setAngle() = degree movement 
    # of servo. Any channel can be used for future modifications
    # Linear servo = all in, Servo moter = looking right
    control.setAngle(5,0)
    GPIO.remove_event_detect(17) # Remove the interrupt from the Pi
    time.sleep(.5)				 # Delay for 1/2 sec
    
    control.setAngle(4,0)
    GPIO.remove_event_detect(17) # Remove the interrupt from the Pi	
    time.sleep(.5)				 # Delay for 1/2 sec
    
    # Interupt for 1st PIR sensor using callbacks
    GPIO.add_event_detect(17, GPIO.RISING, callback=my_callback)
    

# Define function for my_callback2 - Function for 2nd PIR sensor
# on BCM pin 23 on Pi
def my_callback2(channel):  
    
    # When 2nd PIR sensor detects, print center movment to user
    print "Center Movement Detected" 
    
    # Servos initialized for positions when 2nd PIR detects movement
    # Linear servo = halfway out, Servo motor = center
    control.setAngle(5,90)			
    GPIO.remove_event_detect(23)
    time.sleep(.5)
    
    control.setAngle(4,70)
    GPIO.remove_event_detect(23)
    time.sleep(.5)
    
    # Interupt for 2nd PIR sensor using callbacks
    GPIO.add_event_detect(23, GPIO.RISING, callback=my_callback2)
    

# Define function for my_callback3 - Function for 3rd PIR sensor
# on BCM pin 24 on Pi
def my_callback3(channel):
    
	# When 3rd PIR sensor detects, print left movment to user
    print "Left Movement Detected"
    
    # Servos initialized for positions when 3rd PIR detects movement
    # Linear servo = all the way out, Servo motor = looking left
    control.setAngle(5,180)
    GPIO.remove_event_detect(24)
    time.sleep(.5)
    
    control.setAngle(4,90)
    GPIO.remove_event_detect(24)
    time.sleep(.5)
    
    # Interupt for 3rd PIR sensor using callbacks
    GPIO.add_event_detect(24, GPIO.RISING, callback=my_callback3)


# Define Sensor Calibration - Calibrate sensors for 20 seconds
def sensorCal():
	
	# count in for loop
	for i in range(0,20):
		print ".",
		sys.stdout.flush()	# flush input buffer
		time.sleep(1)		# write each period at 1 sec
	else:
		print

	# Notify User that sensors are ready
	print("Sensor's Ready" + "\n")

  
##################################-BEGIN PROGRAM-#################################

# PRINT NEW LINE
print("\n")

# Notify user of calibration
print("Calibrating PIR Sensors for 20 seconds")

# Call sensorCal to calibrate sensors
sensorCal()

# Wait for user to press enter before program exe
raw_input("Press Enter When Ready >") 

# Call interupts with callbacks for each of the sensors
# BCM pin 17 = Right Sensor, BCM pin 23 = Center Sensor, BCM pin 24 = Left Sensor
GPIO.add_event_detect(17, GPIO.RISING, callback=my_callback)
GPIO.add_event_detect(23, GPIO.RISING, callback=my_callback2)
GPIO.add_event_detect(24, GPIO.RISING, callback=my_callback3)

# Run program until user presses ctrl + c
while True:
	pass

##################################-END PROGRAM-####################################