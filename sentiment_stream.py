from textblob import TextBlob
import tweepy
import json
import re

def filter(tweet_dict):
		try:
			text = tweet_dict['text']
		except KeyError:
			return None

		#No urls
		if re.search("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", text):
			return None

		#Only feel words
		if not re.search("(i feel)|(i am feeling)|(i'm feeling)|(i dont feel)|(I'm)|(Im)|(I am)|(makes me)", text):
			return None

		return text

class MoodMapStreamer(tweepy.StreamListener):
	def __init__(self):
		self.count = 0

	def on_data(self, data):
		decoded = json.loads(data)

		#text = filter(decoded)

		try:
			text = decoded['text']
		except KeyError:
			return None

		if text:
			p_text = TextBlob(text)

			self.count += 1

			print "%s (n = %d, polarity = %f)" % (text, self.count, p_text.polarity)

		return True

	def on_error(self, status):
		print status


consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

stream = tweepy.Stream(auth, MoodMapStreamer(), timeout=None)

stream.filter(locations = [-180, -90, 180, 90])