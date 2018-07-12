import tweepy
import json
from paralleldots import set_api_key, get_api_key
import nltk
from nltk.corpus import *
from collections import Counter

consumer_key = " "
consumer_secret = " "
access_token = " "
access_secret = " "
oauth = tweepy.OAuthHandler(consumer_key, consumer_secret)
oauth.set_access_token(access_token, access_secret)
api = tweepy.API(oauth)


def display_menu():
    global tw
    tw = True
    message = str
    while tw == True:
        print("WELCOME TO TWITTER_BOT!!")
        print("1. Retrieve tweets")
        print("2. Count the followers")
        print("3. Determine the sentiment")
        print("4. Compare tweets")
        print("5. Analyse the top usage")
        print("6. Tweet a message")
        print("7. Exit")
        option = int(input("What do you want to choose ?"))
        if option == 1:
            Get_Search()
            display_menu()
        elif option == 2:
            fcount()
            display_menu()
        elif option == 3:
            sentiment_analysis()
            display_menu()
        elif option == 4:
            compare()
            display_menu()
        elif option == 5:
            top_usage()
            display_menu()
        elif option == 6:
            tweet_status(new = message)
            display_menu()
        elif option == 7:
            print("Come again!")
            tw = False
        else:
            print("Enter a above mentioned value!")
            display_menu()

def query():
    global tweets
    tweet_input = input("Of which star do you want to see the tweets?")
    tweet_input = "*" + tweet_input
    tweets = api.search(q = tweet_input)

def Get_Search():
    query()
    status = tweets[0]
    json_str = json.dumps(status._json,indent=4,sort_keys=True)
    print(json_str)

def fcount():
    query()
    print("UserName      Follower Count")
    for tweet in tweets:
        print(tweet.user.name+"     "+str(tweet.user.followers_count))


def sentiment_analysis():
    twpos = 0
    twneu = 0
    twneg = 0
    query()
    from paralleldots import similarity, taxonomy, sentiment, emotion, abuse
    set_api_key("")
    get_api_key()
    for tweet in tweets:
        text = tweet.text
        sentiment_value = sentiment(text)
        values1 = sentiment_value
        if values1 == "positive":
            twpos = twpos + 1
        elif values1 == "negative":
            twneg = twneg + 1
        else:
            twneu = twneu + 1
    if twneu > twneg and twneu > twpos:
        print("Sentiment: Neutral")
    elif twneg > twneu and twneg > twpos:
        print("Sentiment: Negative")
    else:
        print("Sentiment: Positive")


def compare():
    twword = 1
    twword1 = 4
    tweets = api.user_timeline(screen_name="sharukhkhan", count=200, tweet_mode="extended")
    for tweet_compare in tweets:
        fulltext = tweet_compare.full_text
        tmp = []
        tmp.append(fulltext)
        temp = tmp
        import re
        cur_tweet = re.sub(r"http\S+", "", str(temp))
        cur_tweet = re.split(r"\s", cur_tweet)
        for word in cur_tweet:
            word=word.upper()
            if word == "IND" or word == "MANNAT" or word == "MUMBAI" or word == "INDIA":
                twword = twword + 1
    print("Sharukh Khan in India: "+ str(twword))


    tweets = api.user_timeline(screen_name="salmankhan", count=200, tweet_mode="extended")
    for tweet_compare in tweets:
        fulltext = tweet_compare.full_text
        tmp = []
        tmp.append(fulltext)
        temp = tmp
        import re
        cur_tweet = re.sub(r"http\S+", "", str(temp))
        cur_tweet = re.split(r"\s", cur_tweet)
        for word in cur_tweet:
            word = word.upper()
            if word == "DELHI":
                twword1 = twword1 + 1
    print("Salman Khan in Delhi: " + str(twword1))

def top_usage():
    global count
    stop_words = set(stopwords.words('english'))
    a = [a.upper() for a in stop_words]
    tweets = api.user_timeline(screen_name="shahrukhkhan", count=200, tweet_mode="extended")
    for tweet_compare in tweets:
        fulltext = tweet_compare.full_text
        tmp = []
        tmp.append(fulltext)
        temp = tmp
        import re
        cur_tweet = re.sub(r"http\S+", "", str(temp))
        cur_tweet1 = re.split(r"\s", cur_tweet)
        cur_tweet = [d for d in cur_tweet1 if not d in stop_words]
        cur_tweet=[]
        for d in cur_tweet1:
            if d not in stop_words:
                cur_tweet.append(d)
                count = Counter(cur_tweet).most_common(10)
        print(count)


def tweet_status(new):
    message = input("What do you want?")
    api.update_status(message)

print("Twitter_Bot")
display_menu()