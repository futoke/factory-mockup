import os
import random
import signal
import subprocess
import time

while True:
    rnd_num = random.randint(1, 5)

    p = subprocess.Popen([
        'mpv',
        '--fs',
        '--no-osd-bar',
        f'video/{rnd_num}.mp4'
    ])
    time.sleep(15)
    os.kill(p.pid, signal.SIGKILL)

# mpv --playlist=video.pls --loop-playlist=inf --input-ipc-server=/tmp/mpvsocket
