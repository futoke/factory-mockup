# from gpiozero import LED
# from time import sleep


# while True:
#     for led_num in range(2, 27):
#         led = LED(led_num)
#         led.on()

#         print('NYAAA')
#         sleep(1)


from gpiozero import LED
from signal import pause

for led_num in range(2, 27):
    led = LED(led_num)
    led.blink()

pause()