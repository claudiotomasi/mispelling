#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv, string, random, numpy, codecs, sys
import re,string
#Twitter API credentials
consumer_key = "yrvZ7JAMm8jJ8dsYewLsf7OrA"
consumer_secret = "Xb1Fd6dVykFGScinOfyqiyQKYtBR19ASLSTEaf0Y58vExaaeAC"
access_key = "135605919-s4heOuOWQIszNOIeFdBgh1kESfqlB7Jl471kwqcB"
access_secret = "lH1YZ9VjghCOeCFrS8S4A8oF6Rg9P8pgPrzSG6ipQRjqg"


def strip_links(text):
    char_regex = re.compile('[^a-zA-Z\. ]')
    legals  = re.findall(char_regex, text)
    for l in legals:
        text= text.replace(l[0], '')
    return text

def strip_all_entities(text):
    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,'.')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

def remove_hashtags_links(tweet):
	return strip_all_entities(strip_links(tweet))

def total_perturbation(string_tweets, pert):
    length = len(string_tweets)
    sizePerturbation = numpy.uint8(length * 10/ 100)
    lista = list(string_tweets)
    for j in range(1, sizePerturbation):
        newChar = random.choice(string.letters[:26])
        what = random.randint(1, length-1)
        #while line[what] == ' ' or line[what] == "\'":
        	#what = random.randint(0, length-1)
        lista[what] = newChar
        string_tweets = ''.join(lista)
    pert.write(unicode(string_tweets))


def single_perturbation(f, outtweets):
	for i in outtweets:
		line = i[2].decode('utf-8')
		length = len(line)
		sizePerturbation = numpy.uint8(length * 5/ 100)
		for j in range(1, sizePerturbation):
			lista = list(line)
			newChar = random.choice(string.letters[:26])
			what = random.randint(1, length-1)
			#while line[what] == ' ' or line[what] == "\'":
				#what = random.randint(0, length-1)
			lista[what] = newChar
			line = ''.join(lista)
		f.write(unicode(line)+" ")


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	#initialize a list to hold all the tweepy Tweets
	alltweets = []

	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)

	#save most recent tweets
	alltweets.extend(new_tweets)

	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)

		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

		#save most recent tweets
		alltweets.extend(new_tweets)

		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		print "...%s tweets downloaded so far" % (len(alltweets))

	#transform the tweepy tweets into a 2D array that will populate the csv
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

	#write the csv
	with open('training/%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)

	string_tweets = ""
	with codecs.open("training/%s_original.txt" % screen_name, "w", 'utf-8-sig') as f:
		for tweet in outtweets:
			line = tweet[2].decode('utf-8')
			line = remove_hashtags_links(line)
			string_tweets += line+" "
		f.write(unicode(string_tweets)) #aggiugnere \n ?

	nTweets = len(outtweets)

	with codecs.open("training/%s_testing.txt" % screen_name, "w", 'utf-8-sig') as perturbation:
            total_perturbation(string_tweets, perturbation)


	#with codecs.open("training/%s_singlePert.txt" % screen_name, "w", 'utf-8-sig') as f:
		#single_perturbation(f, outtweets)



if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets(sys.argv[1])
