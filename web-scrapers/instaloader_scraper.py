# -*-coding:utf-8 -*-
'''
@File    :   instaloader.py
@Time    :   2023/01/24 15:05:33
@Author  :   MittyYu 
@Desc    :   None
'''

import pandas as pd
import os
import csv, time, re, json
import instaloader
from datetime import datetime
from itertools import dropwhile, takewhile
import h_post
import random

class MyRateController(instaloader.RateController):
    def sleep(self, secs: float):
        wait_time = random.uniform(10, 20)
        print(wait_time)
        time.sleep(wait_time)


class Scraper:
    def __init__(self) -> None:
        self.L = instaloader.Instaloader(
                download_pictures=False,
                download_videos=False, 
                download_video_thumbnails=False,
                compress_json=False, 
                download_geotags=False, 
                post_metadata_txt_pattern=None, 
                max_connection_attempts=0,
                download_comments=False,
            )
        self.id = "mittyu_8"
        self.password = "890527mittyu"
        self.hashtag_list = ['beachcleanup']
        self.weight_keyword = {"lbs", "lb", "kg", "kgs"}
        self.language = 'English'
        self.post_dic = {}
        self.h_post_list = []
        
    def user_login(self):
        try:
            self.L.login(self.id, self.password)
            self.L.context.log("Logging in as %s..." % self.id)
            self.L.load_session_from_file(self.id)
        
        # not finished
        except:
            if not self.L.context.is_logged_in:
                self.L.context.log("Session file does not exist yet - Logging in.")
                self.L.context.log("Username: %s" %self.id)
                self.L.context.log("Password: %s" %self.password)
                self.L.context.log("User_agent: %s" %self.L.context.user_agent)
                self.L.context.log("Logged in: %s" %self.L.context.is_logged_in)
                self.L.context.log("Session file: %s" %self.L.context.session_filename)
                self.L.context.log("Session file exists: %s" %self.L.context.session_file_exists())
                self.L.context.log("Session file loaded: %s" %self.L.context.session_file_loaded)
            
    # def scrap(self):
    #     self.post = instaloader.Hashtag.from_name(self.L.context, self.hashtag).get_posts()

    def post_to_csv(self):
        i=0
        self.post_dic = {'caption':[], 'hashtag':[], 'location':[]}
        words_of_interest = {"lbs", "lb", "kg", "kgs"}

        for i,post in enumerate(self.L.get_hashtag_posts(self.hashtag)):
            try:
                if any(x in post.caption for x in words_of_interest):
                    self.post_dic['caption'].append(post.caption)
                    self.post_dic['hashtag'].append(post.caption_hashtags)
                    self.post_dic['location'].append(post.location)
                if len(self.post_dic) > 5:
                    break
            except:
                pass
            
    def hashtag_post_between(self, hashtag, SINCE, UNTIL, cnt):
        """_summary_
        Get post with the hashtag between a time interval
        Args:
            hashtag (string): name of the hashtag
        """
        c=0
        posts = self.L.get_hashtag_posts(hashtag)
        print("capturing posts from "+str(SINCE)+" to "+str(UNTIL))
        print("Hashtag:", hashtag)
        hashtag_post = h_post.Hashtag_Post(hashtag, SINCE, UNTIL)
        
        print(posts)
        for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
            try:
                if any(x in post.caption for x in self.weight_keyword):
                    hashtag_post.owner_username_list.append(post.owner_username)
                    hashtag_post.owner_id_list.append(post.owner_id)
                    hashtag_post.post_date_list.append(post.date_utc)
                    hashtag_post.location_list.append(post.location)
                    hashtag_post.post_caption_list.append(post.caption)
                    hashtag_post.tagged_users_list.append(post.tagged_users)
                    hashtag_post.caption_mentions_list.append(post.caption_mentions)
                    hashtag_post.is_video_list.append(post.is_video)
                    hashtag_post.video_view_count_list.append(post.video_view_count)
                    hashtag_post.video_duration_list.append(post.video_duration)
                    hashtag_post.likes_list.append(post.likes)
                    hashtag_post.comments_list.append(post.comments)
                    hashtag_post.post_url_list.append(post.shortcode)
                    hashtag_post.hashtags_caption_list.append(post.caption_hashtags)
                    c += 1
                if c > cnt:
                    break
            except Exception as e:
                print(e)
                

        for date, name, location in zip(hashtag_post.post_date_list, hashtag_post.owner_username_list, hashtag_post.location_list):
            print(date, name, location)

        
        hashtag_post.post_to_csv()
        self.h_post_list.append(hashtag_post)
        print(hashtag_post.df)
        
        
S = Scraper()
S.user_login()

SINCE = datetime(2023, 1, 31) # Recent Date / format = (yyyy, mm, dd)
UNTIL = datetime(2022, 9, 1) # Oldest Date /format = (yyyy, mm, dd)
cnt = 50
for hashtag in S.hashtag_list:
    S.hashtag_post_between(hashtag, SINCE, UNTIL, cnt)