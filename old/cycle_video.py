from itertools import cycle
from time import sleep


videos = cycle((1, 2, 3, 4))

while True:
    print(f'Playing video{next(videos)}')
    sleep(0.5)