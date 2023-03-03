# -*-coding:utf-8 -*-
'''
@File    :   post.py
@Time    :   2023/01/31 21:10:22
@Author  :   MittyYu 
@Desc    :   None
'''

import pandas as pd
from datetime import datetime

class Hashtag_Post:
    def __init__(self, hashtag, since, until) -> None:
        self.hashtag = hashtag
        self.timeframe = [since, until]
        self.owner_username_list = []
        self.owner_id_list = []
        self.post_date_list = []
        self.location_list = []
        self.post_caption_list = []
        self.tagged_users_list = [] 
        self.caption_mentions_list = []
        self.is_video_list = []
        self.video_view_count_list = []
        self.video_duration_list = []
        self.likes_list = []
        self.comments_list = []
        self.post_date_list = []
        self.post_url_list = []
        self.hashtags_caption_list = []
        self.df = pd.DataFrame()
        
    def post_to_csv(self):
        self.df = pd.DataFrame({
            "owner_username": self.owner_username_list,
            "owner_id": self.owner_id_list,
            "post_date": self.post_date_list,
            "location": self.location_list,
            "likes": self.likes_list,
            "comments": self.comments_list,
            "post_caption": self.post_caption_list,
            "hashtags_caption": self.hashtags_caption_list,
            "tagged_users": self.tagged_users_list,
            "caption_mentions": self.caption_mentions_list,
            "is_video": self.is_video_list,
            "video_view_count": self.video_view_count_list,
            "video_duration": self.video_duration_list,
            "post_shortcode": self.post_url_list,
            })

        self.df.to_csv(self.hashtag+".csv")
        
    def __repr__(self):
        print("Hashtag:", self.hashtag)
        print("Time interval: from", self.timeframe[0], "to", self.timeframe[1])
        print(self.df)