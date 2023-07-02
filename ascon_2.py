# sudo apt install mpv socat
import time
import random
import logging
import subprocess

from logging.handlers import RotatingFileHandler

from gpiozero import Button
from gpiozero import LEDBoard

# Настройка логирования.
logging.basicConfig(
    handlers=[
        RotatingFileHandler(
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
leds.value = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

def start_player():
    logging.info('Start player')
    try:
        subprocess.Popen([
            'nohup',
            'mpv',
            '--hwdec=v4l2m2m',
            '--playlist=video/all-2.pls',
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
            ['echo', f'loadfile video/{filename}'],
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
            leds.value = (1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            
        if button_3.is_pressed:
            leds.value = (0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0)
            
        if button_4.is_pressed:
            leds.value = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1)
            

        time.sleep(0.05)


if __name__ == '__main__':
    main()