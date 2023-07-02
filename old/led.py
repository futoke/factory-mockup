# from gpiozero import LED
# from time import sleep


# while True:
#     for led_num in range(2, 27):
#         led = LED(led_num)
#         led.on()

#         print('NYAAA')
#         sleep(1)


# from gpiozero import LED
from gpiozero import LEDBoard
from signal import pause

leds = LEDBoard(14, 15, 18, 23, 24, 25, 8, 7, 12, 6, 5, 11, 9, 10, 22, 27)
leds.value = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

pause()