# sudo apt install mpv socat
# pip install umodbus

# mkdir -p /home/ascon/.config/autostart
# nano /home/ascon/.config/autostart/acson.desktop

# [Desktop Entry]
# Type=Application
# Name=Ascon
# Exec=/usr/bin/python3 /home/ascon/factory-mockup/ascon_2.py

import time
import socket
import logging
import subprocess

from umodbus import conf
from umodbus.client import tcp

from itertools import cycle
from random import randint
from logging.handlers import RotatingFileHandler

from gpiozero import Button
from gpiozero import LEDBoard

DELAY = 5
MODBUS_IP = '192.168.1.53'
MODBUS_PORT = 5020

# Настройка логирования.
logging.basicConfig(
    handlers=[
        RotatingFileHandler(
            # '/home/ascon/factory-mockup/logs/mockup.log',
            'logs/mockup.log',
            maxBytes=100000,
            backupCount=50
        )
    ],
  level=logging.INFO,
  format='%(asctime)s %(levelname)s PID %(process)d %(message)s'
)

# Настройка кнопок.
button_1 = Button(17)
button_2 = Button(4)
button_3 = Button(3)
button_4 = Button(2)

# Настройка светодиодов.
leds = LEDBoard(14, 15, 18, 23, 24, 25, 8, 7, 12, 6, 5, 11, 9, 10, 22, 27)
leds.value = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

# Перебираемые видеоролики.
videos = cycle((1, 2, 3, 4))


def start_player():
    logging.info('Start player')
    try:
        subprocess.Popen([
            'nohup',
            'mpv',
            '--hwdec=mmal',
            '--audio-device=alsa/hdmi:CARD=vc4hdmi0,DEV=0',
            '--playlist=/home/ascon/factory-mockup/video/all-2.pls',
            '--fullscreen',
            '--script-opts=osc-showfullscreen=no',
            '--loop-playlist=inf',
            '--input-ipc-server=/tmp/mpvsocket'
        ], close_fds=False)
    except Exception as ex:
        logging.error('Exception occurred', exc_info=True)

    
def play_video(filename):
    logging.info(f'Playing video file {filename}')
    try:
        echo = subprocess.Popen(
            ['echo', f'loadfile /home/ascon/factory-mockup/video/{filename}'],
            stdout=subprocess.PIPE, 
            text=True
        )
        socat = subprocess.Popen(
            ['socat', '-', '/tmp/mpvsocket'],
            stdin=echo.stdout,
            stdout=subprocess.PIPE, 
            text=True
        )
        socat.communicate()
    except Exception as ex:
        logging.error('Exception occurred', exc_info=True)

def send_data(data, slave_id=1, address=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((MODBUS_IP, MODBUS_PORT))
        message = tcp.write_single_register(
            slave_id=slave_id,
            address=address, 
            value=data
        )
        response = tcp.send_message(message, sock)
        logging.info(f'Receive response from modbus server: {response}')

    except Exception as ex:
        logging.error('Exception occurred', exc_info=True)
    finally:
        sock.close()



def main():
    # start_player()
    delay = DELAY    

    while True:
        if button_1.is_pressed:
            print(f'send 111')
            if delay:
                delay -= 1
            else:
                # play_video(f'{next(videos)}.mp4')
                delay = DELAY

        if button_2.is_pressed:
            print(f'send 1')
            send_data(data=randint(20, 150), address=1)
            print(f'send 2')
            send_data(data=randint(200, 1000), address=2)
            print(f'send 3')
            send_data(data=randint(75, 95), address=3)
            
            leds.value = (0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
            
        if button_3.is_pressed:
            send_data(data=randint(1000, 10000), address=4)
            send_data(data=randint(2000, 3000), address=5)
            send_data(data=randint(0, 10), address=6)
            leds.value = (1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1)
            
        if button_4.is_pressed:
            send_data(data=randint(1, 50), address=7)
            send_data(data=randint(-100, 100), address=8)
            leds.value = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0)
            
        time.sleep(0.05)


if __name__ == '__main__':
    main()