from gtts import gTTS
import json
import os
import _thread
import time

id = ''
n_threads = 1

def save_audio(text, filename):
    language = 'en-ca'
    tts = gTTS(text=text, lang=language, slow=False)

    path = 'data/' + id + '/audio/'
    if not os.path.exists(path):
        os.makedirs(path)
    tts.save(path + filename)

def save_post(post):
    text = post['title']
    filename = 'post.mp3'
    save_audio(text, filename)
    print('[Info] Post audio saved')

def save_comments(comments, done, c, length):
    for comment in comments:
        i = comment['_id']
        text = comment['text']
        filename = 'comment_' + str(comment['_id']) + '.mp3'
        save_audio(text, filename)
        print('[Info] Comment audio saved (' + str(int(i) + 1) + '/' + str(length) + ')')
    
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

    save_post(data['post'])
    multithread(save_comments, n_threads, data['comments'])
    
    return True