#import config
import pymongo
import os # NEW
from tweepy import OAuthHandler, Cursor, API
from tweepy import Stream


client = pymongo.MongoClient(host="mongodb", port=27017)
db = client.tweet_db
collection = db.tweet_db
#API_KEY=${twitter_api_key} # NEW
#API_SECRET=${twitter_api_secret} # NEW

API_KEY = os.environ.get('twitter_api_key') # NEW
API_SECRET = os.environ.get('twitter_api_secret') # NEW
print(API_KEY)

def authenticate():
    """Function for handling Twitter Authentication. Please note
       that this script assumes you have a file called config.py
       which stores the 2 required authentication tokens:

       1. API_KEY
       2. API_SECRET
     

    See course material for instructions on getting your own Twitter credentials.
    """
    auth = OAuthHandler(API_KEY, API_SECRET)
    return auth

if __name__ == '__main__':
    auth = authenticate()
    api = API(auth)

    cursor = Cursor(
        api.user_timeline,
        id = 'elonmusk',
        tweet_mode = 'extended'
    )

    for status in cursor.items(10):
        text = status.full_text

        # take extended tweets into account
        # TODO: CHECK
        if 'extended_tweet' in dir(status):
            text =  status.extended_tweet.full_text
        if 'retweeted_status' in dir(status):
            r = status.retweeted_status
            if 'extended_tweet' in dir(r):
                text =  r.extended_tweet.full_text
        tweet = {
            'text': text,
            'username': status.user.screen_name,
            'followers_count': status.user.followers_count
        }
        print(tweet) 
        
        collection.insert_one(tweet) # NEW - INSERT TO DB
        print(tweet)
        
 
