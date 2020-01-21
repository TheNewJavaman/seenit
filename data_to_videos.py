import json
import os
import _thread

n_threads = 1
id = ''
files = []

def combine_data(filename):
    path = 'data/' + id + '/videos/'

    os.system('ffmpeg -loop 1 ' + \
        '-i data/' + id + '/images/' + filename + '.png ' + \
        '-i data/' + id + '/audio/' + filename + '.mp3 ' + \
        '-c:v libx264 -tune stillimage ' + \
        '-c:a aac -b:a 192k -pix_fmt yuv420p ' + \
        '-y -r 60 ' + \
        '-shortest ' + path + filename + '.mp4')

def thread_isolater(comments, done, c, length):
    path = 'videos/'
    global files

    for comment in comments:
        i = comment['_id']
        combine_data('comment_' + str(i))

    done[c] = True

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

def convert_data(new_id, new_n_threads):
    global id
    id = new_id
    global n_threads
    n_threads = new_n_threads

    filename = 'data/' + id +'/data.json'
    with open(filename) as f:
        data = json.load(f)

    path = 'data/' + id + '/videos/'
    if not os.path.exists(path):
        os.makedirs(path)

    multithread(thread_isolater, n_threads, data['comments'])
    combine_data('post')