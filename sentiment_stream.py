from textblob import TextBlob
import tweepy
import json
import sys

class MoodMapStreamer(tweepy.StreamListener):
	def __init__(self):
		self.avg_polarity = 0
		self.count = 0

	def on_data(self, data):
		decoded = json.loads(data)
		try:
			text = decoded['text'].encode('ascii', 'ignore')
		except KeyError:
			return True
		curr = TextBlob(text)

		if curr.polarity != 0:
			print '%s --> %f' % (text, curr.polarity)
			self.count += 1
			self.avg_polarity = (self.avg_polarity*(self.count - 1) + curr.polarity) / self.count
			print 'N: %d, Average Polarity: %f' % (self.count, self.avg_polarity)

		return True

	def on_error(self, status):
		print status


consumer_key = '' #api key
consumer_secret = '' #api secret
access_token = '' #access token
access_token_secret = '' #access token secret

auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

locations = [[-122.75,36.8,-121.75,37.8], [-74,40,-73,41], [-122.75,36.8,-121.75,37.8,-74,40,-73,41], [-180,-90,180,90]]

stream = tweepy.Stream(auth, MoodMapStreamer(), timeout=None)

stream.filter(locations = locations[int(sys.argv[1])])
