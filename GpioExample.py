from neo import Gpio # import Gpio library
from time import sleep # import sleep to wait for blinks

neo = Gpio() #create new Neo object

pinOne = 25 #pin to use

neo.pinMode(pinOne, neo.OUTPUT)# Use innerbank pin 2 and set it as output either 0 (neo.INPUT) or 1 (neo.OUTPUT)

#Blink example
while True: #Do for five times
	neo.digitalWrite(pinOne,neo.HIGH) #write high value to pin
	sleep(1)# wait one second
	neo.digitalWrite(pinOne,neo.LOW) #write low value to pin
	sleep(1)# wait one second