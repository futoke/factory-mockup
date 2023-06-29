from gpiozero import LED
from time import sleep


for led_num in range(2, 27):
    led = LED(led_num)
    led.on()
