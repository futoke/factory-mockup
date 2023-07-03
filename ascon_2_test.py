# Это надо вставить в ascon_2.py

import sqlite3
import subprocess

from time import sleep
from random import randint


def start_server():
    subprocess.Popen([
        'py',
        'ascon_server.py'
    ], close_fds=False)
    print('Starting modbus server')
    # logging.info('Start player')
    # try:
    #     subprocess.Popen([
    #         'nohup',
    #         'mpv',
    #         '--hwdec=mmal',
    #         '--audio-device=alsa/hdmi:CARD=vc4hdmi0,DEV=0',
    #         '--playlist=/home/ascon/factory-mockup/video/all-2.pls',
    #         '--fullscreen',
    #         '--script-opts=osc-showfullscreen=no',
    #         '--loop-playlist=inf',
    #         '--input-ipc-server=/tmp/mpvsocket'
    #     ], close_fds=False)
    # except Exception as ex:
    #     logging.error('Exception occurred', exc_info=True)


def set_data_to_db(reg, data):
    try:
        con = sqlite3.connect('exchange.db')

        cursor = con.cursor()
        cursor.execute(f'UPDATE registers SET reg{reg} = {data} where id = 1')
        
        con.commit()
    except Exception as ex:
        print(ex.args)
    finally:
        con.close()


def main():
    start_server()
    
    while True:
        for reg in range(1, 9):
            set_data_to_db(reg, randint(10, 50))
        sleep(3)


if __name__ == '__main__':
    main()