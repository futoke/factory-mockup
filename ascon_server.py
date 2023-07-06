import sqlite3
import logging

from logging.handlers import RotatingFileHandler
from socketserver import TCPServer

from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server

MODBUS_IP = '192.168.11.11'
# MODBUS_IP = '192.168.0.5'
MODBUS_PORT = 5020
PREFIX = '/home/ascon/factory-mockup'
# PREFIX = '/home/ichiro/factory-mockup'

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

conf.SIGNED_VALUES = True
TCPServer.allow_reuse_address = True
app = get_server(TCPServer, (MODBUS_IP, MODBUS_PORT), RequestHandler)


def get_data_from_db():
    data = [0, 0, 0, 0, 0, 0, 0, 0]
    try:
        con = sqlite3.connect(f'{PREFIX}/exchange.db')

        cursor = con.cursor()
        cursor.execute('SELECT * FROM registers')

        data = cursor.fetchone()
    except Exception as ex:
        logging.error('Exception occurred', exc_info=True)
    finally:
        con.close()

    return data

def clear_db():
    try:
        con = sqlite3.connect(f'{PREFIX}/exchange.db')

        cursor = con.cursor()
        for reg in range(1, 9):
            cursor.execute(f'UPDATE registers SET reg{reg} = 0 where id = 1')
        
        con.commit()
    except Exception:
        logging.error('Exception occurred', exc_info=True)
    finally:
        con.close()


@app.route(slave_ids=[1], function_codes=[3, 4], addresses=list(range(1, 9)))
def read_data(slave_id, function_code, address):
    data = get_data_from_db()
    return data[address]


if __name__ == '__main__':
    clear_db()
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()