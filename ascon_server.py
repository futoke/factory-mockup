import sqlite3

from socketserver import TCPServer

from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server

# MODBUS_IP = '192.168.11.11'
MODBUS_IP = '192.168.0.5'
MODBUS_PORT = 5020
# PREFIX = '/home/ascon/factory-mockup'
PREFIX = '/home/ichiro/factory-mockup'

conf.SIGNED_VALUES = True
TCPServer.allow_reuse_address = True
app = get_server(TCPServer, (MODBUS_IP, MODBUS_PORT), RequestHandler)


def get_data_from_db():
    data = []
    try:
        con = sqlite3.connect(f'{PREFIX}/exchange.db')

        cursor = con.cursor()
        cursor.execute('SELECT * FROM registers')

        data = cursor.fetchone()
    except Exception as ex:
        print(ex.args)
    finally:
        con.close()

    return data


@app.route(slave_ids=[1], function_codes=[3, 4], addresses=list(range(40001, 40009)))
def read_data(slave_id, function_code, address):
    data = get_data_from_db()
    return data[address]


if __name__ == '__main__':
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()