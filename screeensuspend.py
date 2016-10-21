import pdb
import RPi.GPIO as GPIO
import time
import subprocess
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#zet de laatste tijd het scherm aan en de timeout
lastMotion=time.time()
schermAan=True
timeOut=60
#publish.single("huis/gang/pir", "script started", hostname="localhost")

def printFunction(channel):
 print("scherm aan")
 global lastMotion
 global schermAan
 publish.single("huis/gang/pir", "motion", hostname="localhost")
 print("motion")
 lastMotion=time.time()
 if(schermAan==False):
  schermAan=True
  subprocess.call(["/usr/bin/tvservice","-p"])
  subprocess.call(["/usr/bin/xset","-dpms -force on"])

GPIO.add_event_detect(23, GPIO.RISING, callback=printFunction, bouncetime=300)

while True:
 if((time.time()-lastMotion>timeOut) and schermAan==True):
  print("scherm uit")
  schermAan=False
  publish.single("huis/gang/pir", "scherm uit", hostname="localhost")
  subprocess.call(["/usr/bin/tvservice","-o"])
 print("scherm: "+str(schermAan)+" timer: "+str(time.time()-lastMotion))
 time.sleep(2)
GPIO.cleanup()
