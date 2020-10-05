#!/usr/bin/env python3
import os

# cmd = f""
# os.system('wc -w static/txt/hashtags.txt | awk '{print $1}'')

category = ['influencers', 'hashtags', 'locations']
hashtag_text = (f'static/txt/{category[1]}.txt', category[1])
print(hashtag_text[0])

num_hashtags = os.system('wc -w static/txt/hashtags.txt | awk \'{print $1}\'')