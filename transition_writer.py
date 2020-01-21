from PIL import Image, ImageFont, ImageDraw
import _thread
from math import *
import os

n_threads = 12
comment_text_rgb = '#acabaa'
comment_background_rgb = '#1f0f27'

def multithread(func, n_threads, arr):
    thread_arr = []
    done = []
    for i in range(n_threads):
        thread_arr.append([])
        done.append(False)
    for c, element in enumerate(arr):
        for i in range(n_threads):
            if c % n_threads == i:
                thread_arr[i].append(element)
                break
    for i in range(n_threads):
        _thread.start_new_thread(func, (thread_arr[i], done, i, len(arr)))
    while False in done:
        pass

path = 'transition/'
if not os.path.exists(path):
    os.makedirs(path)

width = 1920
height = 1080
fps = 60
duration = 1
frames = int(fps * duration)
x_range = width - 600 - 100
size = 4

for i in range(frames):
    image = Image.new('RGB', (width, height), comment_background_rgb)
    
    for j in range(100):
        x = (x_range / frames) * i + j
        y = (sin((x) / (-200 / pi)) * 150) + 580
        x += 300

        draw = ImageDraw.Draw(image)
        for xa in range(-size, size):
            for ya in range(-size, size):
                draw.point([(x + xa, y + ya)], fill=comment_text_rgb)

    image.save('transition/frame_' + str(i) + '.png', optimize=True)

os.system('ffmpeg -r ' + str(fps) + ' -f image2 -s ' + str(width) + 'x' + str(height) + ' ' + \
    '-i transition/frame_%d.png -vcodec libx264 -y -crf 15 -pix_fmt yuv420p transition/transition.mp4')