# -*- encoding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.IN)


while True:
    GPIO.setup(26, GPIO.OUT)
    GPIO.output(26, True)
	



"""
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install build-essential git cmake libqt4-dev libphonon-dev python2.7-dev libxml2-dev libxslt1-dev qtmobility-dev python-pip moc libjpeg-dev vlc python-pyside










"""
