files = ['data_to_images.py', 'data_to_speech.py', 'data_to_videos.py', 'seenit.py', 'web_scraper.py']
lines = 0

for file_name in files:
    with open(file_name) as f:
        contents = f.read()
        lines += len(contents.split('\n'))

print(lines)