import random
import time
import mpv
import requests

from PIL import Image, ImageDraw, ImageFont

BASE_URL = 'https://fakestoreapi.com'

player = mpv.MPV(
    ytdl=True,
    input_default_bindings=True,
    input_vo_keyboard=True
)

for idx in range(1, 6):
    player.playlist_append(f'video/{idx}.mp4')

player.loop_playlist = 'inf'
player.playlist_pos = 0

player.wait_until_playing()
player.keypress('f')

while True:
    overlay = player.create_image_overlay()

    rnd_time = random.randint(2, 16)
    rnd_index = random.randint(0, 4)
    rnd_json = random.randint(0, 19)
    
    # time.sleep(rnd_time)

    response = requests.get(f'{BASE_URL}/products')
    data = response.json()
    url_str = data[rnd_json]['price']

    if not player.core_idle:
        overlay.remove()

        img = Image.new(
            'RGBA', 
            (1000, 150), 
            (255, 255, 255, 0)
        ) 
        d = ImageDraw.Draw(img)
        d.text(
            (10, 10), 
            f'rnd_time: {rnd_time}, rnd_index: {rnd_index}, url_str: {url_str}', 
            font=ImageFont.truetype('DejaVuSans.ttf', 40), 
            fill=(0, 255, 255, 128)
        )

        overlay.update(img, pos=(400, 400))
    
    if url_str == 39.99:
        player.playlist_play_index(rnd_index)