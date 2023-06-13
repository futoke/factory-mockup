import time
import random
import socket
import logging
import subprocess

from logging.handlers import RotatingFileHandler

from umodbus import conf
from umodbus.client import tcp

MODBUS_IP = 'localhost'
MODBUS_PORT = 5020

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

# Настройка modbus.
conf.SIGNED_VALUES = True


def start_player():
    logging.info('Start player')
    try:
        subprocess.Popen([
            'mpv',
            '--playlist=video/all.pls',
            '--fullscreen',
            '--script-opts=osc-showfullscreen=no',
            '--loop-playlist=inf',
            '--input-ipc-server=/tmp/mpvsocket'
        ])
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
        rnd_num = random.randint(1, 5)
        
        play_video(f'{rnd_num}.mp4')
        send_data(rnd_num)

        time.sleep(8)


if __name__ == '__main__':
    main()