import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import datetime
import os

# Returns the source for a webpage after page has been rendered and JS loaded
def load(link):
    driver = webdriver.Firefox()
    driver.get(link)
    driver.execute_script( \
        'window.scrollTo(0, document.body.scrollHeight);' + '\n' + \
        'var lenOfPage = document.body.scrollHeight;' + '\n' + \
        'return lenOfPage;' \
        )
    time.sleep(3)
    html_doc = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

# Obtains the #1 upvoted subreddit post of the day
def get_post(subreddit):
    link = 'http://www.reddit.com/r/' + subreddit + '/top/?t=day'
    soup = load(link)

    top_post = soup.findAll('div', {'class': 'Post'})[0]
    upvotes = list(top_post.children)[0].get_text() + ' upvotes'
    author = list(list(list(list(list(top_post.children)[1].children)[0].children)[0].children)[0].children)[1].get_text()
    title = list(list(list(top_post.children)[1].children)[1].children)[0].get_text()
    number_of_comments = list(list(list(list(top_post.children)[1].children)[3].children)[1].children)[0].get_text()
    link = 'http://www.reddit.com/' + list(list(list(list(top_post.children)[1].children)[3].children)[1].children)[0].get('href')
    id = link \
        .replace('http://www.reddit.com//r/AskReddit/comments/', '') \
        [:6]
    
    post = {
        '_id': id,
        'author': author,
        'link': link,
        'number_of_comments': number_of_comments,
        'date': None,
        'title': title,
        'upvotes': upvotes
    }

    return post

def get_post_date(post):
    soup = load(post['link'])
    date_html = soup.find('time')
    post['date'] = soup.find('time').get_text()

    return post

# Fetches comments and metadata from a specified Reddit post
def get_comments(post):
    soup = load(post['link'])

    comment_n = 30
    comment_table = list(soup.findAll('div', {'class': 'commentarea'})[0].children)[3]
    comments = []
    table_divs = list(comment_table.children)
    for div in table_divs:
        # Exception may occur here
        if 'thing' in div.attrs['class']:
            comments.append(div)
            if len(comments) == comment_n:
                break

    comments_data = []
    for i, comment in enumerate(comments):
        text = list(list(comment.children)[2].children)[1].get_text()
        relative_time = list(list(list(comment.children)[2].children)[0].children)[7] # 
        author = 'u/' + list(list(list(comment.children)[2].children)[0].children)[1].get_text()
        if i < 15:
            upvotes = list(list(list(comment.children)[2].children)[0].children)[7].get_text()
        else:
            upvotes = list(list(list(comment.children)[2].children)[0].children)[4].get_text()

        text = text \
            [:len(text) - 2] \
            .replace('\n\n', '\n') \
            .replace('  ', ' ')

        comment = {
            '_id': i,
            'author': author,
            'text': text,
            'upvotes': upvotes
        }

        comments_data.append(comment)

    return comments_data

# Formatted date string used for identifying files
def get_date_string():
    now = datetime.datetime.now()

    time = {
        'year': str(now.year),
        'month': str(now.month),
        'day': str(now.day),
        'hour': str(now.hour),
        'minute': str(now.minute),
        'second': str(now.second)
    }

    date_parts = [time['year']]
    time_segments = ['month', 'day', 'hour', 'minute', 'second']
    for time_segment in time_segments:
        if len(time[time_segment]) == 1:
            time[time_segment] = '0' + time[time_segment]
        date_parts.append(time[time_segment])

    date_string = '-'.join(date_parts)

    return date_string

# Outputs Python data objects into json files
def save_data(data, id, date_string):
    path = 'data/' + date_string + '_' + id + '/'
    if not os.path.exists(path):
        os.makedirs(path)

    filename = path + 'data.json'
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)

# If a function is occasionally faulty, it's run through this handler
def attempt(func_name, max_attempts, args):
    i = 0
    while i < max_attempts:
        i += 1
        try:
            output = globals()[func_name](args)
            print('[Info]', func_name,'succeeded (' + str(i) + '/' + str(max_attempts) + ' tries)')
            return output
        except Exception as e:
            print('[Error]', func_name, 'failed (' + str(i) + '/' + str(max_attempts) + ' tries)', e)
            if i == max_attempts:
                print('[Error]', func_name, 'has failed')
                exit()

def fetch_data():
    max_attempts = 3
    post = attempt('get_post', max_attempts, ('AskReddit'))
    post = attempt('get_post_date', max_attempts, (post))
    comments = attempt('get_comments', max_attempts, (post))

    date_string = get_date_string()
    id = post['_id']
    data = {
        '_id': date_string + '_' + id,
        'post': post,
        'comments': comments
    }

    save_data(data, id, date_string)

    return date_string + '_' + id