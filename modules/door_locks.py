#=======================================
# Imports
#=======================================

import RPi.GPIO as GPIO
import time


#========================================
# Definitions / Constants
#========================================

LOCK_BUTTON = 5
LOCK_RELAY = 17
LOCK_PULSE = 0.25

#=========================================
# Varibales
#=========================================

last_button = False
door_locked = False

#=======================================
# GPIO Setup
#=======================================

GPIO.setmode(GPIO.BCM)

GPIO.setup(LOCK_BUTTON, GPIO.IN)
GPIO.setup(LOCK_RELAY, GPIO.OUT)

GPIO.output(LOCK_RELAY, False)

#======================================
# Functions
#======================================

def lock_doors():
	GPIO.output(LOCK_RELAY, True)
	time.sleep(LOCK_PULSE)
	GPIO.output(LOCK_RELAY, False)

#======================================
# Main Loop
#======================================

while True:

	button = GPIO.input(LOCK_BUTTON)

	if button and not last_button:

		lock_doors()

	last_button = button
