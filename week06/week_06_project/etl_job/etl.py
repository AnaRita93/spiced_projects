import time
import logging
import pymongo
import random
import re
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Establish a connection to the MongoDB server
client = pymongo.MongoClient(host="mongodb", port=27017)

# Select the database you want to use withing the MongoDB server
db = client.tweet_db
collection = db.tweet_db
#time.sleep(10)

# Connect to Postgres
POSTGRES_USER=${pingudb_user}
POSTGRES_PASSWORD=${pingudb_password}
DB = 'pingudb'
HOST = 'postgres_database'
PORT = '5432'

URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:{PORT}/{DB}"
pg = create_engine(URI,echo=True)


#pg = create_engine('postgresql://postgres:1234@postgres_database:5432/pingudb', echo=True)

pg.execute('''CREATE TABLE IF NOT EXISTS tweets (
    text VARCHAR(512),
    sentiment NUMERIC
);
''')


analyser = SentimentIntensityAnalyzer()


def extract():
    """gets a random tweet"""
    tweets = list(collection.find())
    if tweets:
        t = random.choice(tweets)
        return t
        

def transform(tweet):
    """use vader to calcualte sentiment polarity"""
    text = re.sub("'", "", tweet["text"])
    sentiment = analyser.polarity_scores(text)['compound']
    result = [text, sentiment]
    return result
    
def load(tweet, sentiment):
    """load the data into pg"""
    pg.execute(f"""INSERT INTO tweets (text, sentiment) VALUES ('''{tweet}''', {sentiment});""")

while True:
    tweet = extract()
    print('EXTRACT')
    if tweet:
        result = transform(tweet)
        print('TRANSFORM')
        load(result[0], result[1])
        print('LOAD')
    time.sleep(10)



















