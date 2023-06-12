import random
import subprocess
import time


subprocess.Popen([
    'mpv',
    '--playlist=video/all.pls',
    '--fullscreen',
    '--script-opts=osc-showfullscreen=no',
    '--loop-playlist=inf',
    '--input-ipc-server=/tmp/mpvsocket'
])

while True:
    rnd_num = random.randint(1, 5)

    echo = subprocess.Popen(
        ['echo', f'loadfile video/{rnd_num}.mp4'],
        stdout=subprocess.PIPE, 
        text=True
    )
    socat = subprocess.Popen(
        ['socat', '-', '/tmp/mpvsocket'],
        stdin=echo.stdout,
        stdout=subprocess.PIPE, 
        text=True
    )
    socat.communicate()
    time.sleep(8)

# mpv --playlist=video.pls --loop-playlist=inf --input-ipc-server=/tmp/mpvsocket
# echo 'show-text ${playback-time}' | socat - /tmp/mpvsocket
