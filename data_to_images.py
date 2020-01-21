import json
import os
from PIL import Image, ImageFont, ImageDraw
import _thread

post = {}
id = ''
n_threads = 1
post_text_rgb = '#acabaa'
post_background_rgb = '#1f0f27'
comment_text_rgb = '#acabaa'
comment_background_rgb = '#1f0f27'

def text_wrap(text, font, max_width):
    lines = []
    text = text \
        .replace('\n', ' \n ') \
        .strip()
    
    if font.getsize(text)[0] <= max_width:
        lines.append(text) 
    else:
        words = text.split(' ')  
        i = 0
        while i < len(words):
            line = '' 
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:                
                if words[i] != '\n':
                    line = line + words[i] + " "
                    i += 1
                else:
                    break
            if not line:
                if words[i] != '\n':
                    line = words[i]
                i += 1

            lines.append(line)    

    return lines

def draw_text(text, filename, font_name, hex_color, x, y, align, font_size, vertical_align='top'):
    path = 'data/' + id + '/images/'

    image = Image.open(path + filename)
    image_size = image.size

    font_file_path = 'fonts/' + font_name + '.ttf'
    font = ImageFont.truetype(font_file_path, size=font_size, encoding="unic")
 
    lines = text_wrap(text, font, 1720)
    line_height = font.getsize('hg')[1]
    color = rgb_hex_to_dec(hex_color)
    draw = ImageDraw.Draw(image)

    if vertical_align == 'center':
        text_height = line_height * len(lines)
        y = (800 - text_height) / 2 + 100

    w = 0

    for text in lines:
        if align == 'center':
            W = x
            w, h = draw.textsize(text, font=font)
            draw.text(xy=((W - w) / 2, y), text=text, fill=color, font=font)
        elif align == 'right':
            w, h = draw.textsize(text, font=font)
            draw.text(xy=(x - w, y), text=text, fill=color, font=font)
        else:
            draw.text(xy=(x, y), text=text, fill=color, font=font)
        
        y = y + line_height

    image.save(path + filename, optimize=True)

    # The outer x bounds of the (centered, x=1920) text
    return ((1920 / 2) - (w / 2), (w / 2) + (1920 / 2), y)

def rgb_hex_to_dec(hex_string):
    hex_string = hex_string.replace('#', '')
    r = int(hex_string[:2], 16)
    g = int(hex_string[2:4], 16)
    b = int(hex_string[4:], 16)

    return (r, g, b)

def write_blank_image(rgb, filename):
    mode = 'RGB'
    size = (1920, 1080)
    color = rgb_hex_to_dec(rgb)

    path = 'data/' + id + '/images/'
    if not os.path.exists(path):
        os.makedirs(path)

    image = Image.new(mode, size, color)
    image.save(path + filename)

def write_blank_images_post():
    write_blank_image(post_background_rgb, 'post.png')
    print('[Info] Wrote background image for post')

def write_blank_images_comments(comments, done, c, length):
    for comment in comments:
        i = comment['_id']
        write_blank_image(comment_background_rgb, 'comment_' + str(i) + '.png')
        print('[Info] Wrote background image for comment (' + str(i + 1) + '/' + str(length) + ')')

    done[c] = True

def draw_line(filename, coords, width, hex_color):
    path = 'data/' + id + '/images/'

    image = Image.open(path + filename)

    color = rgb_hex_to_dec(hex_color)
    draw = ImageDraw.Draw(image)

    draw.line(coords, fill=color, width=width)

    image.save(path + filename, optimize=True)

def write_post_text(post):
    x_left, x_right, y_top = draw_text(post['title'], 'post.png', 'Roboto-Medium', post_text_rgb, 1920, 275, 'center', 60)

    draw_line('post.png', (480, (y_top + 600) / 2, 1440, (y_top + 600) / 2), 4, post_text_rgb)

    draw_text(post['upvotes'], 'post.png', 'Roboto-MediumItalic', post_text_rgb, x_left, 600, 'left', 45)
    draw_text(post['author'], 'post.png', 'Roboto-MediumItalic', post_text_rgb, x_right, 600, 'right', 45)

    draw_text('r/AskReddit', 'post.png', 'Roboto-Regular', post_text_rgb, 30, 1015, 'left', 35)
    draw_text(post['date'], 'post.png', 'Roboto-Regular', post_text_rgb, 1890, 1015, 'right', 35)
    draw_text('seenit', 'post.png', 'Roboto-LightItalic', post_text_rgb, 1920, 995, 'center', 50)

    print('[Info] Wrote text for post')

def write_comments_text(comments, done, c, length):
    for comment in comments:
        i = comment['_id']
        draw_text(post['title'], 'comment_' + str(i) + '.png', 'Roboto-Regular', comment_text_rgb, 30, 30, 'left', 35)

        font_size = 45
        font_file_path = 'fonts/' + 'Roboto-Light' + '.ttf'
        font = ImageFont.truetype(font_file_path, size=font_size, encoding="unic")
        lines = text_wrap(comment['text'], font, 1720)
        line_height = font.getsize('hg')[1]
        text_height = line_height * len(lines)
        while text_height > 800:
            font_size -= 1
            font = ImageFont.truetype(font_file_path, size=font_size, encoding="unic")
            lines = text_wrap(comment['text'], font, 1720)
            line_height = font.getsize('hg')[1]
            text_height = line_height * len(lines)

        draw_text(comment['text'], 'comment_' + str(i) + '.png', 'Roboto-Light', comment_text_rgb, 100, 100, 'left', font_size, 'center')

        draw_text(comment['upvotes'], 'comment_' + str(i) + '.png', 'Roboto-Italic', comment_text_rgb, 1060, 1005, 'center', 42)
        draw_text(comment['author'], 'comment_' + str(i) + '.png', 'Roboto-Italic', comment_text_rgb, 2780, 1005, 'center', 42)

        draw_text('r/AskReddit', 'comment_' + str(i) + '.png', 'Roboto-Regular', comment_text_rgb, 30, 1015, 'left', 35)
        draw_text(post['date'], 'comment_' + str(i) + '.png', 'Roboto-Regular', comment_text_rgb, 1890, 1015, 'right', 35)
        draw_text('(' + str(i + 1) + ' / ' + str(length) + ')', 'comment_' + str(i) + '.png', 'Roboto-LightItalic', comment_text_rgb, 1920, 995, 'center', 50)

        print('[Info] Wrote text for comment (' + str(i + 1) + '/' + str(length) + ')')

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

    filename = 'data/' + id + '/data.json'
    with open(filename) as f:
        data = json.load(f)

    write_blank_images_post()
    multithread(write_blank_images_comments, n_threads, data['comments'])

    global post
    post = data['post']
    write_post_text(post)

    multithread(write_comments_text, n_threads, data['comments'])

    return True