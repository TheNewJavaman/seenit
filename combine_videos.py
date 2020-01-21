import json
import os
from moviepy.editor import *

id = ''

def ffmpeg_concat(data, files, path):
    files = '\nfile '.join(files)
    files = 'file ' + files
    with open(path + 'files.txt', 'w') as f:
        f.write(files)

    os.system('ffmpeg -safe 0 -f concat -i ' + path + 'files.txt -y -c copy ' + path + 'final.mp4')

def ffmpeg_fade(data, files, path):
    files = ' '.join(files)

    os.system('ffmpeg-concat -t fade -d 750 -o ' + path + 'final.mp4 ' + files)

def movie_py_fade(data, files, path):
    videos = []

    for filename in files:
        clip = VideoFileClip(filename)
        videos.append(clip)

    fade_duration = 1
    videos = [clip.crossfadein(fade_duration) for clip in videos]

    final = concatenate_videoclips(videos, padding=-fade_duration)
    final.write_videofile(path + 'final.mp4')


def movie_py_concat(data, files, path):
    videos = []

    for filename in files:
        clip = VideoFileClip(filename)
        videos.append(clip)
    
    final = concatenate_videoclips(videos)
    final.write_videofile(path + 'final.mp4')

def convert_data(new_id, method, transition):
    global id
    id = new_id

    filename = 'data/' + id +'/data.json'
    with open(filename) as f:
        data = json.load(f)

    path = 'data/' + id + '/'
    files = []
    files.append(path + 'videos/post.mp4')
    if transition == 1:
        for i in range(len(data['comments'])):
            files.append('transition/transition.mp4')
            files.append(path + 'videos/comment_' + str(i) + '.mp4')
    else:
        for i in range(len(data['comments'])):
            files.append('videos/comment_' + str(i) + '.mp4')

    globals()[method](data, files, path)

    return True