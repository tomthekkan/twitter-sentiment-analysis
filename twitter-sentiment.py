#!/usr/bin/python
import sys
import csv
import tweepy
import matplotlib.pyplot as plt

from collections import Counter
from aylienapiclient import textapi

if sys.version_info[0] <3:
	input = raw_input


#Twitter credentials

consumer_key = "5rfrqgRyXdYRnlkSZt8lqMDev"
consumer_secret = "V89gZ2JJXQoUwTqIs816eGGAqVCJgyQs9QULYu7dngdDBwVyip"
access_token = "979242557312921605-JzzDjoGvlaG56kO2CZEdrXZKWB2UzzB"
access_token_secret = "92YFF0E2s1wD7jGetXPFQD8R1nTW4Apgtxl0qwSsbUGPG"

#Aylien credentials

application_id = "7c953276"
application_key = "60c95180c4ff203cd4fe40e36eeaeea6"

#Setup instance of tweepy

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Setup instance of aylien text api

client = textapi.Client(application_id,application_key)

# search twitter for the interest

query = input("What subject do you want to analyze")
number = input("How many tweets do you want to analyze?\n")


results = api.search(
	lang = "en",
	q=query + "-rt",
	count = number,
	result_type = "recent"
	)

print "Tweets gathered\n"

# create csv file for store tweets

neg_c=0
pos_c=0
neut_c=0
filename = '/home/tom/Documents/study/python/scraping/sentiment_analysis_of_{}_tweets_about_{}.csv'.format(number,query)
f= open(filename,'w')
header = "Tweet,Sentiment\n"
f.write(header)
for result in results:
	tweet = result.text
	tidy_tweet = tweet.strip().encode('ascii','ignore')

	if len(tweet) == 0:
		print "Empty tweet"
		continue
	response = client.Sentiment({'text': tidy_tweet})
	print response
	f.write(response['text'].replace(',','|').replace(';','|').replace('\n','|') +',' + response['polarity'] + '\n')
	print response['text'].replace(',','|')
	if response['polarity'] == 'positive':
		pos_c += 1
	elif response['polarity'] == 'neutral':
		neut_c += 1
	else:
		neg_c += 1
	
f.close()


# declare variables for pie chart

colors = ['green','red','grey']
sizes = [pos_c,neg_c,neut_c]
labels = 'Positive', 'Negative', 'Neutral'

plt.pie(
	x=sizes,
	shadow = colors,
	labels = labels,
	startangle=90
)
plt.title("Sentiment of {} Tweets about {}_of(Positive:{}|Neutral:{}|Negative:{}".format(number,query,pos_c,neut_c,neg_c))
plt.show()

