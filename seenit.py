import web_scraper
import data_to_images
import data_to_speech
import data_to_videos
import combine_videos
import time

time_1 = time.time()

# To select a specific, pre-saved thread
id = '2019-10-01-16-52-12_dbky3c'

# Retrieve new data
#id = web_scraper.fetch_data()
time_2 = time.time()

# Multithread to number_of_comments; single-core usage is extremely low, so it's better to overthread
#data_to_images.convert_data(id, 30)
time_3 = time.time()

# Multithread to number_of_comments; single-core usage is extremely low, so it's better to overthread
#data_to_speech.convert_data(id, 30)
time_4 = time.time()

# Multithread to just under 100% use; ffmpeg multithreads well already, so fewer threads is better
#data_to_videos.convert_data(id, 12)
time_5 = time.time()

# Concatenate video files
combine_videos.convert_data(id, 'movie_py_fade', 1)
time_6 = time.time()

# Timer for stats :)
print('[Time] web_scraper: ' + str(time_2 - time_1))
print('[Time] data_to_images: ' + str(time_3 - time_2))
print('[Time] data_to_speech: ' + str(time_4 - time_3))
print('[Time] data_to_videos: ' + str(time_5 - time_4))
print('[Time] combine_videos: ' + str(time_6 - time_5))
print('[Time] seenit: ' + str(time_6 - time_1))