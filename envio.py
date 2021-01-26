"""
envio toggle output
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
    """
    config log file
    """
    logging.basicConfig(format='%(message)s',filename='log.txt', level=logging.INFO)


def log_entry(gpio,state):
    """
    log entry for every state change of the input pin
    @type   gpio: int
    @param  gpio: number of input gpio
    @type   state: bool
    @type   state: 0 is low and 1 is hig
    """
    now = datetime.now()
    time_stamp = now.strftime("%Y-%m-%dT%H:%M:%S gpio {} {}".format(gpio,state))
    logging.info(time_stamp)


def gpio_setup(gpio_out, gpio_in):
    """
    configure GPIO Pins
    @type   gpio: int
    @param  gpio: number of input gpio
    @type   gpio: int
    @param  gpio: number of output gpio
    """

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_out,GPIO.OUT)
    GPIO.setup(gpio_in, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


class toggle_gpio_tread(threading.Thread):
    """
    tread for input/output handling
    @type  par: dictionary
    @param par: input, output, interval, log

    """
    def __init__(self, par):
        threading.Thread.__init__(self)
        self.par = par

        gpio_setup(par['output'], par['input'])
        if par['log']:
            log_setup()
            self.logged = False

    def run (self):
   
        while self.par['event'].is_set():
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


@click.command()
@click.option('-i', required=True, type=int, help='Input GPIO(GPIOY)')
@click.option('-o', required=True, type=int, help='Output GPIO(GPIOX)')
@click.option('--log',is_flag=True, help='logfile activated')
def cli(i,o,log):
    """
    operate the cli input 

    @type    i: int
    @param   i: number of input pin
    @type    o: int
    @param   o: number of output pin
    @type  log: bool
    @param log: logfile flag for input pin state, if set then log.txt will created
    """
    par = {}
    par['input'] = i
    par['output'] = o
    par['log'] = log
    par['interval'] = TOGGLE_INTERVAL
    par['event'] = threading.Event()
    par['event'].set()
    print(type(par))

    print("GPIOY(Input): {} \nGPIOX(Output): {}".format(par['input'],par['output']))

    toggle_thread = toggle_gpio_tread(par)
    toggle_thread.start()

    try:
        while 1:
            time.sleep(.1)
    except KeyboardInterrupt:
        #print("Interrupt")
        par['event'].clear()
        toggle_thread.join()
        print("program aborted by user")


if __name__ == "__main__":
    cli()    
