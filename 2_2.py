import RPi.GPIO as GPIO
from pirc522 import RFID
import time
import sys, traceback

try:
    GPIO.setmode(GPIO.BOARD)
    greenLedPin = 11
    blueLedPin = 13
    GPIO.setup(greenLedPin, GPIO.OUT,initial=0)
    GPIO.setup(blueLedPin, GPIO.OUT,initial=0)
    RFID_UID = [170, 33, 136, 22, 21]
    rc522 = RFID()
    while True :
        rc522.wait_for_tag()
        (error, tag_type) = rc522.request()

        if not error :
            (error, uid) = rc522.anticoll()

            if not error :
                if RFID_UID == uid :
                    GPIO.output(blueLedPin, GPIO.LOW)
                    GPIO.output(greenLedPin, GPIO.HIGH)
                else :
                    GPIO.output(greenLedPin, GPIO.LOW)
                    GPIO.output(blueLedPin, GPIO.HIGH)

                time.sleep(1)

except KeyboardInterrupt:
    print("Exit pressed Ctrl+C")      
except:
    print("Other Exception")         
finally:
    GPIO.cleanup()                      
    print("End of program")     