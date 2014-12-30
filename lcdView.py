#!/usr/bin/python
# A script to output the last heard callsign of the DVAP
# Based on code from the Radio Pi project at http://usualpanic.com and
#  Adafruit.
# You'll also need Tailer to be install into python https://pypi.python.org/pypi/tailer
# Greyions 2014-12-27

import math
import time
import tailer
import sys
import os
import threading
from threading	import Thread
from subprocess	import *
from datetime	import datetime
from time	import sleep, strftime

import Adafruit_CharLCD as LCD

# Initalize the LCD using the pins
lcd = LCD.Adafruit_CharLCDPlate()

# Set the background color
#lcd.set_color(0,0,1) # Blue
lcd.set_color(1,0,0) # Red
#lcd.set_color(0,1,0) # Green
#lcd.set_color(1,1,0) # Yellow
#lcd.set_color(1,0,1) # Magenta
#lcd.set_color(1,1,1) # White
lcd.clear()

def tailFile():
	for line in tailer.follow(open('/var/log/gateway/Headers.log')):
		s = line
		a = s.split()
		#print a[6:8]
		z = a[6:8]
		str = " ";
		y = str.join(z)
		lcd.clear()
		lcd.message('Station Heard\n' + y)

def btnPress():
	btn = ((LCD.SELECT, 'Select', (0,0,1)),
		(LCD.LEFT, 'Left', (0,0,1)),
		(LCD.UP, 'Up', (0,0,1)),
		(LCD.DOWN, 'Down', (0,0,1)),
		(LCD.RIGHT, 'Right', (0,0,1)))

	while True:
		for b in btn:
			if lcd.is_pressed(b[0]):
				#lcd.clear()
				#lcd.message(b[1])
				ab = b[0] 
				# Button definitions 
				# Select = 0
				# Left = 4
				# Right = 1
				# Up = 3
				# Down = 2
				if ab == 0: # Select button Pressed
					lcd.clear()
					lcd.set_backlight(0)
					exit()
				if ab == 1: # Right button pressed
					lcd.clear()
				if ab == 3: # Up button pressed
					lcd.clear()
					display_ipaddr()
					sleep(5)
					lcd.clear()
					lcd.message('Time\n' + datetime.now().strftime('%b %d  %H:%M'))

def display_ipaddr():
	show_wlan0 = "ip addr show wlan0 | cut -d/ -f1 | awk '/inet/ {printf \"w%15.15s\", $2}'"
   	show_eth0  = "ip addr show eth0  | cut -d/ -f1 | awk '/inet/ {printf \"e%15.15s\", $2}'"
   	ipaddr = run_cmd(show_eth0)
   	if ipaddr == "":
		ipaddr = run_cmd(show_wlan0)
	lcd.message('IP address\n' + ipaddr)

def run_cmd(cmd):
   p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
   output = p.communicate()[0]
   return output

if __name__ == '__main__':
	t = Thread(target = tailFile)
	t.setDaemon(True)
	t.start()

btnPress()
