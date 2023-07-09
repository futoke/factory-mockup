# sudo apt install mpv socat
# pip install umodbus

# mkdir -p /home/ascon/.config/autostart
# nano /home/ascon/.config/autostart/acson.desktop

# [Desktop Entry]
# Type=Application
# Name=Ascon
# Exec=/usr/bin/python3 /home/ascon/factory-mockup/ascon_2.py

from signal import pause
import time
import sqlite3
import logging
import subprocess

from umodbus import conf
from umodbus.client import tcp

from itertools import cycle
from random import randint, seed
from logging.handlers import RotatingFileHandler

from gpiozero import Button
from gpiozero import LEDBoard

DELAY = 4
# PREFIX = '/home/ascon/factory-mockup'
PREFIX = '/home/ichiro/factory-mockup'

# Настройка логирования.
logging.basicConfig(
    handlers=[
        RotatingFileHandler(
            f'{PREFIX}/logs/mockup.log',
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


def start_server():
    logging.info('Start modbus server')
    try:
        subprocess.Popen([
            '/usr/bin/python3',
            f'{PREFIX}/ascon_server.py'
        ], close_fds=False)
    except Exception:
        logging.error('Exception occurred', exc_info=True)


def start_player():
    logging.info('Start video player')
    try:
        subprocess.Popen([
            'nohup',
            'mpv',
            '--hwdec=mmal',
            '--audio-device=alsa/hdmi:CARD=vc4hdmi0,DEV=0',
            f'--playlist={PREFIX}/video/all-2.pls',
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
            ['echo', f'loadfile {PREFIX}/video/{filename}'],
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
    except Exception:
        logging.error('Exception occurred', exc_info=True)


def send_data_to_db(data):
    try:
        con = sqlite3.connect(f'{PREFIX}/exchange.db')

        cursor = con.cursor()
        for reg, dt in enumerate(data):
            cursor.execute(f'UPDATE registers SET reg{reg+1} = {dt} where id = 1')
        
        con.commit()
    except Exception:
        logging.error('Exception occurred', exc_info=True)
    finally:
        con.close()


def grs():
    return randint(0, 3)


def cycle_video():
    play_video(f'{next(videos)}.mp4')


def run_cnc_group_1():
    print('group 1')
    send_data_to_db((grs(), grs(), grs(), 0, 0, 0, 0, 0))
    leds.value =    (0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)


def run_cnc_group_2():
    print('group 2')
    send_data_to_db((0, 0, 0, grs(), grs(), grs(), 0, 0))
    leds.value =    (1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1)


def run_cnc_group_3():
    print('group 3')
    send_data_to_db((0, 0, 0, 0, 0, 0, grs(), grs()))
    leds.value =    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0)


def main():
    start_server()
    start_player()

    button_1.when_pressed = cycle_video
    button_2.when_pressed = run_cnc_group_1
    button_3.when_pressed = run_cnc_group_2
    button_4.when_pressed = run_cnc_group_3

    pause()

    # delays = [DELAY, DELAY, DELAY, DELAY]

    # while True:
    #     if button_1.is_pressed:
    #         if delays[0]:
    #             delays[0] -= 1
    #         else:
    #             play_video(f'{next(videos)}.mp4')
    #             delays[0] = DELAY

    #     # Выключены -- 0, красный -- 1, желтый -- 2, зеленый -- 3
    #     if button_2.is_pressed:
    #         if delays[1]:
    #             delays[1] -= 1
    #         else:
    #             send_data_to_db((grs(), grs(), grs(), 0, 0, 0, 0, 0))
    #             leds.value =    (0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    #             delays[1] = DELAY
            
    #     if button_3.is_pressed:
    #         if delays[2]:
    #                 delays[2] -= 1
    #         else:
    #             send_data_to_db((0, 0, 0, grs(), grs(), grs(), 0, 0))
    #             leds.value =    (1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1)
    #             delays[2] = DELAY
            
    #     if button_4.is_pressed:
    #         if delays[3]:
    #                 delays[3] -= 1
    #         else:
    #             send_data_to_db((0, 0, 0, 0, 0, 0, grs(), grs()))
    #             leds.value =    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0)
    #             delays[3] = DELAY
            
    #     time.sleep(0.05)


if __name__ == '__main__':
    main()