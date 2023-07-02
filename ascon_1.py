import time
import random
import logging
import subprocess

from logging.handlers import RotatingFileHandler
from gpiozero import Button


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
button_1 = Button(2)
button_2 = Button(3)
button_3 = Button(4)
button_4 = Button(17)
button_5 = Button(27)
button_6 = Button(22)
button_7 = Button(10)
button_8 = Button(9)


def start_player():
    logging.info('Start player')
    try:
        subprocess.Popen([
            'nohup',
            'mpv',
            '--hwdec=v4l2m2m',
            '--playlist=video/all.pls',
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
    # start_player()

    while True:
        if button_1.is_pressed:
            print('Button 1 is pressed')
            continue
        if button_2.is_pressed:
            print('Button 2 is pressed')
            continue
        if button_3.is_pressed:
            print('Button 3 is pressed')
            continue
        if button_4.is_pressed:
            print('Button 4 is pressed')
            continue
        if button_5.is_pressed:
            print('Button 5 is pressed')
            continue
        if button_6.is_pressed:
            print('Button 6 is pressed')
            continue
        if button_7.is_pressed:
            print('Button 7 is pressed')
            continue
        if button_8.is_pressed:
            print('Button 8 is pressed')
            continue
            # play_video(f'{rnd_num}.mp4')
        time.sleep(0.05)


if __name__ == '__main__':
    main()