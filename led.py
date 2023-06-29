from gpiozero import LED
from time import sleep


while True:
    for led_num in range(2, 27):
        led = LED(led_num)
        led.on()

        print('NYAAA')
        sleep(1)
