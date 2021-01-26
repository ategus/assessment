"""
Module Docstring
"""

__author__ = "Ronny Schellenberg"
__version__ = "0.1.0"
__license__ = "MIT"

import click
import RPi.GPIO as GPIO
import time
from datetime import datetime
import logging
import threading


TOGGLE_INTERVAL= 1


def log_setup():
    logging.basicConfig(format='%(message)s',filename='log.txt', level=logging.INFO)


def log_entry(gpio,state):
    now = datetime.now()
    time_stamp = now.strftime("%Y-%m-%dT%H:%M:%S gpio {} {}".format(gpio,state))
    logging.info(time_stamp)


def gpio_setup(gpio_out, gpio_in):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_out,GPIO.OUT)
    GPIO.setup(gpio_in, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)



class toggle_gpio(threading.Thread):
    
    def __init__(self, par):
        threading.Thread.__init__(self)
        self.par = par
        gpio_setup(par['output'], par['input'])
        if par['log']:
            log_setup()
            self.logged = False

    def run (self):

        while True:

            if GPIO.input(self.par['input']) == GPIO.HIGH:
                GPIO.output(self.par['output'],True)
                time.sleep(self.par['interval'])
                GPIO.output(self.par['output'],False)
                time.sleep(self.par['interval'])
                if self.par['log']:
                    if self.logged == False:
                        log_entry(self.par['input'], 'HIGH')
                        self.logged = True
            else:
                if self.par['log']: 
                    if self.logged == False:
                        log_entry(self.par['input'], 'LOW')
                        self.logged = True


def cli():

    par = {}
    par['input'] = 3
    par['output'] = 4
    par['log'] = True
    par['interval'] = TOGGLE_INTERVAL

    print("GPIOY(Input): {} \nGPIOX(Output) {}".format(par['input'],par['output']))

    toggle_thread = toggle_gpio(par)
    toggle_thread.start()



if __name__ == "__main__":
    cli()    
