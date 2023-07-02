# sudo apt install mpv socat

# mkdir -p /home/ascon/.config/autostart
# nano /home/ascon/.config/autostart/acson.desktop

# [Desktop Entry]
# Type=Application
# Name=Ascon
# Exec=/usr/bin/python3 /home/ascon/factory-mockup/ascon_1.py

import time
import random
import logging
import subprocess

from logging.handlers import RotatingFileHandler

from gpiozero import Button
from gpiozero import LEDBoard

BOUNCE_TIME = 0.2

# Настройка логирования.
logging.basicConfig(
    handlers=[
        RotatingFileHandler(
            '/home/ascon/factory-mockup/logs/mockup.log',
            maxBytes=100000,
            backupCount=50
        )
    ],
  level=logging.INFO,
  format='%(asctime)s %(levelname)s PID %(process)d %(message)s'
)

# Настройка кнопок.
button_1 = Button(2, bounce_time=BOUNCE_TIME)
button_2 = Button(3, bounce_time=BOUNCE_TIME)
button_3 = Button(4, bounce_time=BOUNCE_TIME)
button_4 = Button(17, bounce_time=BOUNCE_TIME)
button_5 = Button(27, bounce_time=BOUNCE_TIME)
button_6 = Button(22, bounce_time=BOUNCE_TIME)
button_7 = Button(10, bounce_time=BOUNCE_TIME)
button_8 = Button(9, bounce_time=BOUNCE_TIME)

# Настройка светодиодов.
leds = LEDBoard(14, 15, 18)
leds.value = (1, 0, 0)


def start_player():
    logging.info('Start player')
    try:
        subprocess.Popen([
            'nohup',
            'mpv',
            # '--hwdec=v4l2m2m',
            '--hwdec=mmal',
            '--audio-device=alsa/hdmi:CARD=vc4hdmi0,DEV=0',
            '--playlist=/home/ascon/factory-mockup/video/all-1.pls',
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


def main():
    start_player()

    while True:
        if button_1.is_pressed:
            leds.value = (1, 0, 0)
            play_video('1.mp4')

        if button_2.is_pressed:
            leds.value = (0, 1, 0)
            play_video('2.mp4')

        if button_3.is_pressed:
            leds.value = (1, 0, 0)
            play_video('3.mp4')

        if button_4.is_pressed:
            leds.value = (0, 1, 0)
            play_video('4.mp4')

        if button_5.is_pressed:
            leds.value = (0, 0, 1)
            play_video('5.mp4')

        if button_6.is_pressed:
            leds.value = (0, 0, 1)
            play_video('6.mp4')

        if button_7.is_pressed:
            leds.value = (0, 0, 1)
            play_video('7.mp4')

        if button_8.is_pressed:
            leds.value = (0, 0, 1)
            play_video('8.mp4')

        time.sleep(0.05)


if __name__ == '__main__':
    main()