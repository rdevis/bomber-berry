#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twitter import *

CONSUMER_KEY = "X"
CONSUMER_SECRET = "X"
TOKEN_KEY = "X"
TOKEN_SECRET = "X"

def sendTweet(message):
	try:
		t = Twitter(auth=OAuth(TOKEN_KEY, TOKEN_SECRET,CONSUMER_KEY, CONSUMER_SECRET))
		t.statuses.update(status=message)
	except:
		pass