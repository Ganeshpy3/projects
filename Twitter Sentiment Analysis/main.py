import re
import pandas as pd
import tweepy
from textblob import TextBlob

class TwitterSentimentAnalysis:
    def __init__(self,cousumer_key,consumer_secret,access_token,access_token_secret):
        self.consumer_key=consumer_key
        self.consumer_secret=consumer_secret
        self.access_token=access_token
        self.access_token_secret=access_token_secret

    def authenticate(self):
        try:
            self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            self.auth.set_access_token(self.access_token,self.access_token_secret)
            self.api = tweepy.API(self.auth)
            print("Authenticated Successfully")
            return True
        except:
            print("Error")
            return False

    def extract_tweets(self,username):
        self.tweet= []
        self.public_tweets = self.api.user_timeline(screen_name=username, count=1000, lang="en", tweet_mode='extended')
        for tweet in self.public_tweets:
            self.tweet.append(tweet.full_text)

    def clean_text(self,text):
        text = re.sub('@[A-Za-z0-9]+', '', text)
        text = re.sub("#", '', text)
        text = re.sub('RT[\s]+', '', text)
        text = re.sub('https?:\/\/\S+', '', text)
        return text
    def polarity(self,tweets):
        polarit=TextBlob(tweets).sentiment.polarity
        if polarit>0:
            return "Positive"
        elif polarit<0:
            return "Negative"
        else:
            return "Neutral"
    def clean_tweets(self):
        self.cleaned_tweet=pd.DataFrame(self.tweet,columns=["Tweets"])
        self.cleaned_tweet["Tweets"]=self.cleaned_tweet["Tweets"].apply(self.clean_text)
        self.cleaned_tweet["Polarity"]=self.cleaned_tweet["Tweets"].apply(self.polarity)

    def sentiment(self):
        val=self.cleaned_tweet["Polarity"].value_counts(normalize=True)
        return val*100
#go to Twitter Developer account
consumer_key="Your_Cusumer_Key"
consumer_secret="Consumer_Secret"
access_token="ToKen"
access_token_secret="Token"



username=input("Twitter Account")
if __name__=='__main__':
    app=TwitterSentimentAnalysis(consumer_key,consumer_secret,access_token,access_token_secret)
    sucess=app.authenticate()
    if sucess:
        app.extract_tweets(username)
        app.clean_tweets()
        val=app.sentiment()
        print(val)
    else:
        print("Please Check token / secret keys")
