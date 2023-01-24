/#!/usr/bin/env python
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
from instaloader import Instaloader


class Scraper:
    def __init__(self) -> None:
        self.L = Instaloader()
        self.id = 'cme291ocean'
        self.password = 'CME291cleanup'
        self.hashtag = 'oceancleanup'
        self.weight_keyword = {"lbs", "lb", "kg", "kgs"}
        self.language = 'English'
    
    
    def login(self):
        try:
            self.L.login(self.id, self.password)
            self.L.context.log("Logging in as %s..." % self.id)
            self.L.load_session_from_file(self.id)
            self.L.login(self.id, self.password)
        
        # not finished
        except:
            if not self.L.context.is_logged_in:
                self.L.context.log("Session file does not exist yet - Logging in.")
                self.L.context.log("Username: %s" %self.id)
                self.L.context.log("Password: %s" %self.password)
                self.L.context.log("User_agent: %s" %L.context.user_agent)
                self.L.context.log("Logged in: %s" %L.context.is_logged_in)
                self.L.context.log("Session file: %s" %L.context.session_filename)
                self.L.context.log("Session file exists: %s" %L.context.session_file_exists())
                self.L.context.log("Session file loaded: %s" %L.context.session_file_loaded)
            
    
    