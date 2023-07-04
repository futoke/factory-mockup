import time
import socket

from umodbus import conf
from umodbus.client import tcp

from itertools import cycle
from random import randint

MODBUS_IP = '192.168.0.5'
MODBUS_PORT = 5020


def get_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((MODBUS_IP, MODBUS_PORT))
        message = tcp.read_holding_registers(
            slave_id=1, 
            starting_address=40001,
            quantity=8
        )
        response = tcp.send_message(message, sock)
        print(response)
    except Exception as ex:
        print(f'Exception occurred {ex.args}')
    finally:
        sock.close()


def main():
    while True:
        get_data()
        time.sleep(1)


if __name__ == '__main__':
    main()